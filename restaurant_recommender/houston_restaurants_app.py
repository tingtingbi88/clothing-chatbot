## (Removed invalid move/delete comments)
import streamlit as st
import pandas as pd

# Set a soft blue background color

st.markdown(
    """
    <style>
    html, body, .stApp, .main, .block-container, .stMarkdown, .stText, .stDataFrame, .stSelectbox, .stRadio, .stCheckbox, .stButton, .stCaption, .stSubheader, .stHeader, .stTitle, .stTextInput, .stSelectbox label, .stRadio label, .stCheckbox label {
        font-size: 28px !important;
        font-family: 'Segoe UI', 'Arial', sans-serif !important;
    }
    body, .stApp {
        background-color: #e3f0ff !important;
    }
    .main .block-container {
        max-width: 100vw !important;
        padding-left: 0vw !important;
        padding-right: 0vw !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Restaurant Recommender", layout="wide")
st.title("Restaurant Recommender")

# --- City selection and data loading ---


# City selection as large radio buttons with subheaders
st.markdown("""
<style>
.stRadio > div[role='radiogroup'] label {
    font-size: 1.5em !important;
    font-weight: bold !important;
    margin-right: 2em;
}
</style>
""", unsafe_allow_html=True)
st.subheader("**Select City:**")
import re
def strip_html_tags(text):
    return re.sub('<.*?>', '', text)
city_options = ["<b>🤠Houston</b>", "<b>🌵Phoenix</b>", "<b>🍑Atlanta</b>"]
selected_city_label = st.radio(
    "Select City",
    city_options,
    horizontal=True,
    key="city_radio",
    label_visibility="collapsed",
    format_func=lambda x: strip_html_tags(x)
)
if strip_html_tags(selected_city_label) == "🤠Houston":
    selected_city = "Houston"
    df = pd.read_csv("/Users/tingtingbi/Downloads/Houston_Restaurants.csv")
elif strip_html_tags(selected_city_label) == "🌵Phoenix":
    selected_city = "Phoenix"
    df = pd.read_csv("/Users/tingtingbi/Downloads/Arizona_Restaurants.csv")
else:
    selected_city = "Atlanta"
    df = pd.read_csv("/Users/tingtingbi/Downloads/Atlanta_Restaurants.csv")
    # Normalize column names for Atlanta
    df = df.rename(columns={"Restaurant name": "Restaurant Name"})



# Get unique locations and types for the selected city
locations = sorted(df["location"].dropna().unique())
types = sorted(df["type"].dropna().unique())





# Checkboxes for location selection with Select All only
st.subheader("**Select Location(s):**")
if 'loc_selected' not in st.session_state:
    st.session_state['loc_selected'] = {loc: True for loc in locations}  # Initialize selected locations
loc_cols = st.columns(min(len(locations), 4))
selected_locations = []
for i, loc in enumerate(locations):
    checked = st.session_state['loc_selected'].get(loc, True)
    new_val = loc_cols[(i + 1) % 4].checkbox(loc, value=checked, key=f"loc_{loc}")
    st.session_state['loc_selected'][loc] = new_val
    if new_val:
        selected_locations.append(loc)


# Checkboxes for type selection (with emojis)
st.subheader("**Select Type(s):**")
type_emojis = {
    "dessert": "🍦🧋",
    "cafe": "🍵☕️",
    "restaurant": "🍽️",
    "bar": "🥂"
}
if 'type_selected' not in st.session_state:
    st.session_state['type_selected'] = {t: True for t in types}
type_cols = st.columns(min(len(types), 4))
selected_types = []
for i, t in enumerate(types):
    label = f"{type_emojis.get(t.lower(), '')} {t.title()}" if t.lower() in type_emojis else t.title()
    checked = st.session_state['type_selected'].get(t, True)
    new_val = type_cols[i % 4].checkbox(label, value=checked, key=f"type_{t}_{i}")
    st.session_state['type_selected'][t] = new_val
    if new_val:
        selected_types.append(t)

# Seating dropdown for Atlanta
selected_seating = None
if selected_city == "Atlanta":
    seating_options = sorted(df["seating"].dropna().unique()) if "seating" in df.columns else []
    if seating_options:
        selected_seating = st.selectbox("Select Seating", ["(Any)"] + seating_options)



# Show cost dropdown only if 'restaurant' is among selected types
selected_cost = None
if any(t.lower() == "restaurant" for t in selected_types):
    cost_options = sorted(df["Cost"].dropna().unique()) if "Cost" in df.columns else []
    if cost_options:
        selected_cost = st.selectbox("Select Cost", ["(Any)"] + cost_options)



# If type is 'restaurant' and city is Houston, show cuisine dropdown (only if 'Cuisine' column exists)
cuisine_options = []
selected_cuisine = None
if "restaurant" in [t.lower() for t in selected_types] and selected_city == "Houston" and "Cuisine" in df.columns:
    # Filter by selected locations and types first
    filtered_for_cuisine = df[df["location"].isin(selected_locations) & df["type"].isin(selected_types)]
    # Get unique cuisines for this selection
    cuisine_options = sorted(filtered_for_cuisine["Cuisine"].dropna().unique())
    if cuisine_options:
        cuisine_options = ["(Any)"] + cuisine_options
        selected_cuisine = st.selectbox("Select Cuisine", cuisine_options)




# Filter restaurants based on selection
# If nothing is selected, filtered will be empty. If all are selected, include all.
if not selected_locations:
    filtered = df.iloc[0:0]  # empty DataFrame
else:
    filtered = df[df["location"].isin(selected_locations)]
if not selected_types:
    filtered = filtered.iloc[0:0]
else:
    filtered = filtered[filtered["type"].isin(selected_types)]
if any(t.lower() == "restaurant" for t in selected_types) and selected_cost and selected_cost != "(Any)":
    filtered = filtered[filtered["Cost"] == selected_cost]
# Apply seating filter for Atlanta
if selected_city == "Atlanta" and selected_seating and selected_seating != "(Any)":
    filtered = filtered[filtered["seating"] == selected_seating]

# Output recommended restaurants

# Layout: main (left) and favorites (right)
left, right = st.columns([2, 1])

with left:
    # --- Favorites section next to dropdowns ---


    # Define go-tos for use in card rendering
    houston_go_tos = [
        "La la kind cafe",
        "mala",
        "happy lamb hot pot"
    ]
    phoenix_go_tos = [
        "Schmooze",
        "Light Heart",
        "Brightside Cafe"
    ]
    atlanta_go_tos = [
        "delbar",
        "food terminal",
        "yeppa"
    ]

    fav_col1, fav_col2, fav_col3 = st.columns([1, 1, 1])
    with fav_col1:
        st.markdown("<div style='margin-bottom:0.5em'></div>", unsafe_allow_html=True)
        st.subheader("🤠Houston Go-Tos:")
        for fav in houston_go_tos:
            st.markdown(f"⭐ <b>{fav.title()}</b>", unsafe_allow_html=True)
    with fav_col2:
        st.markdown("<div style='margin-bottom:0.5em'></div>", unsafe_allow_html=True)
        st.subheader("🌵Phoenix Go-Tos:")
        for fav in phoenix_go_tos:
            st.markdown(f"⭐ <b>{fav}</b>", unsafe_allow_html=True)
    with fav_col3:
        st.markdown("<div style='margin-bottom:0.5em'></div>", unsafe_allow_html=True)
        st.subheader("🍑Atlanta Go-Tos:")
        for fav in atlanta_go_tos:
            st.markdown(f"⭐ <b>{fav.title()}</b>", unsafe_allow_html=True)

    st.subheader("Recommended Restaurants:")
    # If cuisine is selected, filter by it as well
    filtered_display = filtered
    if "restaurant" in [t.lower() for t in selected_types]:
        if selected_cuisine and selected_cuisine != "(Any)":
            filtered_display = filtered_display[filtered_display["Cuisine"] == selected_cuisine]


    # Surprise Me button for filtered results (current city/filters)
    if not filtered_display.empty:
        if st.button("🎲 Surprise Me!"):
            import random
            random_idx = random.choice(filtered_display.index.tolist())
            random_row = filtered_display.loc[random_idx]
            st.balloons()
            st.success(f"Surprise pick: **{random_row.get('Restaurant Name', random_row.get('name', ''))}** in {random_row.get('location', '')}")
            # Show the card for the surprise pick
            name = random_row.get("Restaurant Name", random_row.get("name", "")).strip()
            type_val = random_row.get("type", "").lower() if pd.notna(random_row.get("type", "")) else ""
            cuisine = random_row.get("Cuisine", "") if pd.notna(random_row.get("Cuisine", "")) else ""
            notes = random_row.get("notes", "")
            seating = random_row.get("seating", "")
            parking = str(random_row.get("parking", ""))
            walkable = "walkable" in parking.lower()
            parking_lower = parking.lower()
            if walkable:
                walk_emoji = " 🚶🏻‍♂️"
                parking_emoji = ""
            else:
                walk_emoji = ""
                parking_emoji = ""
                if "free open lot" in parking_lower or "heights mercantile free two hour parking" or "free MKT parking" or "free parking lot" in parking_lower:
                    parking_emoji = " 🚗"
                elif "paid" in parking_lower:
                    parking_emoji = " 🅿️"
            star_emoji = ""
            if selected_city == "Houston" and name.lower() in [g.lower() for g in houston_go_tos]:
                star_emoji = " ⭐"
            if selected_city == "Phoenix" and name.lower() in [g.lower() for g in phoenix_go_tos]:
                star_emoji = " ⭐"
            if selected_city == "Atlanta" and name.lower() in [g.lower() for g in atlanta_go_tos]:
                star_emoji = " ⭐"
    
            cuisine_emoji = ""
            if cuisine == "Japanese":
                cuisine_emoji = " 🍜"
            elif cuisine == "American":
                cuisine_emoji = " 🍔"
            elif cuisine == "Chinese":
                cuisine_emoji = " 🥟🥢"
            elif cuisine == "Italian":
                cuisine_emoji = " 🍝🍕"
            elif cuisine == "Mexican":
                cuisine_emoji = " 🌮"
            if type_val == "restaurant" and cuisine:
                cuisine_line = f"<b>Cuisine:</b> {cuisine}{cuisine_emoji}<br>"
            else:
                cuisine_line = ""
            card_style = "border-radius:18px; box-shadow: 0 4px 16px rgba(0,0,0,0.10); border:1px solid #ffb6c1; background:{}; padding:1em; margin-bottom:1em; width: 100%; max-width: 350px; min-width: 220px; box-sizing: border-box;"
            highlight_color = "#ffe066"  # yellow highlight
            card_color = highlight_color
            if selected_city == "Houston":
                card_html = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4>{cuisine_line}<b>Notes:</b> {notes}<br><b>Parking:</b> {parking}{parking_emoji}{walk_emoji}</div>'
            elif selected_city == "Phoenix":
                card_html = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4>{cuisine_line}<b>Notes:</b> {notes}</div>'
            elif selected_city == "Atlanta":
                card_html = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4><b>Notes:</b> {notes}<br><b>Seating:</b> {seating}</div>'
            st.markdown(card_html, unsafe_allow_html=True)

    # Surprise Me (Anywhere!) button for all cities/all restaurants
    all_dfs = []
    # Houston
    df_houston = pd.read_csv("/Users/tingtingbi/Downloads/Houston_Restaurants.csv")
    df_houston["city"] = "Houston"
    all_dfs.append(df_houston)
    # Phoenix
    df_phoenix = pd.read_csv("/Users/tingtingbi/Downloads/Arizona_Restaurants.csv")
    df_phoenix["city"] = "Phoenix"
    all_dfs.append(df_phoenix)
    # Atlanta
    df_atlanta = pd.read_csv("/Users/tingtingbi/Downloads/Atlanta_Restaurants.csv")
    df_atlanta = df_atlanta.rename(columns={"Restaurant name": "Restaurant Name"})
    df_atlanta["city"] = "Atlanta"
    all_dfs.append(df_atlanta)
    all_restaurants = pd.concat(all_dfs, ignore_index=True)
    if st.button("🌎 Surprise Me (Anywhere!)"):
        import random
        random_idx = random.choice(all_restaurants.index.tolist())
        random_row = all_restaurants.loc[random_idx]
        st.balloons()
        st.success(f"Anywhere pick: **{random_row.get('Restaurant Name', random_row.get('name', '')).title()}** in {random_row.get('location', '')} ({random_row.get('city', '')})")
        # Show the card for the surprise pick (city-specific logic)
        name = random_row.get("Restaurant Name", random_row.get("name", "")).strip()
        type_val = random_row.get("type", "").lower() if pd.notna(random_row.get("type", "")) else ""
        cuisine = random_row.get("Cuisine", "") if pd.notna(random_row.get("Cuisine", "")) else ""
        notes = random_row.get("notes", "")
        seating = random_row.get("seating", "")
        parking = str(random_row.get("parking", ""))
        walkable = "walkable" in parking.lower()
        parking_lower = parking.lower()
        if walkable:
            walk_emoji = " 🚶🏻‍♂️"
            parking_emoji = ""
        else:
            walk_emoji = ""
            parking_emoji = ""
            if "free open lot" in parking_lower or "heights mercantile free two hour parking" or "free MKT parking" or "free parking lot" in parking_lower:
                parking_emoji = " 🚗"
            elif "paid" in parking_lower:
                parking_emoji = " 🅿️"
        star_emoji = ""
        city_val = random_row.get("city", "")
        if city_val == "Houston" and name.lower() in [g.lower() for g in houston_go_tos]:
            star_emoji = " ⭐"
        if city_val == "Phoenix" and name.lower() in [g.lower() for g in phoenix_go_tos]:
            star_emoji = " ⭐"
        if city_val == "Atlanta" and name.lower() in [g.lower() for g in atlanta_go_tos]:
            star_emoji = " ⭐"
        # Use a default color for surprise anywhere
        highlight_color = "#ffe066"  # yellow highlight
        card_color = highlight_color
        cuisine_emoji = ""
        if cuisine == "Japanese":
            cuisine_emoji = " 🍜"
        elif cuisine == "American":
            cuisine_emoji = " 🍔"
        elif cuisine == "Chinese":
            cuisine_emoji = " 🥟🥢"
        elif cuisine == "Italian":
            cuisine_emoji = " 🍝🍕"
        elif cuisine == "Mexican":
            cuisine_emoji = " 🌮"
        if type_val == "restaurant" and cuisine:
            cuisine_line = f"<b>Cuisine:</b> {cuisine}{cuisine_emoji}<br>"
        else:
            cuisine_line = ""
        card_style = "border-radius:18px; box-shadow: 0 4px 16px rgba(0,0,0,0.10); border:1px solid #ffb6c1; background:{}; padding:1em; margin-bottom:1em; width: 100%; max-width: 350px; min-width: 220px; box-sizing: border-box;"
        if city_val == "Houston":
            card_html = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4>{cuisine_line}<b>Notes:</b> {notes}<br><b>Parking:</b> {parking}{parking_emoji}{walk_emoji}</div>'
        elif city_val == "Phoenix":
            card_html = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4>{cuisine_line}<b>Notes:</b> {notes}</div>'
        elif city_val == "Atlanta":
            card_html = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4><b>Notes:</b> {notes}<br><b>Seating:</b> {seating}</div>'
        st.markdown(card_html, unsafe_allow_html=True)

    # Show debug info for number of results
    st.caption(f"Results found: {len(filtered_display)}")
    if not filtered_display.empty:
        # Use a single default card color for all cards (no cuisine colors)
        default_color = "#fff0f5"

        # Create two columns once for all cards
        card_cols = st.columns([1, 0.05, 1])  # left, gap, right
        left_col, _, right_col = card_cols
        for idx, (_, row) in enumerate(filtered_display.iterrows()):
            name = row["Restaurant Name"].strip() if "Restaurant Name" in row else row.get("name", "").strip()
            type_val = row["type"].lower() if "type" in row and pd.notna(row["type"]) else ""
            cuisine = row["Cuisine"] if "Cuisine" in row and pd.notna(row["Cuisine"]) else ""
            notes = row.get("notes", "")
            seating = row.get("seating", "")
            parking = str(row.get("parking", ""))
            walkable = "walkable" in parking.lower()
            # Parking emoji logic
            parking_lower = parking.lower()
            if walkable:
                walk_emoji = " 🚶🏻‍♂️"
                parking_emoji = ""
            else:
                walk_emoji = ""
                parking_emoji = ""
                if "free open lot" in parking_lower or "heights mercantile free two hour parking" or "free MKT parking" or "free parking lot" in parking_lower:
                    parking_emoji = " 🚗"
                elif "paid" in parking_lower:
                    parking_emoji = " 🅿️"
            # Add star if in go-tos for the selected city
            star_emoji = ""
            if selected_city == "Houston" and name.lower() in [g.lower() for g in houston_go_tos]:
                star_emoji = " ⭐"
            if selected_city == "Phoenix" and name.lower() in [g.lower() for g in phoenix_go_tos]:
                star_emoji = " ⭐"
            if selected_city == "Atlanta" and name.lower() in [g.lower() for g in atlanta_go_tos]:
                star_emoji = " ⭐"
            card_color = default_color
            # Cuisine emoji logic
            cuisine_emoji = ""
            if cuisine == "Japanese":
                cuisine_emoji = " 🍜"
            elif cuisine == "American":
                cuisine_emoji = " 🍔"
            elif cuisine == "Chinese":
                cuisine_emoji = " 🥟🥢"
            elif cuisine == "Italian":
                cuisine_emoji = " 🍝🍕"
            elif cuisine == "Mexican":
                cuisine_emoji = " 🌮"

            # Only show cuisine for restaurant type, and only if cuisine is present
            if type_val == "restaurant" and cuisine:
                cuisine_line = f"<b>Cuisine:</b> {cuisine}{cuisine_emoji}<br>"
            else:
                cuisine_line = ""

            # Card HTML for each city
            card_style = "border-radius:18px; box-shadow: 0 4px 16px rgba(0,0,0,0.10); border:1px solid #ffb6c1; background:{}; padding:1em; margin-bottom:1em; width: 100%; max-width: 350px; min-width: 220px; box-sizing: border-box;"
            card_html_houston = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4>{cuisine_line}<b>Notes:</b> {notes}<br><b>Parking:</b> {parking}{parking_emoji}{walk_emoji}</div>'
            card_html_phoenix = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4>{cuisine_line}<b>Notes:</b> {notes}</div>'
            card_html_atlanta = f'<div style="{card_style.format(card_color)}"><h4 style="margin-bottom:0.2em;">{name}{star_emoji}</h4><b>Notes:</b> {notes}<br><b>Seating:</b> {seating}</div>'
            # Alternate cards between left and right columns
            target_col = left_col if idx % 2 == 0 else right_col
            if selected_city == "Houston":
                target_col.markdown(card_html_houston, unsafe_allow_html=True)
            elif selected_city == "Phoenix":
                target_col.markdown(card_html_phoenix, unsafe_allow_html=True)
            elif selected_city == "Atlanta":
                target_col.markdown(card_html_atlanta, unsafe_allow_html=True)
    else:
        st.info("No restaurants found for this combination.")

