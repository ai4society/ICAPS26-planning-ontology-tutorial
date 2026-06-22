# Website

The tutorial's static announcement site. Plain HTML/CSS (no build step), matching
the garnet design of the slide deck.

- **`index.html`** — the announcement landing page (overview, contents, notebooks,
  presenters, resources, citation).
- **`assets/`** — images used by the page (ontology schema, presenter photos, logos).

## Hosting (GitHub Pages)

Enable Pages -> *Deploy from a branch* -> `main` -> `/ (root)`. The repo-root
`../index.html` redirects to this folder, so the published site serves:

- `/` -> this announcement page (`website/`)
- `/slides/` -> the full-page HTML slide deck (present directly from the browser)

To preview locally, open `index.html`, or serve the repo root:

```bash
python -m http.server   # then visit http://localhost:8000/
```
