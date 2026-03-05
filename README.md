# Clothing & Restaurant Apps

This repo contains three main apps:

1. **Clothing Chatbot (TypeScript)** – CLI and web server for wardrobe management
2. **Clothing Chatbot (Streamlit)** – Pastel-themed Python app for outfit suggestions
3. **Houston Restaurant Recommender (Streamlit)** – Restaurant explorer for Houston & Phoenix

---


## 1. Clothing Chatbot (TypeScript)

**Features:**
- CSV-based wardrobe management
- CLI and web UI (Node/Express)
- Easy to extend and customize

**Setup:**
```bash
npm install
```

**Run CLI + Express web server:**
```bash
npm start
```
- Visit [http://localhost:3000](http://localhost:3000) for the web UI.
- Use the CLI in your terminal as prompted.

---



## 2. Clothing Chatbot (Streamlit)

**Features:**
- Cute, pastel Streamlit web app (Python)
- Weather info and today’s date
- Lottie animation
- Dress disables bottoms logic
- Outfit combinations and suggestions

**Install dependencies:**
```bash
pip install -r requirements.txt
pip install streamlit streamlit-lottie pandas requests
```

**Set up pastel theme:**
Create `.streamlit/config.toml` in your project root:
```toml
[theme]
primaryColor = "#FFB6C1"
backgroundColor = "#FFF0F5"
secondaryBackgroundColor = "#FDEEF4"
textColor = "#4B2E83"
font = "sans serif"
```

**Get a weather API key:**
Sign up at [OpenWeatherMap](https://openweathermap.org/api) and add your key to `app.py`.

**Run the app:**
```bash
streamlit run app.py
```
- Opens in your browser at [http://localhost:8501](http://localhost:8501)
- Lottie animation, weather, date, and outfit selection

**CSV Format:**
The app expects a CSV file at `/Users/tingtingbi/Downloads/Clothes Inventory - 2026 Clothes.csv` with at least these columns:
```
Category,"Description (Brand)",Primary Color,Secondary Color,Type,Frequency
```
Example row:
```
Athletic,Lululemon green tank,Green,Not Applicable,Shirts,Weekly
```
You can edit the path in `app.py` if your CSV is elsewhere.

**Customization:**
- Change the Lottie animation: edit `lottie_url` in `app.py`
- Change the wardrobe CSV path: edit `csv_path` in `app.py`
- Change the city for weather: edit `city` in `app.py`
- Add more clothing types: update `tops_types` and `bottoms_types` in `app.py`

---

## 3. Houston Restaurant Recommender (Streamlit)

**houston_restaurants_app.py** is a Streamlit app for exploring and recommending restaurants in Houston and Phoenix.

**Features:**
- City selection (Houston or Phoenix)
- Dynamic filters for location, type, cost, and cuisine
- Emoji-rich UI and two-column card layout
- Favorites/go-tos and color-coded cards

**Install dependencies:**
```bash
pip install -r requirements.txt
pip install streamlit pandas
```

**Run the app:**
```bash
streamlit run houston_restaurants_app.py
```
- Opens in your browser at [http://localhost:8501](http://localhost:8501)
- Requires CSV files: `Houston_Restaurants.csv` and `Arizona_Restaurants.csv` in your Downloads folder

---

