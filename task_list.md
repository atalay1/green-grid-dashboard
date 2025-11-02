📋 Green Grid Dashboard: Project Tasks
Epic 1: Data Pipeline & Processing

- Task 1: Research API and build initial fetch script

     Description: Read the Energi Data Service docs for DeclarationProduction. Write a requests script to fetch the last 48 hours of data for DK1 and DK2 and save the raw JSON output.

[ ] Task 2: Create data cleaning and processing script

Description: Use pandas to load the raw JSON. Handle missing values, convert HourUTC to a datetime object, and create a HourDK column (CET/CEST time zone).

[ ] Task 3: Engineer the "CO2-equivalent" (CO2e) Eco-Score

Description: Create a new gCO2e_per_kWh column by calculating the CO2-equivalent using the GWP100 factors: gCO2e_per_kWh = CO2_g_kWh + (CH4_g_kWh * 28) + (N2O_g_kWh * 265). Save this final, clean DataFrame.

Epic 2: Dashboard (MVP)

[ ] Task 4: Setup Streamlit App

Description: Create app.py. Set up the basic streamlit page configuration (title, layout) and a function to load the clean data (using @st.cache_data).

[ ] Task 5: Build "Current Status" View

Description: Get the most recent data row. Use st.columns and st.metric to display the current gCO2e_per_kWh for DK1 and DK2. Add a simple conditional "green/red" text recommendation.

[ ] Task 6: Build Historical Chart

Description: Use plotly.express to create an interactive line chart of the gCO2e_per_kWh over the last 48 hours, using color to separate DK1 and DK2. Display it in the app.

Epic 3: Machine Learning - Forecasting

[ ] Task 7: Time-Series Feature Engineering

Description: Create a script/notebook to load the historical data. Extract features from the timestamp like hour_of_day, day_of_week, month, and lag features (e.g., lag_1hr, lag_24hr, rolling_avg_3hr).

[ ] Task 8: Train and Save Forecasting Model

Description: Split data into train/test sets. Train a regression model (RandomForestRegressor, XGBoost, etc.) to predict gCO2e_per_kWh. Evaluate with MAE and save the final model as a .joblib file.

[ ] Task 9: Integrate Forecast into App

Description: Load the saved .joblib model in app.py (using @st.cache_resource). Write a function to generate features for the next 24 hours, make predictions, and display them on a Plotly chart (e.g., as a dashed line).

Epic 4: Deployment & Documentation

[ ] Task 10: Deploy App to Streamlit Cloud

Description: Create a requirements.txt file (or use the environment.yml if deploying via Docker). Push the project to a GitHub repository and deploy it on Streamlit Cloud so it's publicly accessible.

[ ] Task 11: Write Project README

Description: Create a high-quality README.md file for the GitHub repo. Include a project summary, a link to the live app, a screenshot, technical stack, and "How to Run Locally" instructions.