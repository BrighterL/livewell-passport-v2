# Livewell Passport — site revamp

Static site. No framework, no build dependencies beyond Python 3.

- `src/styles.css`, `src/site.js` — shared styles and script
- `src/legal.txt` — privacy notice and terms as crawled from the live site (converted at build time)
- `build.py` — all page content and templates. Edit copy here.
- `assets/img/` — client photos resized from livewellpassport.com
- `dist/` — deployable output (upload this folder to any static host)
- `dist-artifact/` — same site, index page without the document skeleton, for the claude.ai preview (not committed)
- `review/` — the claude.ai review shell that embeds the site and stores notes

Build: `python3 build.py`

Deploy: every push to `main` runs `.github/workflows/pages.yml`, which builds `dist/` and publishes it to GitHub Pages.

Before launch:
1. Contact form: set `data-endpoint` on the form in `build.py` (contact_page) to a form service URL (Formspree, Basin, or the clinic's CRM). Until then the success panel tells visitors to email or call.
2. Replace placeholder stock photos in `assets/img/` with clinic photography when available.
3. Confirm membership pricing ($500/mo, regular $750) and the limited-time wording.
4. Add a 404 rule on the host that serves `404.html`.
