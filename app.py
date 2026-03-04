import streamlit as st
import pandas as pd
import json 
from streamlit_lottie import st_lottie
from datetime import datetime

st.set_page_config(page_title="Clothing Chatbot", layout="centered")
st.title("Clothing Chatbot")

# Cute CSS for buttons and dropdowns
st.markdown("""
    <style>
    .stButton>button {
        color: white;
        background: linear-gradient(90deg, #ffb6c1 0%, #ffe4e1 100%);
        border-radius: 20px;
        font-size: 18px;
        padding: 0.5em 2em;
        box-shadow: 2px 2px 8px #f8bbd0;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ffe4e1 0%, #ffb6c1 100%);
        color: #4B2E83;
    }
    .stSelectbox>div>div {
        border-radius: 12px;
        background: #fff0f5;
        border: 2px solid #ffb6c1 !important;
        box-shadow: 0 2px 8px #f8bbd033;
    }
    .stApp {
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Lottie animation
import json
with open("Shopping.json", "r") as f:
   lottie_json = json.load(f)
st_lottie(lottie_json, height=200)


# --- Weather Section ---
import requests
city = "Houston"
api_key = "2b69f76bbf0f018921e6d22a8a432b71"  # Replace with your real API key
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
response = requests.get(url)
data = response.json()
#st.write(data)  # For debugging
temp = data["main"]["temp"]
today = datetime.now().strftime("%A, %B %d, %Y")
st.info(f"Today is {today}")
weather = data["weather"][0]["description"]
st.info(f"🌤️Weather in {city}: {temp}°F, {weather}🌤️")




csv_path = "/Users/tingtingbi/Downloads/Clothes Inventory - 2026 Clothes.csv"
df = pd.read_csv(csv_path)

def normalise(s):
    return s.strip().lower()

tops_types = ["Shirts", "Dress", "Sweater", "Sweatshirts", "Jacket"]
bottoms_types = ["Leggings", "Shorts", "Skirt", "Pants"]

categories = sorted(df["Category"].unique())
colors = sorted(df["Primary Color"].unique())

# Build lookup dictionary (one or more descriptions per combo)
descriptions = {}
for _, row in df.iterrows():
    cat = row["Category"]
    col = row["Primary Color"]
    typ = row["Type"]
    desc = row["Description (Brand)"].strip()
    key = f"{normalise(cat)}-{normalise(col)}-{normalise(typ)}"
    if key not in descriptions:
        descriptions[key] = []
    descriptions[key].append(desc)

# Session state for results
if "top_results" not in st.session_state:
    st.session_state.top_results = []
if "bottom_results" not in st.session_state:
    st.session_state.bottom_results = []

# --- Split page: Tops (left), Bottoms (right) ---
left, right = st.columns(2)

with left:
    st.subheader("Cute Tops")
    tops_types_available = [t for t in tops_types if t in df["Type"].unique()]
    selected_category_top = st.selectbox("Category (Tops)", categories, key="cat_top")
    selected_color_top = st.selectbox("Primary Color (Tops)", colors, key="color_top")
    selected_type_top = st.selectbox("Type (Tops)", tops_types_available, key="type_top")

    if st.button("✨ Describe Top ✨", key="describe_top", use_container_width=True):
        key_top = f"{normalise(selected_category_top)}-{normalise(selected_color_top)}-{normalise(selected_type_top)}"
        if key_top in descriptions:
            st.session_state.top_results = descriptions[key_top]
        else:
            st.session_state.top_results = ["No top description found for this combination."]

    if st.session_state.top_results:
        st.success("Top Found!")
        for desc in st.session_state.top_results:
            st.markdown(f"**{desc}**")

# If the selected top type is "Dress", skip bottoms and combinations
if selected_type_top == "Dress":
    st.info("You selected a Dress. No bottom needed!")
else:
    with right:
        st.subheader("Adorable Bottoms")
        bottoms_types_available = [t for t in bottoms_types if t in df["Type"].unique()]
        selected_category_bottom = st.selectbox("Category (Bottoms)", categories, key="cat_bottom")
        selected_color_bottom = st.selectbox("Primary Color (Bottoms)", colors, key="color_bottom")
        selected_type_bottom = st.selectbox("Type (Bottoms)", bottoms_types_available, key="type_bottom")

        if st.button("✨ Describe Bottom ✨", key="describe_bottom", use_container_width=True):
            key_bottom = f"{normalise(selected_category_bottom)}-{normalise(selected_color_bottom)}-{normalise(selected_type_bottom)}"
            if key_bottom in descriptions:
                st.session_state.bottom_results = descriptions[key_bottom]
            else:
                st.session_state.bottom_results = ["No bottom description found for this combination."]

        if st.session_state.bottom_results:
            st.success("Bottom Found!")
            for desc in st.session_state.bottom_results:
                st.markdown(f"**{desc}**")

    # --- All Combinations Section ---
      # --- All Combinations Section ---
    st.divider()
    st.subheader("🌸 Outfit Ideas🌸")

    if st.session_state.top_results and st.session_state.bottom_results:
        for top in st.session_state.top_results:
            for bottom in st.session_state.bottom_results:
                st.markdown(
                    f"<b>Top:</b> {top}<br><b>Bottom:</b> {bottom}",
                    unsafe_allow_html=True
                )
    else:
        st.info("Select and describe both a top and a bottom to see all combinations.")