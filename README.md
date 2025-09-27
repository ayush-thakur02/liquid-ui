# Liquid UI

Liquid UI is a lightweight, modular Python framework for building interactive web user interfaces. It encapsulates best practices around component-driven development, state management, and flexible template rendering to accelerate the creation of UI prototypes and dashboards. With a plug-and-play folder structure, a range of built-in components, and demo scripts, Liquid UI helps you focus on crafting beautiful, responsive interfaces without boilerplate overhead.

***

## Table of Contents

- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [Directory Structure](#directory-structure)
- [Component Library](#component-library)
- [Demo Scripts](#demo-scripts)
- [State Management](#state-management)
- [Static Assets & Templates](#static-assets--templates)
- [Getting Started](#getting-started)
- [Benefits](#benefits)
- [License](#license)

***

## Key Features

- **Python-First UI Building**: Write UI logic and components in pure Python.
- **Component System**: Buttons, checkboxes, sliders, file/image uploads, text input, radios, and more.
- **Stateful UI**: Persistent state across interactions and demos.
- **Grid Layout Utility**: Compose complex layouts easily with the `grid_layout` utility.
- **Demo-Driven**: Ready-to-run demos for all components.
- **Extensible Templates**: Powerful templating with Jinja2/HTML templates.
- **Modern CSS & SVG Assets**: Sleek style and icons for your UI elements.

***

## Architecture Overview

**Liquid UI** is composed of several modular sub-systems:

| Layer            | Responsibility                                                                |
|------------------|-------------------------------------------------------------------------------|
| `framework.py`   | The core application logic: UI runtime, routing, integration of components    |
| `utils/`         | Utilities: includes grid_layout for flexible GUI layout, and state_manager    |
| `demos/`         | Example scripts demonstrating component use-cases and page composition        |
| `static/`        | Static files: CSS for styling and SVG for icons                              |
| `templates/`     | Jinja2-compatible HTML templates for UI rendering                            |
| `state/`         | Support code for state preservation across UI interactions                    |
| `images/`        | Image assets for UI/image component demos                                    |

**Component flow:**
- The core framework registers available UI components from `utils/components/`.
- State is tracked by the global state manager, allowing multi-page or component-level persistence.
- UI layout is orchestrated via utility functions, chiefly the grid layout manager.
- Static CSS and HTML templates maintain appearance consistency, while SVG icons give the UI a modern polish.
- Demo scripts (`demos/`) show usage, wiring, and UI-flow patterns.

***

## Directory Structure

```
liquid-ui/
├── demos/           # Demo/example Python scripts for each main component
├── images/          # Sample images and UI assets
├── state/           # State management and persistence modules
├── static/          # Static frontend assets: CSS and SVG icons
├── templates/       # HTML (Jinja2) templates for UI rendering
├── utils/           # Utilities: layout, state manager, core components
│   └── components/  # Library of reusable UI components
├── framework.py     # Framework core logic
└── README.md
```

***

## Component Library

Liquid UI supports these reusable, extensible UI components:

- **Button**
- **Checkbox**
- **File Upload**
- **Image**
- **Input Box**
- **Radio Button**
- **Slider**
- **Text Display**

All components are maintained in `utils/components/`. Each comes with a dedicated demo script to help you understand usage and customization.

***

## Demo Scripts

Find example usage of each component and UI pattern in `demos/`. Notable demos:

- `all-demo.py` (Showcase of all base components)
- `calculator.py` (Functional calculator UI)
- `checkbox-demo.py`, `slider-demo.py`, `file-demo.py`, etc. (Feature-specific UIs)
- `state-preservation-demo.py` (Persistent state demonstration)[1][2]

Run demo scripts as standalone apps to experiment or adapt for your needs.

***

## State Management

Global and local UI state is handled by the `state_manager.py` utility. This enables:

- Retaining user input between page loads or UI updates
- Building multi-step forms or wizards
- Demoing session-persistent elements

***

## Static Assets & Templates

- `static/styles.css`: Handles all core styling for fast, visually coherent UIs.
- `static/icon.svg`: Unified icon used in layouts and as brand/UI marker.
- `templates/`: Base and index HTML templates, easily extendable for custom UI layouts.

***

## Getting Started

1. **Clone the repo**

    ```bash
    git clone https://github.com/ayush-thakur02/liquid-ui.git
    cd liquid-ui
    ```

2. **Explore demos**

    ```bash
    python demos/all-demo.py
    # or
    python demos/slider-demo.py
    ```

3. **Customize for your project**
    - Extend components in `utils/components/`, plug in new layouts or templates, and style via `static/styles.css`.

***

## Benefits

- **Rapid UI Prototyping**: Ready-to-use demos accelerate the prototype cycle.
- **Minimal Boilerplate**: Structured, pre-wired templates and assets let you focus on your app, not setup.
- **Reusable Patterns**: Components, layout, and state logic are modular and extensible.
- **Developer Friendly**: Pythonic code, clear folder organization, and plenty of demo examples.
- **Customizable**: Easily adapt themes, layouts, and components for your specific needs.
