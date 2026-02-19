from pathlib import Path
import re

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]


COLORS = {
    "blue": "#8098FF",
    "blue_dark": "#4a6ed4",
    "red": "#F47D5B",
    "red_dark": "#c45a3d",
    "green": "#B4DBA2",
    "green_dark": "#7cb668",
    "green_darker": "#5a9a4a",
    "purple": "#A09AC8",
    "purple_dark": "#7a72a8",
    "yellow": "#FEDF9E",
    "yellow_dark": "#d4b870",
    "grey": "#F6F5F9",
    "black": "#0E0705",
    "teal": "#A2E1FF",
    "teal_dark": "#6bc4e8",
    "pink": "#FFB6BB",
}

REGION_COLORS = {
    "EU": COLORS["blue"],
    "Europe": COLORS["blue"],
    "US": COLORS["red"],
    "USA": COLORS["red"],
    "China": COLORS["green_dark"],
    "Japan": COLORS["purple"],
    "South Korea": COLORS["yellow"],
}

FALLBACK_COLORS = [COLORS["teal"], COLORS["pink"], COLORS["green"], COLORS["grey"]]

TITLE_SIZE = 24
AXIS_LABEL_SIZE = 14
TICK_LABEL_SIZE = 12
VALUE_LABEL_SIZE = 11
LEGEND_SIZE = 11
SOURCE_SIZE = 10


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


def clean_region(region):
    s = str(region).strip()
    if s == "USA":
        return "US"
    if s == "Europe":
        return "EU"
    return s


def clean_unit(unit):
    s = str(unit).strip().lower()
    if s == "percent":
        return "%"
    return s


def sanitize_filename(text):
    s = re.sub(r"[^a-z0-9]+", "_", text.strip().lower())
    return s.strip("_")


def value_label(v, unit):
    if unit == "%":
        return f"{v:.1f}%"
    if "percent gdp" in unit:
        return f"{v:.1f}% GDP"
    return f"{v:.1f}"


def unit_axis_label(unit):
    if unit == "%":
        return "Share (%)"
    if "percent gdp" in unit:
        return "Percent of GDP"
    return unit.title()


def color_for_region(region, fallback_idx=0):
    if region in REGION_COLORS:
        return REGION_COLORS[region]
    return FALLBACK_COLORS[fallback_idx % len(FALLBACK_COLORS)]


def style_axes(ax, grid_axis="y"):
    ax.set_facecolor("none")
    ax.set_axisbelow(True)
    ax.grid(axis=grid_axis, color="#e8e8ec", linestyle="-", linewidth=0.8, alpha=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["black"])
    ax.spines["bottom"].set_color(COLORS["black"])
    ax.tick_params(colors="#475569", labelsize=TICK_LABEL_SIZE)


def plot_single_region_timeseries(g, unit, title_font):
    fig, ax = plt.subplots(figsize=(11, 6))
    g = g.sort_values("year")
    region = g["region"].iloc[0]
    color = color_for_region(region)

    ax.plot(
        g["year"],
        g["value"],
        marker="o",
        linewidth=2.6,
        markersize=8,
        color=color,
        markeredgecolor="white",
        markeredgewidth=1.1,
    )
    for _, row in g.iterrows():
        ax.text(
            row["year"],
            row["value"],
            value_label(row["value"], unit),
            fontsize=VALUE_LABEL_SIZE,
            color=COLORS["black"],
            ha="center",
            va="bottom",
        )

    ax.set_title(g["indicator"].iloc[0], fontsize=TITLE_SIZE, color=COLORS["black"], fontname=title_font, pad=14)
    ax.set_xlabel("Year", fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    ax.set_ylabel(unit_axis_label(unit), fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    ax.set_xticks(sorted(g["year"].unique()))
    style_axes(ax, grid_axis="y")
    return fig, ax


def plot_single_year_multiregion(g, unit, title_font):
    fig, ax = plt.subplots(figsize=(11, 6))
    g = g.sort_values("value", ascending=False).reset_index(drop=True)
    colors = [color_for_region(r, i) for i, r in enumerate(g["region"])]
    bars = ax.barh(g["region"], g["value"], color=colors, edgecolor="white", linewidth=1.0)
    ax.invert_yaxis()

    for b, (_, row) in zip(bars, g.iterrows()):
        ax.text(
            row["value"] + (0.8 if unit == "%" else 0.06),
            b.get_y() + b.get_height() / 2,
            value_label(row["value"], unit),
            va="center",
            fontsize=VALUE_LABEL_SIZE,
            color=COLORS["black"],
        )

    ax.set_title(f'{g["indicator"].iloc[0]} ({int(g["year"].iloc[0])})', fontsize=TITLE_SIZE, color=COLORS["black"], fontname=title_font, pad=14)
    ax.set_xlabel(unit_axis_label(unit), fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    style_axes(ax, grid_axis="x")
    return fig, ax


def plot_grouped_bars(g, unit, title_font):
    fig, ax = plt.subplots(figsize=(11, 6))
    years = sorted(g["year"].unique())
    regions = sorted(g["region"].unique())
    pivot = g.pivot_table(index="year", columns="region", values="value", aggfunc="first").reindex(years)

    width = 0.8 / max(len(regions), 1)
    x = list(range(len(years)))
    for i, region in enumerate(regions):
        vals = pivot[region].tolist() if region in pivot.columns else [None] * len(years)
        x_pos = [v + (i - (len(regions) - 1) / 2) * width for v in x]
        bars = ax.bar(
            x_pos,
            vals,
            width=width,
            label=region,
            color=color_for_region(region, i),
            edgecolor="white",
            linewidth=0.9,
        )
        for b, val in zip(bars, vals):
            if pd.isna(val):
                continue
            ax.text(
                b.get_x() + b.get_width() / 2,
                b.get_height(),
                value_label(float(val), unit),
                fontsize=VALUE_LABEL_SIZE,
                ha="center",
                va="bottom",
                color=COLORS["black"],
            )

    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_title(g["indicator"].iloc[0], fontsize=TITLE_SIZE, color=COLORS["black"], fontname=title_font, pad=14)
    ax.set_xlabel("Year", fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    ax.set_ylabel(unit_axis_label(unit), fontsize=AXIS_LABEL_SIZE, color=COLORS["black"])
    ax.legend(frameon=True, facecolor="white", edgecolor="#e2e0e8", fontsize=LEGEND_SIZE, loc="upper right")
    style_axes(ax, grid_axis="y")
    return fig, ax


def main():
    csv_path = PROJECT_ROOT / "data/Science_Report_Data.csv"
    out_dir = PROJECT_ROOT / "graphs/science_report"
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

    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    df["indicator"] = df["indicator"].astype(str).str.strip()
    df["region"] = df["region"].map(clean_region)
    df["unit"] = df["unit"].map(clean_unit)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["indicator", "region", "unit", "year", "value"]).copy()

    for indicator, g in df.groupby("indicator", sort=True):
        g = g.copy()
        unit = g["unit"].iloc[0]
        years = sorted(g["year"].dropna().astype(int).unique())
        regions = sorted(g["region"].dropna().unique())

        if len(regions) == 1 and len(years) >= 2:
            fig, ax = plot_single_region_timeseries(g, unit, title_font)
        elif len(years) == 1:
            fig, ax = plot_single_year_multiregion(g, unit, title_font)
        else:
            fig, ax = plot_grouped_bars(g, unit, title_font)
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        plt.tight_layout()
        out_path = out_dir / f"{sanitize_filename(indicator)}.png"
        fig.savefig(out_path, dpi=220, transparent=True)
        plt.close(fig)
        print(f"Saved: {out_path}")

    # ── Extra graph: R&D Spending 2022 only ──
    rd = df[(df["indicator"] == "R&D Spending") & (df["year"] == 2022)].copy()
    if not rd.empty:
        unit = rd["unit"].iloc[0]
        fig, ax = plot_single_year_multiregion(rd, unit, title_font)
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        plt.tight_layout()
        out_path = out_dir / "r_d_spending_2022.png"
        fig.savefig(out_path, dpi=220, transparent=True)
        plt.close(fig)
        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
