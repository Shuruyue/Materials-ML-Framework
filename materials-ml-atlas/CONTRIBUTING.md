# Contributing to ML × Materials Science Atlas

Thank you for your interest in contributing.  This document explains how to
propose changes, report issues, and refresh the evidence base.

## Repository layout

```
index.html              Entry point (open in any browser)
src/
  styles.css            Stylesheet
  atlas-content.js      Research-framework data (architecture, taxonomy, …)
  atlas-i18n.js         Localisation strings (EN + ZH-Hant)
  atlas-app.js          Rendering engine
data/
  atlas-sources.js      Generated bibliography (do NOT edit by hand)
  atlas-sources.json    Same data in plain JSON
tools/
  build_data.py         OpenAlex harvester that regenerates the bibliography
  requirements.txt      Python dependencies for the build script
```

## Quick start

1. Clone the repository.
2. Open `index.html` in a browser — no build step needed.
3. To regenerate the evidence base, run:

```bash
pip install -r tools/requirements.txt
python tools/build_data.py
```

## How to contribute

| Type | What to do |
|------|-----------|
| **Fix a typo or broken link** | Open a pull request directly. |
| **Add or update a taxonomy branch** | Edit `src/atlas-content.js`, then open a PR with a brief rationale. |
| **Add a translation** | Add a new language key to the objects in `src/atlas-i18n.js`. |
| **Refresh the bibliography** | Run `python tools/build_data.py` and commit the updated `data/` files. |
| **Report an issue** | Use the GitHub Issues tab with a descriptive title. |

## Style guidelines

- All research text is written in **English** (the Chinese translation mirrors it).
- Commit messages follow conventional style: `fix:`, `feat:`, `docs:`, `refactor:`.
- JavaScript uses `"use strict"`, `var` for globals, and avoids runtime dependencies.
- CSS uses custom properties defined in `:root`.

## Code of conduct

Be respectful, constructive, and focused on improving the scientific quality
of the framework.  Contributions are reviewed for accuracy and clarity.
