# GEG Active Portfolio Sunburst Chart

This project creates a sunburst chart visualization of the GEG (Global Engagement Group) active portfolio based on geographical hierarchies and monetary amounts.

## Overview

The script `sunburst_chart.py` reads data from `geg_active_portfolio.csv` and generates an interactive sunburst chart that visualizes the distribution of funds across different geographical entities. The chart is organized hierarchically, starting with US/International at the root, then continent, region, and country levels.

## Requirements

- Python 3.x
- Required Python packages:
  - pandas
  - plotly
  - numpy

## Installation

Install the required packages using pip:

```bash
pip install pandas plotly numpy
```

## Usage

1. Ensure that `geg_active_portfolio.csv` is in the same directory as the script.
2. Run the script:

```bash
python sunburst_chart.py
```

3. The script will generate an HTML file named `geg_portfolio_sunburst.html` in the same directory.
4. Open the HTML file in a web browser to view the interactive sunburst chart.

## Features

- **Interactive Visualization**: The sunburst chart allows for interactive exploration of the data.
- **Hierarchical Structure**: The data is organized in a hierarchical structure (US/International → Continent → Region → Country).
- **Color Coding**: The chart uses color coding to represent the monetary amounts.
- **Hover Information**: Hovering over segments displays detailed information about the geographical entity and the corresponding amount.

## Data Structure

The script processes the following columns from the CSV file:
- "Geographical Area Served: Geographical Area Served Name" (geo_id)
- "Geographic Entity" (geographic_entity)
- "Request: Amount" (amount)
- "Request: PO" (po)
- "Request: Reference Number" (reference_number)

## Customization

You can customize the chart by modifying the following parameters in the script:
- Color scale: Change `color_continuous_scale='RdBu'` to use a different color palette.
- Title: Modify the `title` parameter in the `px.sunburst()` function.
- Layout: Adjust the `fig.update_layout()` parameters to change margins, colorbar, etc.