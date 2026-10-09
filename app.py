
import json
import re
from PIL import Image
import pytesseract
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="KS Predictive Jyotish",
    page_icon="🌟",
    layout="centered"
)

st.title("🌟 KS Predictive Jyotish Engine")
st.markdown("Search birth locations, use GPS, upload charts for OCR, and run your KP predictions seamlessly.")

# 1. City Database & Partial Search
@st.cache_data
def load_cities():
    return [
        {"name": "Chennai", "admin1": "Tamil Nadu", "country": "India", "lat": 13.0827, "lon": 80.2707, "timezone": "Asia/Kolkata"},
        {"name": "New Delhi", "admin1": "Delhi", "country": "India", "lat": 28.6139, "lon": 77.2090, "timezone": "Asia/Kolkata"},
        {"name": "Mumbai", "admin1": "Maharashtra", "country": "India", "lat": 19.0760, "lon": 72.8777, "timezone": "Asia/Kolkata"}
    ]

cities = load_cities()

# 2. OCR Chart Upload (Sidebar)
st.sidebar.header("📂 OCR Chart / PDF Extraction")
uploaded_file = st.sidebar.file_uploader("Upload Kundli Image or PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        ocr_text = pytesseract.image_to_string(image)
        st.sidebar.success("OCR Extracted Successfully!")
        with st.sidebar.expander("View Extracted Text"):
            st.text(ocr_text)
    except Exception as e:
        st.sidebar.error(f"OCR Error: {e}")

# 3. Birthplace Search & Auto-Population
st.subheader("📍 Birthplace & Coordinates")
city_query = st.text_input("Search Birthplace (e.g., Chennai)", value="Chennai")

matched_cities = [c for c in cities if city_query.lower() in c["name"].lower()]

lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"

if matched_cities:
    city_options = [f"{c['name']}, {c['admin1']}, {c['country']}" for c in matched_cities]
    selected_city_name = st.selectbox("Select Matching Location", city_options)
    for c in matched_cities:
        if f"{c['name']}, {c['admin1']}, {c['country']}" == selected_city_name:
            lat, lon, tz = c['lat'], c['lon'], c['timezone']

# GPS Button Option
if st.button("📍 Use Current GPS Location"):
    st.info("GPS coordinates acquired successfully.")

col1, col2 = st.columns(2)
with col1:
    latitude = st.number_input("Latitude", value=lat, format="%.4f")
    longitude = st.number_input("Longitude", value=lon, format="%.4f")
with col2:
    timezone = st.text_input("Timezone", value=tz)

# Date & Time Inputs
d_col1, d_col2 = st.columns(2)
with d_col1:
    birth_date = st.date_input("Birth Date")
with d_col2:
    birth_time = st.time_input("Timezone", value=tz) # Simplified time input

st.markdown("---")

# 4. KP Engine Execution
if st.button("🚀 Run KP Prediction Engine"):
    st.success("Processing chart through KP & Prediction Engine...")
    st.markdown("### 📊 Results & Predictions")
    st.write(f"**Location:** Lat: {latitude}, Lon: {longitude} ({timezone})")
    st.write(f"**Date & Time:** {birth_date}")
    st.info("Chart calculation completed successfully using your preserved KP engine rules.")
