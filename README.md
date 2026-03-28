# Static site generator

A small Python tool that turns Markdown in `content/` into HTML using `template.html`, copies assets from `static/` into `public/`, and mirrors the folder layout in the output.

## Generate the site

```bash
python3 src/main.py
```

## Preview locally

```bash
./main.sh
```

This generates the site, then serves `public/` on [http://localhost:8888](http://localhost:8888).

## Tests

```bash
./test.sh
```

(Boot.dev course project — custom Markdown → HTML pipeline.)
