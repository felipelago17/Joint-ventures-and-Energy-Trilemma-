"""
Weekly research digest scraper.

Pulls recent items from Norwegian Offshore Directorate, ADNOC newsroom,
EIA Today in Energy, WEC Trilemma site, SSRN Energy Law, Journal of World
Energy Law & Business (OUP), and energy-pedia upstream news, then
prepends a new dated section to news/digest.md.
"""

from __future__ import annotations

import datetime
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import feedparser
import requests
from bs4 import BeautifulSoup

DIGEST_PATH = Path("news/digest.md")
TODAY = datetime.date.today().isoformat()
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; PhD-digest-bot/1.0; "
        "+https://github.com/felipelago17/Joint-ventures-and-Energy-Trilemma-)"
    )
}
MAX_ITEMS = 5  # per source


@dataclass
class Item:
    title: str
    url: str
    date: str = ""
    snippet: str = ""


@dataclass
class Source:
    name: str
    items: List[Item] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fetch_feed(url: str, label: str) -> Source:
    """Generic RSS/Atom feed fetcher."""
    src = Source(name=label)
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:MAX_ITEMS]:
            src.items.append(
                Item(
                    title=entry.get("title", "(no title)").strip(),
                    url=entry.get("link", ""),
                    date=entry.get("published", "")[:10] if entry.get("published") else "",
                    snippet=BeautifulSoup(
                        entry.get("summary", ""), "lxml"
                    ).get_text()[:200].strip(),
                )
            )
    except Exception as exc:  # noqa: BLE001
        src.items.append(Item(title=f"[Error fetching {label}: {exc}]", url=""))
    return src


def scrape_html_links(url: str, label: str, link_selector: str,
                      base: str = "", skip_suffixes: tuple = ()) -> Source:
    """Generic HTML news-page scraper for sites without public RSS."""
    src = Source(name=label)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        seen: set[str] = set()
        for a in soup.select(link_selector):
            href = a.get("href", "")
            if not href or href in seen:
                continue
            if any(href.endswith(s) for s in skip_suffixes):
                continue
            seen.add(href)
            full_url = href if href.startswith("http") else base + href
            title = a.get_text(" ", strip=True)
            if title and len(title) > 10:
                src.items.append(Item(title=title, url=full_url))
            if len(src.items) >= MAX_ITEMS:
                break
    except Exception as exc:  # noqa: BLE001
        src.items.append(Item(title=f"[Error fetching {label}: {exc}]", url=""))
    return src


# ---------------------------------------------------------------------------
# Scrapers
# ---------------------------------------------------------------------------


def scrape_sodir() -> Source:
    """Norwegian Offshore Directorate (renamed from NPD, 2024) — HTML scrape."""
    return scrape_html_links(
        url="https://www.sodir.no/en/whats-new/news/",
        label="Norwegian Offshore Directorate (Sodir)",
        link_selector="a[href*='/en/whats-new/news/']",
        base="https://www.sodir.no",
        skip_suffixes=("/rss/", "/subscribe-to-news/", "/news/"),
    )


def scrape_adnoc() -> Source:
    """ADNOC Newsroom — HTML scrape (no public RSS)."""
    return scrape_html_links(
        url="https://www.adnoc.ae/en/news-and-media/press-releases",
        label="ADNOC Newsroom",
        link_selector="a[href*='/news-and-media/press-releases/']",
        base="https://www.adnoc.ae",
    )


def scrape_eia() -> Source:
    """US Energy Information Administration — Today in Energy RSS."""
    return fetch_feed(
        "https://www.eia.gov/rss/todayinenergy.xml",
        "EIA — Today in Energy",
    )


def scrape_wec() -> Source:
    """WEC Trilemma Index — HTML scrape (JS-heavy; returns landing page note)."""
    src = Source(name="WEC World Energy Trilemma Index")
    url = "https://trilemma.worldenergy.org/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        for a in soup.find_all("a", href=True)[:20]:
            text = a.get_text(strip=True)
            href = a["href"]
            if len(text) > 15 and ("report" in text.lower() or "index" in text.lower()):
                full = href if href.startswith("http") else "https://trilemma.worldenergy.org" + href
                src.items.append(Item(title=text, url=full))
                if len(src.items) >= MAX_ITEMS:
                    break
        if not src.items:
            src.items.append(
                Item(
                    title="WEC Trilemma Index — visit site for latest rankings",
                    url=url,
                )
            )
    except Exception as exc:  # noqa: BLE001
        src.items.append(Item(title=f"[Error fetching WEC: {exc}]", url=""))
    return src


def scrape_ssrn() -> Source:
    """SSRN Energy & Resources Law eJournal — RSS feed."""
    # journal_id=1342872 is the Energy & Resources Law eJournal
    return fetch_feed(
        "https://papers.ssrn.com/sol3/Jeljour_results.cfm"
        "?form_name=journalbrowse&journal_id=1342872&RSSFeed=yes",
        "SSRN — Energy & Resources Law eJournal",
    )


def scrape_jwelb() -> Source:
    """Journal of World Energy Law & Business (OUP) — advance-access feed."""
    src = Source(name="Journal of World Energy Law & Business (OUP)")
    # Try feedparser autodiscovery first, then known OUP site-ID patterns
    candidates = [
        "https://academic.oup.com/jwelb/advance-articles",
        "https://academic.oup.com/rss/site_5504/advanceAccess_5504.xml",
        "https://academic.oup.com/rss/site_5505/advanceAccess_5505.xml",
    ]
    for url in candidates:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                for entry in feed.entries[:MAX_ITEMS]:
                    src.items.append(
                        Item(
                            title=entry.get("title", "(no title)").strip(),
                            url=entry.get("link", ""),
                            date=entry.get("published", "")[:10]
                            if entry.get("published")
                            else "",
                            snippet=BeautifulSoup(
                                entry.get("summary", ""), "lxml"
                            ).get_text()[:200].strip(),
                        )
                    )
                break
        except Exception:  # noqa: BLE001
            continue
    if not src.items:
        src.items.append(
            Item(
                title="JWELB advance articles — visit journal page",
                url="https://academic.oup.com/jwelb/advance-articles",
            )
        )
    return src


def scrape_irena() -> Source:
    """IRENA — International Renewable Energy Agency news RSS."""
    return fetch_feed(
        "https://www.irena.org/rssfeed",
        "IRENA — International Renewable Energy Agency",
    )


def scrape_energy_pedia() -> Source:
    """energy-pedia — upstream oil & gas news (RSS)."""
    return fetch_feed(
        "https://www.energy-pedia.com/rss.aspx",
        "energy-pedia (upstream oil & gas)",
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_source(src: Source) -> str:
    lines = [f"\n### {src.name}\n"]
    if not src.items:
        lines.append("_No items retrieved._\n")
        return "\n".join(lines)
    for item in src.items:
        title = item.title or "(untitled)"
        link_part = f" — [{item.url}]({item.url})" if item.url else ""
        date_part = f" `{item.date}`" if item.date else ""
        lines.append(f"- **{title}**{date_part}{link_part}")
        if item.snippet:
            lines.append(f"  {textwrap.shorten(item.snippet, width=180)}")
    return "\n".join(lines) + "\n"


def build_section(sources: list[Source]) -> str:
    header = f"\n## Digest — {TODAY}\n"
    body = "".join(render_source(s) for s in sources)
    return header + body + "\n---\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    sources = [
        scrape_sodir(),
        scrape_adnoc(),
        scrape_eia(),
        scrape_irena(),
        scrape_wec(),
        scrape_ssrn(),
        scrape_jwelb(),
        scrape_energy_pedia(),
    ]

    new_section = build_section(sources)

    existing = DIGEST_PATH.read_text(encoding="utf-8")

    marker = "<!-- AUTO-GENERATED CONTENT BELOW"
    if marker in existing:
        split_point = existing.find(marker)
        prefix = existing[:split_point]
        suffix = existing[split_point:]
        updated = prefix + new_section + "\n" + suffix
    else:
        updated = existing + "\n" + new_section

    DIGEST_PATH.write_text(updated, encoding="utf-8")
    print(f"Digest written to {DIGEST_PATH} ({len(sources)} sources).")


if __name__ == "__main__":
    main()
