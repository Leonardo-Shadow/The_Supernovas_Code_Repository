# The_Supernovas_Code_Repository
Mars EVA tactical navigation system featuring an interactive map, Supabase spatial integration, and a Python-powered machine learning pipeline for surface telemetry and survival routing.

# MARS-NAV: EVA Tactical Navigation & Survival HUD

Team: The Supernovas Code

Sector: Aeolis-Elysium (MC-23) — Gale Crater & Surroundings

## Project Overview
MARS-NAV is an interactive Martian surface exploration and astronaut survival telemetry system designed for Extravehicular Activity (EVA) missions. It bridges spatial database management (Supabase) with a modular Python Machine Learning pipeline and routing algorithms, delivering real-time environmental forecasts, radiation risk assessments, and optimal navigation strategies for astronauts.

## Repository Structure & Detailed File Descriptions
- csv/: Directory containing Martian geospatial and meteorological datasets (such as dataset_marte_ml.csv). These files serve as the historical source of truth containing coordinates, elevations, and baseline metrics to power the predictive models and routing scripts.

- modelo.py (Module 3 - Machine Learning): Script responsible for analytical processing and predictive modeling. It implements a Polynomial Regression pipeline using Scikit-Learn (PolynomialFeatures and LinearRegression). Its main purpose is to process geographical coordinates and zone altitudes to accurately forecast estimated surface temperature ($^\circ\text{C}$) and radiation exposure levels ($\text{mSv/day}$).

- rutas.py (Module 4 - Tactical Routing & Survival): Algorithmic module focused on astronaut safety and rover mobility. It cross-evaluates terrain slope, critical radiation thresholds, and calculated operational risk to generate tailored survival protocols and suggest optimal travel routes that avoid geological hazards (such as deep sand dunes).

- generar_json.py: Automation script and data bridge. It iteratively traverses the dataset inside the csv/ folder, invokes the analytical functions from modelo.py and rutas.py for each Point of Interest (POI), and consolidates all results into a structured file (predicciones.json) ready to be consumed by the presentation layer.

- predicciones.json: Automatically generated intermediate data file. It contains calculated telemetry, risk levels, and survival strategies organized by region identifier, serving as a structured backup of the Machine Learning engine.

- generar_mapa.py (Static Frontend Compiler): Master compilation script. It executes the scientific Python modules, takes the generated prediction dictionary, and statically embeds it directly inside the tactical HUD web template. As a result, it generates the final index_generado.html file, guaranteeing zero-latency performance and completely eliminating browser CORS security blocks.

- index_generado.html (Module 5 - Tactical HUD Interface): The definitive interactive cartographic web application developed with Leaflet. It connects via the official SDK to Supabase to render real-time high-resolution Martian base maps and rover reconnaissance photographs. Clicking on any solar beacon on the map dynamically displays the environmental telemetry processed by the Machine Learning model and tactical survival routes on the side panel.

## Requirements & Imports
Before running the Python pipeline, ensure you have Python 3.9+ installed along with the required scientific and data-processing libraries.

### Python Imports & Dependencies:

The backend scripts rely on the following core modules:

- pandas & numpy (Tabular data manipulation and CSV ingestion)

- scikit-learn (PolynomialFeatures, LinearRegression for training and forecasting the predictive model)

- json & os (Standard library modules for data serialization and system file handling)

Install all dependencies by running in your terminal:

pip install pandas numpy scikit-learn

(Note: Ensure all .py files remain in the root directory alongside the csv/ folder so internal module imports—such as from modelo import ... and from rutas import ...—resolve properly without path errors).

## Workflow & Data Update Pipeline

This project uses a static compilation architecture to guarantee zero-latency performance and eliminate CORS security restrictions in the browser during live demonstrations.

### Important Note on Data Updates:

Whenever the source dataset inside the csv/ folder is modified or expanded with new Martian coordinates, you must execute the Python scripts sequentially to retrain the models and recompile the web interface:

- Step 1 — Validate ML & Routing Logic (Optional standalone test):
  
      - python modelo.py
      - python rutas.py
- Step 2 — Regenerate the JSON Telemetry Bridge:
  
      - python generar_json.py
(Updates predicciones.json with the latest ML and survival calculations).

Step 3 — Compile the Final Tactical Web Application:

      - python generar_mapa.py
(Rebuilds index_generado.html with the newly computed predictions embedded directly into the code).

## How to View the Application

Once the index_generado.html file has been generated:

1- Simply double-click index_generado.html to open it in any modern web browser (Chrome, Edge, Firefox). (An active internet connection is required to load Martian base maps and rover photography from Supabase storage).

2- Click on any pulsing solar beacon on the map to inspect the geological region, temperature and radiation metrics predicted by the Machine Learning model, the operational risk indicator, and the tactical EVA route strategy.
