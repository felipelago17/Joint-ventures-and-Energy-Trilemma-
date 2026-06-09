"""
Weekly research digest scraper.

Pulls recent items from NPD, ADNOC newsroom, IEA, WEC Trilemma Index,
SSRN Energy Law, and Journal of World Energy Law & Business, then
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
# Scrapers
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


def scrape_npd() -> Source:
    """Norwegian Petroleum Directorate — news RSS."""
    return fetch_feed(
        "https://www.npd.no/en/news/rss/",
        "NPD (Norwegian Petroleum Directorate)",
    )


def scrape_adnoc() -> Source:
    """ADNOC Newsroom — HTML scrape (no public RSS)."""
    src = Source(name="ADNOC Newsroom")
    url = "https://www.adnoc.ae/en/news-and-media/press-releases"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        # ADNOC uses anchor tags with press-release links
        articles = soup.select("a[href*='/news-and-media/press-releases/']")
        seen: set[str] = set()
        for a in articles:
            href = a.get("href", "")
            if not href or href in seen or href == url:
                continue
            seen.add(href)
            full_url = href if href.startswith("http") else "https://www.adnoc.ae" + href
            title = a.get_text(" ", strip=True)
            if title:
                src.items.append(Item(title=title, url=full_url))
            if len(src.items) >= MAX_ITEMS:
                break
    except Exception as exc:  # noqa: BLE001
        src.items.append(Item(title=f"[Error fetching ADNOC: {exc}]", url=""))
    return src


def scrape_iea() -> Source:
    """IEA — news RSS."""
    return fetch_feed(
        "https://www.iea.org/rssnews.xml",
        "IEA (International Energy Agency)",
    )


def scrape_wec() -> Source:
    """WEC Trilemma Index — HTML scrape (no RSS; returns landing page note)."""
    src = Source(name="WEC World Energy Trilemma Index")
    url = "https://trilemma.worldenergy.org/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        # WEC is a JS-heavy site; extract any visible text links
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
    """SSRN Energy Law — RSS feed."""
    return fetch_feed(
        "https://papers.ssrn.com/sol3/Jeljour_results.cfm?form_name=journalbrowse&journal_id=1342872&Network=no&SortOrder=ab_approval_date&abstracts=show&No=0&RSSFeed=yes",
        "SSRN — Energy & Environment Law",
    )


def scrape_jwelb() -> Source:
    """Journal of World Energy Law & Business — OUP RSS."""
    return fetch_feed(
        "https://academic.oup.com/rss/site_5504/advanceAccess_5504.xml",
        "Journal of World Energy Law & Business (OUP)",
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
        scrape_npd(),
        scrape_adnoc(),
        scrape_iea(),
        scrape_wec(),
        scrape_ssrn(),
        scrape_jwelb(),
    ]

    new_section = build_section(sources)

    existing = DIGEST_PATH.read_text(encoding="utf-8")

    # Insert new section after the header block (before the first "---" separator)
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
