# “Structural inequality shapes the daily rhythm of stationarity and mobility” Analysis and Visualization

## Overview

This repository contains the complete computational framework for analyzing anonymized population mobility patterns and their relationships with demographic, socioeconomic, and built environment characteristics. The code supports community-scale and temporal analysis with comprehensive data visualization capabilities.

## Environment Setup & Requirements

To ensure reproducibility and make it easy to set up the correct development/testing environment, please follow the instructions below. 

The code was developed and tested on **Python 3.9**.

1. Clone this repository:
   ```bash
   git clone https://github.com/zc16423/stationarity_mobility_rhythm_analysis.git
   cd stationarity_mobility_rhythm_analysis
   ```

2. Install the required dependencies using the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Key Features

- **Multi-scale Analysis:** Community-level and daily temporal pattern analysis  
- **Demographic Integration:** Population mobility patterns by racial/ethnic composition
- **Dynamic Modeling:** Time-series fitting and kinetic analysis of mobility data  
- **Visualization:** Publication-ready figures and statistical plots  

## Repository Structure

├── README.md

├── LICENSE

├── requirements.txt

├── sample_data.csv

├── econometrics_data.csv

├── data_description.txt

├── figure_data/

│ ├── Figure1/

│ ├── Figure2/

│ ├── Figure3/

│ ├── Figure4/

├── data_processing/

│ ├── device_permeability_weight_calculation.py

│ ├── hourly_mobility_ratio_calculation.py

│ ├── single_cbg_racial_information_matching.py

│ ├── dynamic_rhythm_fitting.py

│ ├── weekend_and_holiday_date_identification.py

│ ├── ols_regression_temporal_dispersion.py

├── visualization/

│ ├── Figure1/

│ ├── Figure2/

│ ├── Figure3/

│ ├── Figure4/

## Data Sources

1. **Demographic Data:** US Census Bureau American Community Survey (ACS) 2015-2019  
   - Racial/ethnic composition by Census Block Group  
   - Educational attainment and employment statistics  
   - Housing characteristics and ownership rates  

2. **Built Environment:** US EPA Smart Location Database (SLD v3)  
   - Walkability indices and employment accessibility  
   - Low-wage employment distribution  

3. **Mobility Data:** Social Distancing Metrics  
   - Hourly home-dwelling device ratios  
   - Aggregated to Census Block Group level  

## Key Methodologies

### Demographic Classification

- **Threshold-based Classification:** Communities classified by majority demographic (≥50%)  
- **Multi-ethnic Analysis:** Separate analysis for White, Hispanic, and Black American communities  
- **Adjustable Parameters:** Threshold values can be modified in processing scripts  

### Temporal Analysis

- **Workday Identification:** Excludes weekends and federal holidays  
- **Federal Holidays:** New Year's Day, MLK Day, Presidents' Day, Memorial Day, Independence Day, Labor Day, Columbus Day, Veterans Day, Thanksgiving, Christmas  
- **Hourly Resolution:** Analysis of home-dwelling device ratios at hourly intervals  

### Dynamic Modeling

- **Community-scale Fitting:** Individual community temporal pattern analysis  
- **Daily-scale Fitting:** Cross-community daily pattern analysis  
- **Kinetic Modeling:** Mathematical modeling of mobility dynamics  
