import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv("ride_fare_data.csv")

X = df.drop("fare_price", axis=1)
y = df["fare_price"]

categorical_cols = ["weather", "service"]
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ],
    remainder="passthrough" 
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

model.fit(X, y)

st.set_page_config(page_title="Ride Fare Predictor", layout="centered")
st.title("🚖 Ola/Uber Fare Price Predictor")

st.markdown("### Enter Ride Details:")

service = st.selectbox("Service", ["Ola", "Uber"])
distance_km = st.slider("Distance (km)", 1.0, 25.0, 5.0)
fuel_price = st.slider("Fuel Price (₹ per litre)", 90.0, 120.0, 100.0)
is_peak_hour = st.checkbox("Is Peak Hour?", value=False)
weather = st.selectbox("Weather", ["clear", "cloudy", "rainy", "storm"])
service_availability = st.slider("Service Availability (0 = low, 1 = high)", 0.0, 1.0, 0.8)

input_data = pd.DataFrame([{
    "service": service,
    "distance_km": distance_km,
    "fuel_price": fuel_price,
    "is_peak_hour": int(is_peak_hour),
    "weather": weather,
    "service_availability": service_availability
}])

predicted_fare = model.predict(input_data)[0]
st.success(f"💰 Predicted Fare: ₹{predicted_fare:.2f}")
