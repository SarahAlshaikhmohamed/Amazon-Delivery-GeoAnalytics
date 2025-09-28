import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import joblib

# Set page configuration
st.set_page_config(
    page_title="Amazon Delivery Analytics Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
# 🎨 Bright Theme with Orange Sidebar
st.markdown("""
<style>
    /* General page */
    body {
        background-color: #fefefe; /* Brighter white background */
        font-family: "Segoe UI", sans-serif;
        color: #2c3e50;
    }

    /* Main headers */
    .main-header {
        font-size: 2.8rem; 
        color: #ff9900; /* Amazon Orange */
        font-weight: bold; 
        margin-bottom: 1rem;
    }

    /* Sub headers */
    .sub-header {
        font-size: 1.6rem; 
        color: #1f77b4; 
        border-bottom: 2px solid #eee; 
        padding-bottom: 0.4rem;
        margin-top: 1.5rem;
        font-weight: 600;
    }

    /* Cards for metrics/info */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f9fcff); 
        padding: 1.2rem; 
        border-radius: 1rem; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
    }
    .metric-card h3 {
        font-size: 1.1rem;
        color: #34495e;
        margin-bottom: 0.3rem;
    }
    .metric-card p {
        font-size: 1.6rem;
        font-weight: bold;
        color: #27ae60; /* Amazon green */
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        padding: 1.2rem;
        min-width: 300px;
        max-width: 300px;
        font-size: 14px;
        color: white;
    }
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Dataset description box */
    .dataset-description {
        background: #f9fbfd; 
        padding: 1rem; 
        border-radius: 0.7rem; 
        margin-bottom: 1.5rem;
        font-size: 1rem;
        color: #2c3e50;
        border-left: 4px solid #1f77b4;
    }

    /* Highlighted features box */
    .features {
        border: solid 1px #ff9900; 
        border-radius: 10px; 
        text-align: center; 
        font-size: 13px; 
        color: #ff9900; 
        padding: 10px; 
        margin-bottom: 20px;
        background-color: #fff8ef;
        font-weight: 500;
    }

    /* Buttons */
    .stButton>button {
        background-color: #27ae60; /* Amazon green */
        color: white; 
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #219150;
        transform: translateY(-2px);
    }

</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">📦 Amazon Delivery Geo-Analytics</h1>', unsafe_allow_html=True)

# Function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("..\Dataset\Clean_amazon_delivery.csv")
        
        return df
    except:
        st.error("Dataset not found. Please place 'Analytics/Clean_amazon_delivery.csv' in the same folder.")
        return pd.DataFrame()
        
# Load data
data = load_data()

# Sidebar for dataset describtion and filters and information
with st.sidebar:
    st.image("delivery-man_5637272.png", width=100)
    filters_tab, about_tab = st.tabs(["Filters", "About",])

    # Sidebar filters
    with filters_tab:  
        
        # Area filter
        Area= st.sidebar.multiselect(
            "Select Areas:",
            options=data['Area'].unique(),
            default=data['Area'].unique()
        )
        
        # Vehicle filter
        Vehicle= st.sidebar.multiselect(
            "Select Vehicles:",
            options=data['Vehicle'].unique(),
            default=data['Vehicle'].unique()
        )
    
        
        # Delivery time filter
        min_time, max_time = st.sidebar.slider(
            "Delivery Time Range (minutes):",
            min_value=int(data['Delivery_Time'].min()),
            max_value=int(data['Delivery_Time'].max()),
            value=(int(data['Delivery_Time'].min()), int(data['Delivery_Time'].max()))
        )
    
            # Apply filters
        filtered_df = data[
            (data['Area'].isin(Area)) &
            (data['Vehicle'].isin(Vehicle)) &
            (data['Delivery_Time'] >= min_time) &
            (data['Delivery_Time'] <= max_time)
        ]
    
    with about_tab:
            st.markdown("""
                <div style="font-size:13px; line-height:1.6; text-align:justify;">
        <h3>About the Dataset</h3>
        <p>The Amazon Delivery Dataset offers a comprehensive look at the company's last-mile logistics, with over 43,600 deliveries. It contains detailed data on orders, delivery agents, weather, traffic, and performance metrics. This allows researchers to analyze factors that influence delivery efficiency and customer experience and identify areas for optimization.</p>

        ### Analytics Objectives
         - Analyze delivery geo-data to uncover trends and patterns.  
         - Identify key factors influencing delivery time.  
         - Create an interactive dashboard for GeoAnlytics data visualization.   
         - **Outlier Detection:** Spotting unusual patterns or anomalies.  

        

        ### Data Source 
          Kaggle - [Amazon Delivery Dataset](https://www.kaggle.com/datasets/minahilfatima12328/car-sales-info/data")
                </div>
            """, unsafe_allow_html=True) 

            #main page 
            # data overview section
tab1, tab2, tab3 = st.tabs(["📊 Dataset Overview", "🗺️ Maps Overview", "📈 Prediction"])


with tab1:
    st.header("Dataset Overview")
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", f"{len(data):,}")
    
    with col2:
        avg_time = data['Delivery_Time'].mean()
        st.metric("Avg Delivery Time", f"{avg_time:.1f} min")


    with col3:
        data['Order_Time'] = pd.to_datetime(data['Order_Time'], errors='coerce')
        most_common_time = data['Order_Time'].dt.time.mode()[0]
        st.metric("Most Common Time", most_common_time.strftime("%H:%M"))
    
    with col4:
        most_common_area = data['Area'].mode()[0]
        st.metric("Top Delivery Area", most_common_area)
    
    # Area Analysis
    st.subheader("📍 Delivery Area Analysis")
    col1, col2 = st.columns(2)
    with col1:
        area_dist = data['Area'].value_counts()
        fig = px.bar(x=area_dist.values, y=area_dist.index, orientation='h',
                    title='Orders by Area', 
                    labels={'x': 'Number of Orders', 'y': 'Area'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Convert area_dist to a DataFrame
        top_areas = area_dist.head().reset_index()
        top_areas.columns = ["Area", "Orders"]

        # Create donut chart with Plotly
        fig = px.pie(
            top_areas,
            values="Orders",
            names="Area",
            hole=0.4,  # makes it a donut
            title="Top Delivery Areas"
        )

        # Show chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    
    # Performance Metrics
    st.subheader("📈 Performance Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Delivery time distribution
        fig = px.histogram(data, x='Delivery_Time', nbins=30,
                         title='Delivery Time Distribution',
                         labels={'Delivery_Time': 'Delivery Time (minutes)'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Agent rating distribution
        fig = px.histogram(data, x='Agent_Rating', nbins=20,
                         title='Agent Rating Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Vehicle distribution
        vehicle_dist = data['Vehicle'].value_counts()
        fig = px.pie(values=vehicle_dist.values, names=vehicle_dist.index,
                   title='Vehicle Type Distribution')
        st.plotly_chart(fig, use_container_width=True)

with tab2:

    st.header("Maps Overview")
    
    # Map controls
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        #"Delivery Routes": Shows lines between stores and delivery points. "Heatmap": Shows color density of delivery locationsv"Store Locations": Shows only store locations
        map_type = st.selectbox("Map View", ["Delivery Routes", "Heatmap", "Store Locations"])
    
    with col2:
        selected_area = st.selectbox("Filter by Area", ["All Areas"] + list(data['Area'].unique()))
    # Filter data
    map_data = data
    if selected_area != "All Areas":
        map_data = map_data[map_data['Area'] == selected_area]
    
    # Sample for performance
    sample_data = map_data.sample(min(1000, len(map_data)))
    # Create map
    if not sample_data.empty:
        avg_lat = sample_data[['Store_Latitude', 'Drop_Latitude']].mean().mean()
        avg_lon = sample_data[['Store_Longitude', 'Drop_Longitude']].mean().mean()
        
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)
        
        if map_type == "Heatmap":  # Heatmap
            heat_data = []
            for _, row in sample_data.iterrows():
                heat_data.append([row['Drop_Latitude'], row['Drop_Longitude']])
                heat_data.append([row['Store_Latitude'], row['Store_Longitude']])
    
            HeatMap(heat_data, radius=15).add_to(m)
            st.info("🔥 Heatmap showing delivery density")

        elif map_type == "Store Locations":
            # Store locations only
            for _, row in sample_data.iterrows():
                folium.Marker(
                    [row['Store_Latitude'], row['Store_Longitude']],
                    popup=f"Store - {row['Order_ID']}",
                    icon=folium.Icon(color='green', icon='shopping-cart')
                ).add_to(m)
            st.info("🏪 Store locations only")

        else:  # Delivery Routes
            # Delivery routes
            for _, row in sample_data.iterrows():
                # Store marker
                folium.Marker(
                    [row['Store_Latitude'], row['Store_Longitude']],
                    popup=f"Store - {row['Order_ID']}",
                    icon=folium.Icon(color='green', icon='shopping-cart')
                ).add_to(m)
                # Drop marker
                folium.Marker(
                    [row['Drop_Latitude'], row['Drop_Longitude']],
                    popup=f"Delivery - {row['Delivery_Time']}min",
                    icon=folium.Icon(color='red', icon='home')
                ).add_to(m)
                # Route line
                folium.PolyLine(
                    [[row['Store_Latitude'], row['Store_Longitude']], 
                    [row['Drop_Latitude'], row['Drop_Longitude']]],
                    color='blue', weight=2, opacity=0.7
                ).add_to(m)
            st.info("🛣️ Showing delivery routes between stores and drop locations")

        col_map, col_info = st.columns([3, 1])  # Left wide, right narrow

        with col_map:
            st_folium(m, width=800, height=300)

        with col_info:
            st.metric("Locations Shown", len(sample_data))
            st.metric("Area", selected_area)
            avg_delivery_time = sample_data['Delivery_Time'].mean()
            st.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} min")

        st.subheader("📌 Delivery Hotspots and Route Insights")

        with open("../Mapping/foliumMapping.html", "r", encoding="utf-8") as f:
            folium_html = f.read()

        st.components.v1.html(folium_html, height=400, scrolling=True)
        st.markdown("---")
    
    if not map_data.empty:
        # Insight 1: Distance vs Delivery Time Analysis
        # Insight 2: Area Performance Comparison
        col1, col2  = st.columns(2)
        
        with col1:
            st.write("### 📊  Performance Comparison")
            # Weather impact with order volume
            weather_analysis = map_data.groupby('Weather').agg({
                'Delivery_Time': 'mean',
                'Order_ID': 'count'
            }).round(2)
            weather_analysis = weather_analysis.rename(columns={'Order_ID': 'Order_Count'})
            
            fig = px.scatter(
                weather_analysis,
                x='Order_Count',
                y='Delivery_Time',
                size='Order_Count',
                title='Weather Impact: Delivery Time vs Order Volume',
                labels={'Order_Count': 'Number of Orders', 'Delivery_Time': 'Avg Delivery Time (min)'},
                hover_name=weather_analysis.index
            )
            st.plotly_chart(fig, use_container_width=True)
             # Weather impact on delivery time
            weather_impact = map_data.groupby('Weather')['Delivery_Time'].mean().sort_values(ascending=False)
            worst_weather = weather_impact.index[0]
            best_weather = weather_impact.index[-1]
            st.write(f"• **Slowest weather condition:** {worst_weather}")
            st.write(f"• **Fastest weather condition:** {best_weather}")
               
        with col2:
            # Insight 3: Traffic and Weather Impact
            st.write("### 🌦️ Traffic Factors Impact") 
            # Traffic impact on delivery time
            traffic_analysis = map_data.groupby('Traffic').agg({
                'Delivery_Time': 'mean',
                'Distance': 'mean',
                'Order_ID': 'count'
            }).round(2)
            traffic_analysis =traffic_analysis.rename(columns={'Order_ID': 'Order_Count'})
            
            fig = px.bar(
                traffic_analysis, 
                y='Delivery_Time',
                title='Average Delivery Time by Traffic Condition',
                labels={'Delivery_Time': 'Avg Delivery Time (min)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
           
        

with tab3:
    st.header("Delivery Time Prediction")
    # Load your trained model
    @st.cache_resource   # cache so it doesn’t reload every run
    def load_model():
        return joblib.load("../Model/model.joblib")   # or your file path
    
    model = load_model()

    # User input form
    with st.form("delivery_form"):
        # Row 1
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            agent_age = st.number_input("Agent Age", 18, 65, 30)
        with col2:
            distance = st.number_input("Distance (km)", 0.0, 50.0, 5.0)
        with col3:
            prep_time = st.number_input("Prep Time (minutes)", 0, 120, 15)
        with col4:
            am_pm = st.selectbox("Pickup AM/PM", ["AM", "PM"])

        # Row 2
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pickup_hour = st.slider("Pickup Hour", 0, 23, 14)
        with col2:
            order_of_week_day = st.slider("Order Day of Week (0=Mon)", 0, 6, 2)
        with col3:
            order_month = st.slider("Order Month", 1, 12, 3)
        with col4:
            agent_rating = st.slider("Agent Rating", 1.0, 5.0, 4.5)

        # Row 3
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            weather = st.selectbox("Weather", ["Sunny", "Fog", "Stormy", "Windy", "Sandstorms"])
        with col2:
            traffic = st.selectbox("Traffic", ["Low", "Medium", "Jam"])
        with col3:
            vehicle = st.selectbox("Vehicle", ["scooter", "van", "motorcycle"])
        with col4:
            area = st.selectbox("Area", ["Metropolitian", "Urban", "Semi-Urban", "Other"])

        # Extra row for category (since it’s long list)
        category = st.selectbox("Category", ["Electronics", "Clothing", "Grocery", "Books", "Sports"])

        submitted = st.form_submit_button("Predict")

        if submitted:
            # Prepare input row
            input_data = pd.DataFrame([{
                "Agent_Age": agent_age,
                "Agent_Rating": agent_rating,
                "Distance": distance,
                "Prep_Time": prep_time,
                "Pickup_Hour": pickup_hour,
                "Order_of_week_day": order_of_week_day,
                "Order_Month": order_month,
                "Weather": weather,
                "Traffic": traffic,
                "Vehicle": vehicle,
                "Area": area,
                "Category": category,
                "PM_AM": am_pm
            }])

            # Encode input like training
            input_data = pd.get_dummies(input_data)
            input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

            # Predict
            prediction = model.predict(input_data)[0]
            st.success(f"Predicted Delivery Time: {prediction:.1f} minutes")

# Footer
st.markdown("---")
st.markdown("Amazon Delivery Dashboard | Created with Streamlit")