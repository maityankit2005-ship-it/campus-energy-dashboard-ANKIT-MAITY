# Campus Energy Dashboard (Python Capstone Project)

This project analyzes electricity usage across campus buildings using Python.  
It performs full data ingestion, validation, aggregation, visualization, and reporting.  
This repository contains the complete pipeline solution for the "Programming for Problem Solving using Python" capstone assignment.

---

##  Project Structure

campus-energy-dashboard/
│
├── campus_energy_dashboard.py # main script
│
├── data/ # input CSV files (your monthly building data)
│ ├── BuildingA_2023-01.csv
│ ├── BuildingB_2023-01.csv
│ └── ...
│
├── output/ # generated outputs
│ ├── cleaned_energy_data.csv
│ ├── building_summary.csv
│ ├── summary.txt
│ ├── dashboard.png
│ └── ...
│
└── logs/
└── ingestion.log # log of read/skip/error messages


---

##  Assignment Summary

This project solves a real-world energy monitoring problem:  
*The university wants insights about electricity usage across buildings to reduce wastage and improve efficiency.*

The script:

1. Reads CSV files for each building
2. Cleans and validates the data
3. Calculates daily & weekly consumption
4. Builds building-level summaries
5. Creates a multi-chart dashboard
6. Exports final CSV and summary report

---

##  Tasks Completed

### **Task 1 — Data Ingestion & Validation**
- Automatically detects all `.csv` files in `/data`
- Cleans column names and handles:
  - missing timestamps
  - corrupt rows
  - numeric conversion errors
- Adds building name from filename
- Logs all issues to `logs/ingestion.log`

### **Task 2 — Aggregation Logic**
- Calculates:
  - Daily totals per building
  - Weekly aggregates
- Generates building summary table showing:
  - mean
  - min
  - max
  - total kWh

### **Task 3 — OOP Modeling**
(Instructor version: optional / simplified)
- Classes included:
  - `Building`
  - `MeterReading`
  - `BuildingManager`
- Converts raw readings into objects for structured analysis

### **Task 4 — Visualization Dashboard**
Creates a final image `dashboard.png` showing:
1. Daily consumption trend line  
2. Weekly total bar chart  
3. Hourly scatter plot  

### **Task 5 — Summary & Persistence**
Exports:
- `cleaned_energy_data.csv`
- `building_summary.csv`
- `summary.txt` (executive summary)

---

##  Input Data Format

Every CSV file in `/data` should contain at least:

timestamp,kwh
2023-01-01 00:00,10
2023-01-01 01:00,12


File names should follow this pattern:
<BuildingName>_<Month>.csv


Example:
Library_2023-01.csv
HostelA_2023-01.csv


---

##  Running the Project

### **1. Place CSV files in the `/data` folder**
Example:

data/
├── AdminBlock_2023-01.csv
├── Library_2023-01.csv
└── HostelA_2023-01.csv


### **2. Run the script**

Open terminal in VS Code:
python campus_energy_dashboard.py


### **3. Check Outputs**

Generated files appear automatically in:
output/
cleaned_energy_data.csv
building_summary.csv
summary.txt
dashboard.png


---

##  Sample Report (summary.txt)

TOTAL CONSUMPTION: 12540 kWh
HIGHEST BUILDING: Library
Peak Load Time: 2023-01-16 18:00


---

##  Requirements

Install dependencies (only if needed):

py -m pip install pandas numpy matplotlib
