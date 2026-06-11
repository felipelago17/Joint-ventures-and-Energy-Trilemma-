# Joint Ventures and the Energy Trilemma: Norway vs UAE

PhD research repository — comparative governance analysis of upstream joint ventures under competing energy-trilemma imperatives.

## Research Questions

1. How do joint-venture governance structures in Norway and the UAE balance energy security, equity, and sustainability?
2. How do JV structures contribute to or constrain each pillar of the energy trilemma?
3. How are regulatory frameworks evolving in response to the energy transition?

## Repository Layout

```
.
├── analysis/
│   ├── uae-ccus-jv-joa-governance.md    # UAE CCUS/CCS JV/JOA governance module
│   └── norway-ccus-jv-joa-governance.md # Norway CCUS/CCS JV/JOA governance module
├── literature/
│   └── by-theme/          # Annotated reading lists per topic
│       ├── jv-governance.md
│       ├── energy-trilemma.md
│       ├── norway-upstream.md
│       ├── uae-upstream.md
│       ├── jv-contribution.md
│       └── computational-sovereignty.md
├── references/
│   ├── uae-ccus-bibliography.md         # UAE CCUS secondary sources (29 entries)
│   ├── uae-ccus.bib                     # BibTeX of above
│   └── primary-instruments.bib          # BibTeX for primary legislation (Norway + UAE)
├── data/
│   ├── ghasha-participating-interests.csv  # Indicative Ghasha concession interests
│   └── subscribers.txt                     # Daily digest subscriber list
├── regulations/
│   ├── README.md          # Paired statutory-vs-contractual index (four-gap table)
│   ├── norway/            # Annotated source register: CO2 Storage Regs, EL001, Havtil
│   ├── uae/               # Annotated source register: Climate Law, concession framework
│   └── international/     # UNCLOS, Energy Charter Treaty, OPEC docs
├── news/
│   └── digest.md          # Auto-updated daily digest (GitHub Actions)
├── docs/                  # MkDocs source (published to GitHub Pages)
├── .github/workflows/
│   └── daily-digest.yml   # Daily email digest workflow
├── mkdocs.yml
└── CITATION.cff
```

## Literature Inventory

### JV Governance (`literature/by-theme/jv-governance.md`)

| Entry | Type | Key Relevance |
|-------|------|---------------|
| Ankura JV Index H1 2023 | Industry report | Green JV volumes (61% of deal flow); ADNOC/Masdar 3-way restructuring as UAE governance case |
| Ankura 2023 Annual Review | Industry report | Full-year record JV volumes; host-country-triggered natural resource restructurings |
| AIEN 2023 Model International JOA | Model contract | Governance benchmark: GHG, human rights, sanctions, decommissioning; Norway/UAE gap analysis |
| Northern Lights JV (13 sources) | Reports / conference papers | CCS JV governance: state oversight, open-source T&S model, IOC accountability, Norway→UAE knowledge transfer |

### UAE Upstream (`literature/by-theme/uae-upstream.md`)

| Entry | Type | Key Relevance |
|-------|------|---------------|
| Palacios & Vidotto Caricati (CGEP, May 2023) | Policy report | ADNOC ESG disclosure gap; governance-environment linkage; NOC state-ownership framework |

### Energy Trilemma (`literature/by-theme/energy-trilemma.md`)

_Entries to be added._

### JV Contribution to the Trilemma (`literature/by-theme/jv-contribution.md`)

_Entries to be added. Framework and search queries in place._

### Norway Upstream (`literature/by-theme/norway-upstream.md`)

_Entries to be added._

## Analysis Modules

### UAE CCUS/CCS JV Governance (`analysis/uae-ccus-jv-joa-governance.md`)

| Section | Content |
|---------|---------|
| No standalone CCS regime | Emirate-level concession architecture; federal Climate Law; Abu Dhabi MRV |
| Project landscape | Al Reyadah (2016), Habshan (FID 2023), Hail & Ghasha multi-party JV |
| The governance gap | Long-tail liability; state liability transfer; pore-space tenure; MRV/financial assurance |
| Conclusion | Concession-embedded CCUS model; comparison with Norway Northern Lights |

Bibliography: [`references/uae-ccus-bibliography.md`](references/uae-ccus-bibliography.md) (29 entries) |
BibTeX: [`references/uae-ccus.bib`](references/uae-ccus.bib) |
Data: [`data/ghasha-participating-interests.csv`](data/ghasha-participating-interests.csv)

### Norway CCUS/CCS JV Governance (`analysis/norway-ccus-jv-joa-governance.md`)

| Section | Content |
|---------|---------|
| Regulatory architecture | Section 4-7 storage licence; Longship state funding; PSA/NPD/Gassnova oversight |
| Northern Lights JV | Formation; open-source infrastructure model; Phase 1/2 capacity |
| How Norway resolves the governance gap | Codified liability transfer; separate storage tenure; mandatory MRV |
| Comparative conclusion | Norway vs UAE categorical comparison table |

## Regulations Source Registers

Paired annotated registers presenting the **statutory-tenure (Norway) vs. contractual /
concession-embedded (UAE)** contrast. See [`regulations/README.md`](regulations/README.md)
for the four-gap index table.

| Register | Key instruments |
|----------|----------------|
| [`regulations/norway/`](regulations/norway/README.md) | Continental Shelf Act 1963; CO₂ Storage Regulations 2014 (Chs 4, 7, 8); CO₂ Safety Regs 2020; EL001 "Aurora" licence |
| [`regulations/uae/`](regulations/uae/README.md) | UAE Constitution Art. 23; Climate Law 2024; Cabinet Decision 67/2024; Ghasha concession framework |

BibTeX for primary instruments: [`references/primary-instruments.bib`](references/primary-instruments.bib) (11 entries)

## Daily Digest Setup

A GitHub Actions workflow (`.github/workflows/daily-digest.yml`) sends a structured HTML email every day at 08:00 UTC summarising commits, new files, regulatory updates, news digest activity, and upcoming deadlines.

Two repository secrets are required:

| Secret | Value |
|--------|-------|
| `GMAIL_APP_PASSWORD` | 16-character app password generated at **Google Account → Security → 2-Step Verification → App passwords** |
| `DIGEST_RECIPIENTS` | Comma-separated list of recipient addresses (e.g. `supervisor@lsbu.ac.uk,colleague@example.com`) |

Add secrets at **GitHub → Repository → Settings → Secrets and variables → Actions → New repository secret**.

To test without waiting for 08:00 UTC, go to **Actions → Daily Email Digest → Run workflow**.

For subscription requests, see the [Subscribe](https://felipelago17.github.io/Joint-ventures-and-Energy-Trilemma-/subscribe/) page on the research site.

## Documentation Site

GitHub Pages: <https://felipelago17.github.io/Joint-ventures-and-Energy-Trilemma->

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Citation

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

## License

Research materials © Felipe Lago. Code in `.github/` is MIT-licensed.
