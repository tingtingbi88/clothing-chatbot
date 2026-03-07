
import streamlit as st
import pandas as pd
import random
import re

# Load recipes data
RECIPES_CSV = "/Users/tingtingbi/Downloads/Digital_Recipes.csv"

st.set_page_config(page_title="Weekly Meal Prep Generator", layout="wide")
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
    body, .stApp {
        background-color: #f5ecd7 !important;
    }
    .stTitle, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        font-family: 'Pacifico', 'Quicksand', cursive, sans-serif !important;
        letter-spacing: 0.5px;
    }
    .meal-card {
        background: linear-gradient(120deg, #ffe5ec 0%, #e0f7fa 100%);
        border-radius: 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.10);
        border: 1.5px solid #f7cac9;
        padding: 1.2em 1.5em 1.2em 1.5em;
        margin-bottom: 1.5em;
        transition: box-shadow 0.2s;
    }
    .meal-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.13);
    }
    .meal-title {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 0.5em;
        font-family: 'Quicksand', 'Arial', sans-serif !important;
    }
    .grocery-panel {
        background: #fff8f0;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.10);
        border: 1.5px solid #f7cac9;
        padding: 1.2em 1.5em 1.2em 1.5em;
        margin-bottom: 1.5em;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Weekly Meal Prep Generator 👩🏻‍🍳")

# Read the recipes CSV
def load_recipes():
    try:
        df = pd.read_csv(RECIPES_CSV)
        return df
    except Exception as e:
        st.error(f"Error loading recipes: {e}")
        return pd.DataFrame()

df = load_recipes()

if df.empty:
    st.stop()

# Only select entrees (exclude sides and desserts) based on 'Meal' column, robust to spaces/casing
if 'Meal' in df.columns:
    entree_df = df[df['Meal'].astype(str).str.strip().str.lower() == 'entree'] # sometimes there are trailing spaces and also convert the name to lower
else:
    # If no 'Meal' column, assume all are entrees
    entree_df = df.copy()

# Days of the week
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Button to generate a week's worth of meals
if st.button("Generate Weekly Meal Plan🪄"):
    if len(entree_df) < 7:
        st.warning("Not enough entree recipes to generate a full week!")
    else:
        selected_indices = random.sample(range(len(entree_df)), 7)
        week_plan = entree_df.iloc[selected_indices].reset_index(drop=True)
        st.subheader(":calendar: Your Meal Plan 📝:")
        meal_plan = {}
        # Collect all unique grocery items for summary
        unique_grocery_items = set()
        # Two-column layout: meals (left), grocery (right)
        left_col, right_col = st.columns([1.2, 1])
        with left_col:
            day_emojis = ["🌞", "🌱", "🌮", "🍝", "🍲", "🍕", "🥘"]
            pastel_cards = [
                "linear-gradient(120deg, #ffe5ec 0%, #e0f7fa 100%)",
                "linear-gradient(120deg, #e0f7fa 0%, #ffe5ec 100%)",
                "linear-gradient(120deg, #fff1e6 0%, #e0f7fa 100%)",
                "linear-gradient(120deg, #e0f7fa 0%, #fff1e6 100%)",
                "linear-gradient(120deg, #e0f2f1 0%, #ffe5ec 100%)",
                "linear-gradient(120deg, #ffe5ec 0%, #e0f2f1 100%)",
                "linear-gradient(120deg, #f3e8ff 0%, #ffe5ec 100%)",
            ]
            for i, day in enumerate(days):
                recipe_name = week_plan.loc[i, 'Entree'] if 'Entree' in week_plan.columns else week_plan.loc[i, 'Recipe']
                ingredients = week_plan.loc[i, 'Ingredients'] if 'Ingredients' in week_plan.columns else ''
                instructions = week_plan.loc[i, 'Instructions'] if 'Instructions' in week_plan.columns else ''
                effort = week_plan.loc[i, 'Effort'] if 'Effort' in week_plan.columns else ''
                # Effort icon
                effort_icon = ""
                if str(effort).strip():
                    try:
                        effort_val = int(effort)
                        if effort_val <= 1:
                            effort_icon = "⭐️ Easy"
                        elif effort_val == 2:
                            effort_icon = "⏳ Medium"
                        else:
                            effort_icon = "🔥 Hard"
                    except:
                        effort_icon = f"{effort}"
                # Pastel card color
                card_color = pastel_cards[i % len(pastel_cards)]
                st.markdown(f"""
                    <div class='meal-card' style='background:{card_color};'>
                        <div class='meal-title'>{day_emojis[i]} <b>{day}</b>: {recipe_name}</div>
                        <span style='font-size:0.95em; color:#888;'>{effort_icon}</span>
                """, unsafe_allow_html=True)
                # Ingredients preview (collapsed in expander)
                if pd.notna(ingredients):
                    items = [item.strip() for item in str(ingredients).splitlines() if item.strip()]
                    formatted_ingredients = '\n'.join(f"- {item}" for item in items)
                    unique_grocery_items.update(items)
                else:
                    formatted_ingredients = ''
                with st.expander("Show Recipe Details"):
                    if pd.notna(instructions) and str(instructions).strip():
                        st.markdown(f"**Instructions:**\n{instructions}")
                    else:
                        st.markdown("No instructions available.")
                    if pd.notna(effort) and str(effort).strip():
                        st.markdown(f"**Effort Level:** {effort_icon}")
                    else:
                        st.markdown("Effort level not specified.")
                st.markdown(f"<div style='margin-bottom:0.5em'></div></div>", unsafe_allow_html=True)
        with right_col:
            st.markdown("<div class='grocery-panel'>", unsafe_allow_html=True)
            st.subheader("🛒 Grocery List")
            for i, day in enumerate(days):
                recipe_name = week_plan.loc[i, 'Entree'] if 'Entree' in week_plan.columns else week_plan.loc[i, 'Recipe']
                ingredients = week_plan.loc[i, 'Ingredients'] if 'Ingredients' in week_plan.columns else ''
                if pd.notna(ingredients):
                    items = [item.strip() for item in str(ingredients).splitlines() if item.strip()]
                    formatted_ingredients = '\n'.join(f"- {item}" for item in items)
                else:
                    formatted_ingredients = ''
                st.markdown(f"**{day} ({recipe_name}):**\n{formatted_ingredients}")
            st.markdown(f"**Total unique grocery items for the week:** {len(unique_grocery_items)}")
            if unique_grocery_items:
                st.markdown("<details><summary>Show all unique items</summary>" + "<br>".join(sorted(unique_grocery_items)) + "</details>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Click the button to generate your meal plan and grocery list!")
