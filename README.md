# Hewlett Geographic Grant Distribution Explorer

This project creates an interactive Streamlit application for visualizing the geographic distribution of grants in the Hewlett Foundation portfolio.

## Overview

The Streamlit app `app.py` allows users to upload grant data in CSV format and generates an interactive sunburst chart that visualizes the distribution of funds across different geographical entities. The chart is organized hierarchically, starting with US/International at the root, followed by regions, sub-regions, and countries.

## Requirements

- Python 3.x
- Required Python packages (see requirements.txt for specific versions):
  - streamlit
  - pandas
  - plotly
  - numpy
  - xlsxwriter

## Installation

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

Or install the main packages individually:

```bash
pip install streamlit pandas plotly numpy xlsxwriter
```

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. The app will open in your default web browser.
3. Upload your grant data CSV file using the file uploader in the sidebar.
   - The CSV should contain columns for "Geographical Area Served: Geographical Area Served Name", "Geographic Entity", "Request: Amount", and "Request: Reference Number".
4. The app will automatically process the data and display the interactive sunburst chart.

## Features

- **Interactive Visualization**: The Streamlit app provides an interactive sunburst chart that allows users to click on segments to drill down into specific geographic areas.
- **Hierarchical Structure**: The data is organized in a hierarchical structure (US/International → Region → Sub-region → Country/State).
- **Dynamic Filtering**: Clicking on chart segments automatically filters the data table and summary statistics.
- **Summary Statistics**: The app displays key metrics like total amount, average grant size, and number of geographic entities.
- **Detailed Data Table**: A filterable and sortable table shows all grants in the selected geographic area.
- **Quick Insights**: Automatically generated insights show top entities and program officers by grant amount.
- **Hover Information**: Hovering over segments displays detailed information including amount, number of grants, and percentage of total.

## Data Structure

The app processes the following columns from the uploaded CSV file:
- "Geographical Area Served: Geographical Area Served Name"
- "Geographic Entity"
- "Request: Amount"
- "Request: PO"
- "Request: Reference Number"

The app uses built-in UN M49 geographic classification data to automatically categorize countries and regions into a consistent hierarchy.

## Geographic Classification

The app uses a comprehensive geographic classification system:

- **US Data**: Organized by regions (South, Northeast, West, Midwest, Territories) and states
- **International Data**: Follows UN M49 standard with:
  - Regions (Africa, Americas, Asia, Europe, Oceania)
  - Sub-regions (e.g., Eastern Africa, Western Africa, Southern Asia)
  - Countries

## Getting Started

1. **Prepare Your Data**:
   - Create a report in the GMS of type: Geographical Areas Served with Request
   - Ensure it contains the required columns mentioned in the Data Structure section
   - Export the file as a CSV

2. **Run the App and Upload**:
   - Launch the app using the command in the Usage section
   - Upload your CSV file using the sidebar uploader
   - Explore the interactive visualization
