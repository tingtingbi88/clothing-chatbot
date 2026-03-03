import streamlit as st
import pandas as pd

# Load and parse the CSV
csv_path = "/Users/tingtingbi/Downloads/Clothes Inventory - 2026 Clothes.csv"
df = pd.read_csv(csv_path)

# Normalize strings
def normalise(s):
    return s.strip().lower()

# Build unique lists
categories = sorted(df["Category"].unique())
colors = sorted(df["Primary Color"].unique())
types = sorted(df["Type"].unique())

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

# Streamlit UI
st.set_page_config(page_title="Clothing Chatbot", layout="centered")
st.title("🧥 Clothing Chatbot")

col1, col2, col3 = st.columns(3)

with col1:
    selected_category = st.selectbox("Category", categories)

with col2:
    selected_color = st.selectbox("Primary Color", colors)

with col3:
    selected_type = st.selectbox("Type", types)

if st.button("Describe", use_container_width=True):
    key = f"{normalise(selected_category)}-{normalise(selected_color)}-{normalise(selected_type)}"
    
    if key in descriptions:
        st.success("✨ Found!")
        for desc in descriptions[key]:
            st.write(f"• {desc}")
    else:
        st.warning("No description found for this combination.")