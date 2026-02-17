from pathlib import Path
import re

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]


COLORS = {
    "blue": "#8098FF",
    "red": "#F47D5B",
    "green_dark": "#7cb668",
    "purple": "#A09AC8",
    "black": "#0E0705",
}

CATEGORY_COLORS = {
    "EU": COLORS["blue"],
    "US Government": COLORS["red"],
    "US Philanthropy": COLORS["green_dark"],
}

TITLE_SIZE = 24
AXIS_LABEL_SIZE = 14
TICK_LABEL_SIZE = 12
VALUE_LABEL_SIZE = 11
LEGEND_SIZE = 11


def pick_fonts():
    local_font_dirs = [
        PROJECT_ROOT / "fonts/plus-jakarta-sans",
        PROJECT_ROOT / "fonts/playfair-display",
        PROJECT_ROOT / "fonts",
    ]
    for local_font_dir in local_font_dirs:
        if not local_font_dir.exists():
            continue
        for pattern in ("*.ttf", "*.otf"):
            for font_file in local_font_dir.rglob(pattern):
                try:
                    fm.fontManager.addfont(str(font_file))
                except Exception:
                    pass

    names = sorted({f.name for f in fm.fontManager.ttflist})
    lower_map = {n.lower(): n for n in names}

    def match_font(candidates, fallback):
        for c in candidates:
            if c.lower() in lower_map:
                return lower_map[c.lower()]
        for c in candidates:
            c_low = c.lower()
            for n in names:
                if c_low in n.lower():
                    return n
        return fallback

    body = match_font(["Plus Jakarta Sans", "PlusJakartaSans"], "DejaVu Sans")
    title = match_font(["Playfair Display", "PlayfairDisplay"], body)
    return body, title


def style_axes(ax, grid_axis="x"):
    ax.set_facecolor("none")
    ax.set_axisbelow(True)
    ax.grid(axis=grid_axis, color="#e8e8ec", linestyle="-", linewidth=0.8, alpha=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["black"])
    ax.spines["bottom"].set_color(COLORS["black"])
    ax.tick_params(colors="#475569", labelsize=TICK_LABEL_SIZE)


def euro_label(v):
    if v >= 1_000_000_000:
        return f"EUR {v / 1_000_000_000:.1f}B"
    return f"EUR {v / 1_000_000:.0f}M"


def clean_name(name):
    return re.sub(r"\s+", " ", str(name)).strip()


def save_plot(fig, out_path):
    fig.patch.set_alpha(0.0)
    fig.savefig(out_path, dpi=220, transparent=True)
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_program_spending(df, out_dir, title_font):
    d = df.sort_values("Spending in Euros", ascending=False).copy()
    d["Program"] = d["Program"].map(clean_name)
    colors = [CATEGORY_COLORS.get(c, COLORS["purple"]) for c in d["Category"]]

    fig, ax = plt.subplots(figsize=(13, 8))
    bars = ax.barh(d["Program"], d["Spending in Euros"], color=colors, edgecolor="white", linewidth=1.0)
    ax.invert_yaxis()

    pad = d["Spending in Euros"].max() * 0.01
    for b, val in zip(bars, d["Spending in Euros"]):
        ax.text(val + pad, b.get_y() + b.get_height() / 2, euro_label(val), va="center", fontsize=VALUE_LABEL_SIZE, color=COLORS["black"])

    ax.set_title("Science Funding by Program (Annual, EUR)", fontsize=TITLE_SIZE, color=COLORS["black"], fontname=title_font, pad=14)
    ax.set_xlabel("Annual Spending (EUR)", fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    style_axes(ax, grid_axis="x")

    legend_handles = [
        plt.Line2D([0], [0], marker="s", linestyle="", markersize=10, markerfacecolor=CATEGORY_COLORS[k], markeredgecolor="white", label=k)
        for k in ["EU", "US Government", "US Philanthropy"]
        if k in d["Category"].unique()
    ]
    ax.legend(handles=legend_handles, frameon=True, facecolor="white", edgecolor="#e2e0e8", fontsize=LEGEND_SIZE, loc="lower right")
    plt.tight_layout()
    save_plot(fig, out_dir / "funders_spending_by_program.png")


def plot_category_totals(df, out_dir, title_font):
    d = (
        df.groupby("Category", as_index=False)["Spending in Euros"]
        .sum()
        .sort_values("Spending in Euros", ascending=False)
    )
    colors = [CATEGORY_COLORS.get(c, COLORS["purple"]) for c in d["Category"]]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    bars = ax.bar(d["Category"], d["Spending in Euros"], color=colors, edgecolor="white", linewidth=1.0)

    for b, val in zip(bars, d["Spending in Euros"]):
        ax.text(b.get_x() + b.get_width() / 2, val, euro_label(val), ha="center", va="bottom", fontsize=VALUE_LABEL_SIZE, color=COLORS["black"])

    ax.set_title("Total Annual Science Funding by Category (EUR)", fontsize=TITLE_SIZE, color=COLORS["black"], fontname=title_font, pad=14)
    ax.set_ylabel("Annual Spending (EUR)", fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    style_axes(ax, grid_axis="y")
    plt.tight_layout()
    save_plot(fig, out_dir / "funders_spending_by_category.png")


def plot_us_breakdown(df, out_dir, title_font):
    d = df[df["Category"] == "US Government"].sort_values("Spending in Euros", ascending=False).copy()
    d["Program"] = d["Program"].map(clean_name)

    fig, ax = plt.subplots(figsize=(12, 6.5))
    bars = ax.barh(d["Program"], d["Spending in Euros"], color=COLORS["red"], edgecolor="white", linewidth=1.0)
    ax.invert_yaxis()

    pad = d["Spending in Euros"].max() * 0.012
    for b, val in zip(bars, d["Spending in Euros"]):
        ax.text(val + pad, b.get_y() + b.get_height() / 2, euro_label(val), va="center", fontsize=VALUE_LABEL_SIZE, color=COLORS["black"])

    ax.set_title("US Government Science Funders (Annual, EUR)", fontsize=TITLE_SIZE, color=COLORS["black"], fontname=title_font, pad=14)
    ax.set_xlabel("Annual Spending (EUR)", fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    style_axes(ax, grid_axis="x")
    plt.tight_layout()
    save_plot(fig, out_dir / "us_government_funders_breakdown.png")


def main():
    source = PROJECT_ROOT / "data/science_funders_overview.ods"
    out_dir = PROJECT_ROOT / "graphs/science_funders"
    out_dir.mkdir(parents=True, exist_ok=True)

    body_font, title_font = pick_fonts()
    plt.rcParams.update(
        {
            "font.family": body_font,
            "font.size": TICK_LABEL_SIZE,
            "axes.titlesize": TITLE_SIZE,
            "axes.labelsize": AXIS_LABEL_SIZE,
            "legend.fontsize": LEGEND_SIZE,
        }
    )

    df = pd.read_excel(source, engine="odf")
    df.columns = [str(c).strip() for c in df.columns]
    df["Program"] = df["Program"].astype(str).str.strip()
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Spending in Euros"] = pd.to_numeric(df["Spending in Euros"], errors="coerce")
    df = df.dropna(subset=["Program", "Category", "Spending in Euros"]).copy()

    plot_program_spending(df, out_dir, title_font)
    plot_category_totals(df, out_dir, title_font)
    plot_us_breakdown(df, out_dir, title_font)


if __name__ == "__main__":
    main()
