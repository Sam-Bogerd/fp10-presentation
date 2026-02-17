import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm
from datetime import datetime, timedelta

# ── Load data ──
with open("data/metr-horizon-v1.1.json") as f:
    data = json.load(f)

doubling_days = data["doubling_time_in_days"]["from_2023_on"]["point_estimate"]  # ~128 days

# ── Color scheme from presentation ──
COLORS = {
    "blue":       "#8098FF",
    "blue_dark":  "#4a6ed4",
    "red":        "#F47D5B",
    "red_dark":   "#c45a3d",
    "green_dark": "#7cb668",
    "green_darker":"#5a9a4a",
    "purple":     "#A09AC8",
    "purple_dark":"#7a72a8",
    "black":      "#0E0705",
    "grey":       "#F6F5F9",
    "grey_text":  "#475569",
    "grid":       "#e8e8ec",
    "border":     "#e2e0e8",
    "non_frontier":"#c4c0cc",
}

COMPANY_COLORS = {
    "openai":    COLORS["blue"],
    "anthropic": COLORS["red"],
    "google":    COLORS["green_dark"],
}

# ── Model metadata ──
MODEL_META = {
    "gpt2":                               ("GPT-2",          "openai"),
    "davinci_002":                         ("Davinci",        "openai"),
    "gpt_3_5_turbo_instruct":             ("GPT-3.5",        "openai"),
    "gpt_4":                              ("GPT-4",           "openai"),
    "gpt_4_1106_inspect":                 ("GPT-4 Turbo",    "openai"),
    "gpt_4_turbo_inspect":                ("GPT-4T",         "openai"),
    "gpt_4o_inspect":                     ("GPT-4o",          "openai"),
    "o1_preview":                         ("o1-preview",      "openai"),
    "o1_inspect":                         ("o1",              "openai"),
    "o3_inspect":                         ("o3",              "openai"),
    "gpt_5_2025_08_07_inspect":           ("GPT-5",          "openai"),
    "gpt_5_1_codex_max_inspect":          ("GPT-5.1",        "openai"),
    "gpt_5_2":                            ("GPT-5.2",        "openai"),
    "claude_3_opus_inspect":              ("Claude 3 Opus",  "anthropic"),
    "claude_3_5_sonnet_20240620_inspect": ("Claude 3.5",     "anthropic"),
    "claude_3_5_sonnet_20241022_inspect": ("Claude 3.5v2",   "anthropic"),
    "claude_3_7_sonnet_inspect":          ("Claude 3.7",     "anthropic"),
    "claude_4_opus_inspect":              ("Claude 4",       "anthropic"),
    "claude_4_1_opus_inspect":            ("Claude 4.1",     "anthropic"),
    "claude_opus_4_5_inspect":            ("Opus 4.5",       "anthropic"),
    "gemini_3_pro":                       ("Gemini 3",       "google"),
}

# Models to label (key milestones only)
LABEL_SET = {
    "gpt2", "davinci_002", "gpt_3_5_turbo_instruct", "gpt_4",
    "o1_preview", "claude_3_7_sonnet_inspect",
    "o3_inspect", "gpt_5_2025_08_07_inspect", "gemini_3_pro",
    "claude_opus_4_5_inspect", "gpt_5_2",
}

# ── Parse models ──
models = []
for key, result in data["results"].items():
    release_date = datetime.strptime(result["release_date"], "%Y-%m-%d")
    m = result["metrics"]["p50_horizon_length"]
    name, company = MODEL_META.get(key, (key, "unknown"))
    models.append({
        "key": key,
        "name": name,
        "company": company,
        "date": release_date,
        "p50": m["estimate"],
        "ci_low": m["ci_low"],
        "ci_high": m["ci_high"],
        "is_sota": result["metrics"]["is_sota"],
    })

models.sort(key=lambda m: m["date"])

# ── Y-axis cap at 500 hours (~3 weeks) ──
Y_MAX = 500

# ── Trend line: anchor on GPT-4 (2023-03-14, ~3.52h) ──
anchor_date = datetime(2023, 3, 14)
anchor_hours = 3.52
slope = np.log(2) / doubling_days

date_min = datetime(2019, 1, 1)
date_max = datetime(2026, 3, 1)
trend_days_arr = np.linspace(0, (date_max - date_min).days, 400)
trend_dates = [date_min + timedelta(days=float(d)) for d in trend_days_arr]
trend_vals = [
    anchor_hours * 2 ** (((date_min + timedelta(days=float(d))) - anchor_date).days / doubling_days)
    for d in trend_days_arr
]
trend_vals = np.array(trend_vals)

# CI band for trend
doubling_ci_low = data["doubling_time_in_days"]["from_2023_on"]["ci_low"]
doubling_ci_high = data["doubling_time_in_days"]["from_2023_on"]["ci_high"]
trend_hi = np.array([
    anchor_hours * 2 ** (((date_min + timedelta(days=float(d))) - anchor_date).days / doubling_ci_low)
    for d in trend_days_arr
])
trend_lo = np.array([
    anchor_hours * 2 ** (((date_min + timedelta(days=float(d))) - anchor_date).days / doubling_ci_high)
    for d in trend_days_arr
])

# ── Try to use Plus Jakarta Sans ──
try:
    font_path = None
    for f in fm.findSystemFonts():
        if "plusjakarta" in f.lower().replace(" ", ""):
            font_path = f
            break
    if font_path:
        prop = fm.FontProperties(fname=font_path)
        FONT_FAMILY = prop.get_name()
    else:
        FONT_FAMILY = "sans-serif"
except Exception:
    FONT_FAMILY = "sans-serif"

plt.rcParams.update({
    "font.family": FONT_FAMILY,
    "font.size": 12,
})

# ── Plot ──
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_alpha(0)
ax.patch.set_facecolor("white")
ax.patch.set_alpha(1)

# Trend CI band
trend_hi_clipped = np.clip(trend_hi, 0, Y_MAX)
trend_lo_clipped = np.clip(trend_lo, 0, Y_MAX)
ax.fill_between(trend_dates, trend_lo_clipped, trend_hi_clipped,
                color=COLORS["purple"], alpha=0.12, zorder=1)

# Trend line
trend_vals_clipped = np.clip(trend_vals, 0, Y_MAX)
ax.plot(trend_dates, trend_vals_clipped,
        color=COLORS["purple"], linewidth=2.5, linestyle="--", alpha=0.7, zorder=2,
        label="Doubling ~every 4 months")

# Data points
for m in models:
    color = COMPANY_COLORS.get(m["company"], COLORS["non_frontier"]) if m["is_sota"] else COLORS["non_frontier"]
    alpha = 0.9 if m["is_sota"] else 0.6

    ci_lo_err = max(m["p50"] - m["ci_low"], 0)
    ci_hi_err = max(m["ci_high"] - m["p50"], 0)
    # Clamp error bars to chart bounds
    ci_hi_err = min(ci_hi_err, Y_MAX - m["p50"]) if m["p50"] < Y_MAX else 0

    ax.errorbar(
        m["date"], min(m["p50"], Y_MAX),
        yerr=[[ci_lo_err], [ci_hi_err]],
        fmt="o", color=color, ecolor=color, elinewidth=1.5,
        capsize=3, capthick=1.5, markersize=7 if m["is_sota"] else 5.5,
        alpha=alpha, zorder=4,
        markeredgecolor="white", markeredgewidth=1.2,
    )

    # Labels for selected SOTA models
    if m["is_sota"] and m["key"] in LABEL_SET:
        text_color = {
            "openai": COLORS["blue_dark"],
            "anthropic": COLORS["red_dark"],
            "google": COLORS["green_darker"],
        }.get(m["company"], COLORS["grey_text"])

        # Default offsets
        dx, dy, ha = 10, -6, "left"

        # Per-model adjustments
        if m["key"] == "o1_preview":               dx, dy, ha = -10, -8, "right"
        if m["key"] == "o3_inspect":               dx, dy, ha = -10, -4, "right"
        if m["key"] == "gpt_5_2025_08_07_inspect": dx, dy, ha = -10, -10, "right"
        if m["key"] == "gemini_3_pro":             dx, dy, ha = -10, -10, "right"
        if m["key"] == "claude_opus_4_5_inspect":  dx, dy = 10, 4
        if m["key"] == "gpt_5_2":                  dx, dy = 10, -10

        ax.annotate(
            m["name"],
            (m["date"], min(m["p50"], Y_MAX)),
            textcoords="offset points",
            xytext=(dx, dy),
            fontsize=9,
            fontweight="bold",
            color=text_color,
            ha=ha,
            zorder=5,
        )

# ── Y-axis: human-readable time labels ──
y_ticks = [0, 24, 72, 168, 336, 500]
y_labels = ["0", "1 day", "3 days", "1 wk", "2 wks", "3 wks"]
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels)
ax.set_ylim(bottom=0, top=Y_MAX)

# ── X-axis ──
ax.set_xlim(date_min, date_max)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# ── Styling ──
ax.set_ylabel("Task time horizon (50% success)", fontsize=13, color=COLORS["black"], fontweight=500)

ax.tick_params(axis="both", colors=COLORS["grey_text"], labelsize=11)
ax.spines["bottom"].set_color(COLORS["black"])
ax.spines["left"].set_color(COLORS["black"])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(True, axis="y", alpha=0.5, color=COLORS["grid"], linewidth=0.7)

# ── Legend ──
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

legend_elements = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["blue"],
           markersize=8, markeredgecolor="white", markeredgewidth=1, label="OpenAI"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["red"],
           markersize=8, markeredgecolor="white", markeredgewidth=1, label="Anthropic"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["green_dark"],
           markersize=8, markeredgecolor="white", markeredgewidth=1, label="Google"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["non_frontier"],
           markersize=7, markeredgecolor="white", markeredgewidth=1, label="Non-frontier"),
    Line2D([0], [0], color=COLORS["purple"], linewidth=2.5, linestyle="--",
           alpha=0.7, label="Doubling ~every 4 months"),
]

legend = ax.legend(
    handles=legend_elements,
    loc="upper left",
    fontsize=10,
    frameon=True,
    facecolor="white",
    edgecolor=COLORS["border"],
    framealpha=0.95,
)

plt.tight_layout()
plt.savefig("metr_horizon_chart.png", dpi=200, transparent=True)
print("Saved to metr_horizon_chart.png")
