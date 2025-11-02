import streamlit as st
import pandas as pd
import plotly.express as px  # <-- NEW: Import Plotly
import os
import sys

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Danish Green Grid Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. Data Loading ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_ROOT, 'data', 'processed_data.csv')

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data(filepath):
    """
    Loads the processed data from the CSV file.
    """
    try:
        df = pd.read_csv(filepath)
        df['HourDK'] = pd.to_datetime(df['HourDK'])
        return df.sort_values(by='HourDK', ascending=True) # Ensure data is sorted
    except FileNotFoundError:
        st.error(
            f"ERROR: Data file not found at {filepath}\n"
            "Please run the data processing scripts first:\n"
            "1. `python src/task_1_fetch_data.py`\n"
            "2. `python src/task_2_and_3_process_data.py`"
        )
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        st.stop()

# --- 3. Main Application ---
st.title("🌿 Danish Green Grid Dashboard")
st.markdown("""
    This dashboard shows the real-time and forecasted carbon intensity (CO2-equivalent) 
    of the Danish electricity grid. Use this to find the greenest time to use energy!
""")

# Load the data
df_processed = load_data(DATA_FILE)


# --- Task 5: Current Grid Status ---
# (This section is from the previous step)

st.header("Current Grid Status")

def get_recommendation_and_color(score):
    """Provides a simple recommendation based on the Eco-Score."""
    if score <= 75:
        return ("✅ **Excellent!** A great time for high-load tasks.", "success")
    elif score <= 150:
        return ("👍 **Good.** A reasonable time to use energy.", "info")
    else:
        return ("⚠️ **High.** Consider waiting for a greener time if you can.", "warning")

col1, col2 = st.columns(2)

try:
    with col1:
        df_dk1 = df_processed[df_processed['PriceArea'] == 'DK1']
        latest_dk1 = df_dk1.iloc[-1]
        prev_dk1 = df_dk1.iloc[-2]
        delta_dk1 = latest_dk1['gCO2e_per_kWh'] - prev_dk1['gCO2e_per_kWh']
        
        st.metric(
            label=f"DK1 (West) Eco-Score",
            value=f"{latest_dk1['gCO2e_per_kWh']:.1f} gCO2e/kWh",
            delta=f"{delta_dk1:.1f} g vs. prev. hour",
            delta_color="inverse"
        )
        message, alert_type = get_recommendation_and_color(latest_dk1['gCO2e_per_kWh'])
        getattr(st, alert_type)(message) # Call st.success, st.info, or st.warning
        st.caption(f"Last update: {latest_dk1['HourDK'].strftime('%B %d, %H:%M')}")

    with col2:
        df_dk2 = df_processed[df_processed['PriceArea'] == 'DK2']
        latest_dk2 = df_dk2.iloc[-1]
        prev_dk2 = df_dk2.iloc[-2]
        delta_dk2 = latest_dk2['gCO2e_per_kWh'] - prev_dk2['gCO2e_per_kWh']
        
        st.metric(
            label=f"DK2 (East) Eco-Score",
            value=f"{latest_dk2['gCO2e_per_kWh']:.1f} gCO2e/kWh",
            delta=f"{delta_dk2:.1f} g vs. prev. hour",
            delta_color="inverse"
        )
        message, alert_type = get_recommendation_and_color(latest_dk2['gCO2e_per_kWh'])
        getattr(st, alert_type)(message) # Call st.success, st.info, or st.warning
        st.caption(f"Last update: {latest_dk2['HourDK'].strftime('%B %d, %H:%M')}")

except IndexError:
    st.error("Not enough data to display current status. Please ensure you have at least 2 hours of data.")
except Exception as e:
    st.error(f"An error occurred while creating metrics: {e}")

st.divider()

# --- END: Task 5 ---


# --- NEW: Task 6 Starts Here ---

st.header("Historical Eco-Score (Last 48 Hours)")

try:
    # --- CHANGE HERE ---
    # Create the Plotly line chart, using 'ProductionType' for color
    fig = px.line(
        df_processed,
        x='HourDK',
        y='gCO2e_per_kWh',
        color='ProductionType',  # <-- THIS IS THE FIX
        facet_row='PriceArea',   # <-- This splits DK1 and DK2 into separate charts
        title="Carbon Intensity (gCO2e/kWh) by Fuel Type",
        labels={
            "gCO2e_per_kWh": "Eco-Score (g CO2e / kWh)",
            "HourDK": "Date & Time",
            "ProductionType": "Fuel Type"
        },
        template="plotly_white"
    )

    # Improve hover data
    fig.update_traces(
        hovertemplate="<b>%{data.name}</b><br>%{x|%B %d, %H:%M}<br>Eco-Score: %{y:.1f} gCO2e/kWh<extra></extra>"
    )
    
    # Update layout to make it cleaner
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Eco-Score (gCO2e/kWh)"
    )
    
    # Adjust facet labels
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # Display the chart in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"An error occurred while creating the historical chart: {e}")

# --- END: Task 6 ---


# --- 4. Sidebar ---
st.sidebar.title("Filters")
st.sidebar.markdown("Filters and controls will go here.")