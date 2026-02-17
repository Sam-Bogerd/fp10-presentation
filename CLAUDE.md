# Project: AI Possible Futures Presentation

Single-file Reveal.js 5.1.0 presentation (`index.html`) with CFG branding.

## Local Preview

Start a local server and preview in Chrome:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080/index.html` in the browser.
Navigate to a specific slide with hash: `http://localhost:8080/index.html#/4` (0-indexed).

The project has pre-approved permissions for `python -m http.server` in `.claude/settings.local.json`.

## METR Chart (Slide 5)

The METR Horizon benchmark chart on slide 5 is generated programmatically from `data/metr-horizon-v1.1.json`.

- **Data source**: `data/metr-horizon-v1.1.yaml` (original), converted to `data/metr-horizon-v1.1.json`
- **Conversion**: Run `python -c "import yaml,json; d=yaml.safe_load(open('data/metr-horizon-v1.1.yaml')); json.dump(d,open('data/metr-horizon-v1.1.json','w'),indent=2,default=str)"`
- **Chart script**: Inline `<script>` block in `index.html` (search for `buildMetrChart`)
- **Scale**: Linear Y-axis (0-500 hours), linear X-axis (2019-2026)
- **Features**: Error bars (95% CI), exponential trend line with confidence band, color-coded by company

To update the chart data, edit the YAML, re-run the conversion, and reload.

## Style Guide

- Colors: `--blue` (OpenAI), `--red` (Anthropic), `--green-dark` (Google), `--purple` (trends), `--grey` (background)
- Fonts: Playfair Display (headings), Plus Jakarta Sans (body)
- Slide size: 1280x720, 4% margin
