# 📦 Amazon Delivery Geo-Analytics
This is a data science and machine learning project that analyzes delivery geo-data, builds predictive models, and provides an interactive dashboard with real-time delivery time predictions. Developed during the Tuwaiq Academy Data Science & ML Bootcamp (Week 3 Project).

---
### 🎯 Objectives
- Analyze delivery geo-data to uncover trends and patterns.
- Identify key factors influencing delivery time.
- Build a regression model.
- Deploy a FastAPI backend with endpoints for real-time delivery time prediction.
- Create an interactive dashboard (Streamlit + Plotly) for data visualization and user input.

---
### ✨ Features
- 📊 Exploratory Data Analysis (EDA): Distribution analysis, correlations, and statistical summaries.
- 🤖 Predictive Modeling: Scikit-learn regression model.
- ⚡ FastAPI Backend: REST API for car price predictions (/predict).
- 📈 Interactive Dashboard: Built with Streamlit + Plotly for user-friendly visualizations focused on maps.

---
### 🛠 Tech Stack
- Python: NumPy, Pandas, Matplotlib, Seaborn.
- Visualization: Streamlit, Plotly.
- Machine Learning: Scikit-learn.
- Backend: FastAPI (for API endpoints).
- Version Control: Git + GitHub.

---
### 📂 Project Structure (will be updated)
```bash
Amazon-Delivery-GeoAnalytics/
│── Analytics/                                        # Preprocessing & Dashboard
    └── Dashboard.py                                  # Streamlit Dashboard App
    └── Preprocessing.ipynb                           # EDA & Cleaning Notebook
    └── car.png                                       # Asset
│── Dataset/                                          # Raw & Cleaned Datasets
    └── car_sales_data.csv                            # Original Dataset
    └── processed_car_sales_data_cleaning.scv         # Procssed Dataset
│── Model/                                            # Model Train & Interface
    └── Machine_Learning_Train.ipynb                  # ML Model Train
    └── Statmodels_Train.ipynb                        # Statmodels Model Train
    └── Deep_Learning_Train.ipynb                     # DL Model Train
    └── Interface.py                                  # Fast API App
    └── Model.pkl                                     # Trained Model
    └── model_metadata                                # Models Metadata
│── requirements.txt                                  # Dependencies
│── Procfile.txt                                      # Deployment Startup Script
│── README.md                                         # Project Documentation
```

---
### 📊 Dataset
This Amazon Delivery Dataset provides a comprehensive view of the company's last-mile logistics operations. It includes data on over 43,632 deliveries across multiple cities, with detailed information on order details, delivery agents, weather and traffic conditions, and delivery performance metrics. The dataset enables researchers and analysts to uncover insights into factors influencing delivery efficiency, identify areas for optimization, and explore the impact of various variables on the overall customer experience.

- Contains the attributes: Order ID, Agent Age, Agent Rating, Store Latitude, Store Longitude, Drop Latitude, Drop Longitude, Order Date, Order Time, Pickup Time, Weather, Traffic, Vehicle, Area, Delivery Time, and Category.
- Source: [Kaggle – Amazon Delivery Dataset](https://www.kaggle.com/datasets/sujalsuthar/amazon-delivery-dataset).

---
### ⚙️ Installation
1. Clone Repository
   ``` bash
   git clone https://github.com/SarahAlshaikhmohamed/Amazon-Delivery-GeoAnalytics.git
   cd Amazon-Delivery-GeoAnalytics
   ```
2. (optional) Create a Virtual Environment
   1. UV Environment:
      ```bash
      pip install uv
      uv venv my-venv
      my-venv\Scripts\Activate
      uv init
      ```
   2. Virtual Environment (Windows):
      ```bash
      python -m venv my-venv
      my-venv\Scripts\Activate
      ```
   3. Virtual Environment (Linux):
      ```bash
      python3 -m venv my-venv
      source my-venv/bin/activate
      ```
3. Install Dependencies
   1. UV Environment:
      ```bash
      uv add requirements.txt
      ```
   2. Virtual Environment
      ```bash
      pip install -r requirements.txt
      ```

---
### ▶️ Usage (will be updated)
- Run EDA & Preprocessing
  ```bash
  python eda/eda_script.py
  ```
- Run Streamlit dashboard
  ```bash
  python -m streamlit run Dashboard.py
  ```
- Run FastAPI Server
  ```bash
  python -m uvicorn Interface:app --reload
  ```
- View Dashboard
  
  [Car Sales Dashboard]()
  
---
### 🌐 API Endpoints (will be updated)
The FastAPI backend exposes several endpoints:
| Method | Endpoint | Description | Request Body (JSON) | Response (JSON) |
|--------|----------|-------------|----------------------|-----------------|
| GET | `/` | Verify that the API is running | None | { "message": "Price Prediction API is running!" }
| POST | `/predict` | Predict car price using Statsmodels, Scikit-learn, and Keras models | json { "engine_size": 2.0, "year": 2018, "mileage": 50000, "manufacturer": "Ford", "model": "Focus", "fuel_type": "Petrol" } | json { "stat_price": 15234.56, "ml_price": 14987.33, "dl_price": 15100.12 }

---
### 📈 Results & Insights (will be updated)
1.  .
2.  .
3.  .

---
### 🚀 Recommendations & Future Work (will be updated)
 - . 
 - .
 - .

---
### 👥 Contributors
- Nouf Almutiri.
- Sarah Alshaikhmohamed.
- Shams Alarifi

---
### 📽️ Presentation
[Project Presentation](https://www.canva.com/design/DAG0F527D8o/cIP1Sh_so05MounhlD1qrw/edit?utm_content=DAG0F527D8o&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---
### 📜 License
This project is licensed under the MIT License.
