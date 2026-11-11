---
name: Sari-Sari Store Manager
description: A hand-painted neighborhood store front for three machine learning decisions
colors:
  signboard-yellow: "#ffc61a"
  enamel-red: "#c8202f"
  awning-green: "#0d6b3f"
  awning-green-deep: "#0a5030"
  shutter-blue: "#1b4fa0"
  sign-ink: "#17130f"
  enamel-white: "#fffdf2"
  pale-yellow: "#fff1b8"
typography:
  display:
    fontFamily: "Bowlby One, Impact, Arial Black, sans-serif"
    fontSize: "clamp(2.25rem, 6.4vw, 5rem)"
    fontWeight: 400
    lineHeight: 1.05
  headline:
    fontFamily: "Bowlby One, Impact, Arial Black, sans-serif"
    fontSize: "clamp(1.8rem, 4.4vw, 3.25rem)"
    fontWeight: 400
    lineHeight: 1.1
  body:
    fontFamily: "Barlow, sans-serif"
    fontSize: "18px"
    fontWeight: 400
  label:
    fontFamily: "Barlow, sans-serif"
    fontSize: "1rem"
    fontWeight: 700
rounded:
  sm: "4px"
  md: "8px"
components:
  button-primary:
    backgroundColor: "{colors.enamel-red}"
    textColor: "{colors.enamel-white}"
    rounded: "{rounded.sm}"
  tab-selected:
    backgroundColor: "{colors.signboard-yellow}"
    textColor: "{colors.sign-ink}"
    rounded: "{rounded.sm}"
  metric-tag:
    backgroundColor: "{colors.signboard-yellow}"
    textColor: "{colors.sign-ink}"
    rounded: "{rounded.sm}"
---

# Design System: Sari-Sari Store Manager

## Overview

**Creative North Star: "The Tindahan Front"**

The app is a neighborhood store seen from the street: a painted yellow sign, a strip of window mesh, a green band of tabs, and a clean enamel wall below. Each tab opens with the store owner's question painted large, and the algorithm comes second.

**Key Characteristics:**
- Flat, saturated enamel color in whole regions
- Poster lettering for store questions and key numbers
- Plain, highly legible Barlow for everything being read

## Colors

Four painted colors over one enamel wall, each with one job.

### Primary
- **Signboard Yellow**: the sign, selected tab, metric tags, and the price card.
- **Enamel Red**: the store name, primary buttons, and the sales question.

### Secondary
- **Awning Green**: the tab band and the product groups question.
- **Shutter Blue**: the restock question.

### Neutral
- **Sign Ink**: text, keylines, and the home question.
- **Enamel White**: the page wall.
- **Pale Yellow**: inputs, table headers, and notices.

**The One Job Rule.** Each tab owns one painted color for its question. Chart series use only red, blue, and green, in that order.

## Typography

**Display Font:** Bowlby One (with Impact, Arial Black)
**Body Font:** Barlow (with sans-serif)

**Character:** Heavy poster letters from a painted sign, paired with a plain workhorse inspired by road signage.

### Hierarchy
- **Display**: the store name only.
- **Headline**: the store question on each tab, and section headings at smaller sizes.
- **Body**: paragraphs, capped near 75 characters per line.
- **Label**: tabs, metric labels, and expander titles.

**The Reading Rule.** Bowlby One is for what is glanced at, never for what is read at length.

## Layout

A centered column up to 1180px on the enamel wall. The sign, mesh, and tab band run the full window width. Streamlit columns stack at phone width, and the sign and question type scale with the window.

## Elevation & Depth

Flat. Depth comes from color regions and the painted drop shadow on the store name. Components carry no box shadows.

## Shapes

Gently rounded corners: 4px on controls and tags, 8px on the sign, question panels, and price card. The sign has an inset ink keyline.

## Components

### Buttons
- **Primary:** enamel red with white bold text, using Streamlit's own hover and focus states.

### Navigation
- **Tabs:** bold enamel text on the green band. The selected tab is signboard yellow with ink text, hover is a deeper green, and keyboard focus is a yellow ring.

### Store Question
- A full-width painted panel holding the owner's question and one line naming the ML paradigm.

### Price Card
- The predicted sales figure in red poster type on a yellow card, hung at a slight tilt. It drops in once and stays still when reduced motion is requested.

## Do's and Don'ts

### Do:
- **Do** open every tab with the store owner's question.
- **Do** keep styling in `style.css` and `.streamlit/config.toml`, away from the ML code.

### Don't:
- **Don't** add chart libraries. Charts stay Streamlit built-ins.
- **Don't** imply real customers or deployments. The data is synthetic.
