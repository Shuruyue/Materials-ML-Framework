# Research Atlas Collection

A monorepo hosting two interactive, self-contained research atlases — each a bilingual (EN/ZH) static web page with zero dependencies.

## Projects

| Project | Description | Papers | Open |
|---------|-------------|--------|------|
| [**ML × Materials Science Atlas**](materials-ml-atlas/) | Maps the intersection of machine learning and materials science — from objective design through deployment | 500+ | [Open](materials-ml-atlas/index.html) |
| [**Epochal Engineering Papers Atlas**](epochal-atlas/) | Studies how landmark engineering and STEM papers changed technology, organized by breakthrough mechanisms | 1,055 | [Open](epochal-atlas/index.html) |

## Quick Start

```bash
git clone https://github.com/Shuruyue/Materials-ML-Framework.git
cd Materials-ML-Framework
```

Open either project's `index.html` in your browser. No server, no build step, no dependencies.

## Repository Layout

```
materials-ml-atlas/                 ML × Materials Science Research Atlas
  index.html                        Entry point
  src/                              Styles, content, rendering, i18n
  data/                             500+ curated sources (JSON + JS)
  tools/                            OpenAlex data harvester
  CONTRIBUTING.md                   Contribution guidelines

epochal-atlas/                      Epochal Engineering Papers Atlas
  index.html                        Entry point
  src/                              Styles, content, rendering, i18n
  data/                             1,055 curated sources + 107 canonical paths
  tools/                            OpenAlex data harvester
```

## Shared Design Principles

- **First-principles organization** — structure by mechanisms, not by trending model names
- **Evidence-backed** — every claim pressure-tested against curated bibliographies
- **Self-contained** — zero runtime dependencies, no CDN, no framework
- **Bilingual** — full English and Traditional Chinese with one-click switching
- **Static deployment** — open the HTML file and it works

## Technology

- Vanilla HTML / CSS / JavaScript (no frameworks, no build tools)
- CSS custom properties, responsive grid layout, print stylesheets
- Python 3.10+ with `requests` for data-harvesting pipelines
- [OpenAlex](https://openalex.org/) as the bibliometric data source

## License

[MIT](LICENSE)
