# Presentation Style Guide

## Theme
- **Light theme** (Reveal.js `white.css`)

## Typography

### Fonts
- **Titles (h1, h2, h3):** Playfair Display (serif)
- **Body text:** Plus Jakarta Sans (sans-serif)

### Font imports
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Yellow | #FEDF9E | Mission/Goal boxes |
| Red | #F47D5B | Problems boxes |
| Purple | #A09AC8 | Outcomes boxes |
| Green | #B4DBA2 | Interventions parent box |
| Grey/White | #F6F5F9 | Faded elements, leaf node fills |
| Black | #0E0705 | Text on colored backgrounds |
| Teal | #A2E1FF | Available for additional elements |
| Blue | #8098FF | "Why Europe" boxes |
| Pink | #FFB6BB | Available for additional elements |

## Color Variants (Darker Strokes)

Each main color has a darker variant used for strokes to provide better definition:

| Color | Fill | Stroke |
|-------|------|--------|
| Blue | #8098FF | #4a6ed4 |
| Red | #F47D5B | #c45a3d |
| Green (parent) | #B4DBA2 | #7cb668 |
| Green (sub-boxes T1/T2/T3) | #7cb668 | #5a9a4a |
| Purple | #A09AC8 | #7a72a8 |
| Yellow | #FEDF9E | #d4b870 |

## Mermaid Diagram Styling

### Box Hierarchy

1. **Parent containers** (WHY, PROB, INT, OUT): Main color fill with darker stroke
2. **Sub-containers** (T1, T2, T3 within Interventions): Darker green (#7cb668) fill with even darker stroke (#5a9a4a)
3. **Leaf-level nodes** (WE1-WE5, P1-P5, I1-I6, O1-O4): Light grey (#F6F5F9) fill with colored border matching parent

### Example Mermaid Styles
```
%% Parent containers
style WHY fill:#8098FF,stroke:#4a6ed4,color:#0E0705
style PROB fill:#F47D5B,stroke:#c45a3d,color:#0E0705
style INT fill:#B4DBA2,stroke:#7cb668,color:#0E0705
style OUT fill:#A09AC8,stroke:#7a72a8,color:#0E0705
style M fill:#FEDF9E,stroke:#d4b870,color:#0E0705

%% Sub-containers (within Interventions)
style T1 fill:#7cb668,stroke:#5a9a4a,color:#0E0705
style T2 fill:#7cb668,stroke:#5a9a4a,color:#0E0705
style T3 fill:#7cb668,stroke:#5a9a4a,color:#0E0705

%% Leaf nodes - grey fill with parent-colored border
style WE1 fill:#F6F5F9,stroke:#4a6ed4,color:#0E0705
style P1 fill:#F6F5F9,stroke:#c45a3d,color:#0E0705
style I1 fill:#F6F5F9,stroke:#5a9a4a,color:#0E0705
style O1 fill:#F6F5F9,stroke:#7a72a8,color:#0E0705
```

### Faded Elements (for audience highlight slides)
```
fill:#F6F5F9,stroke:#d1d5db,color:#9ca3af
```

## Node Text Labels (Comprehensive)

Always use the full, comprehensive text for all nodes:

### Why Europe (WE)
- WE1: "EU+US > US alone"
- WE2: "Third pole"
- WE3: "Democratic legitimacy"
- WE4: "Most to lose"
- WE5: "Safety culture"

### Problems (P)
- P1: "Europe weak"
- P2: "Getting weaker"
- P3: "AGI outpaces"
- P4: "Safety gaps"
- P5: "Racing"

### Intervention Themes (T)
- T1: "Geopolitics & Frontier AI"
- T2: "Adoption & the State"
- T3: "Safety & Resilience R&D"

### Interventions (I)
- I1: "EU Frontier AI"
- I2: "Fast-follow"
- I3: "State capacity"
- I4: "d/acc solutions"
- I5: "New scaling paradigms"
- I6: "AGI Geopolitics"

### Outcomes (O)
- O1: "Strong Europe"
- O2: "EU values in AGI"
- O3: "Geopolitical stability"
- O4: "Risk-free AGI"

### Mission (M)
- M: "Navigate AGI Transition"

## CSS Variables

```css
:root {
    --blue: #8098FF;
    --blue-dark: #4a6ed4;
    --red: #F47D5B;
    --red-dark: #c45a3d;
    --green: #B4DBA2;
    --green-dark: #7cb668;
    --green-darker: #5a9a4a;
    --purple: #A09AC8;
    --purple-dark: #7a72a8;
    --yellow: #FEDF9E;
    --yellow-dark: #d4b870;
    --grey: #F6F5F9;
    --black: #0E0705;
    --teal: #A2E1FF;
    --teal-dark: #6bc4e8;
    --pink: #FFB6BB;
}
```

## Audience Badge Colors

```css
.badge-progress { background: #8098FF; color: #0E0705; }
.badge-safety { background: #F47D5B; color: #0E0705; }
.badge-compete { background: #B4DBA2; color: #0E0705; }
.badge-dacc { background: #A09AC8; color: #0E0705; }
```
