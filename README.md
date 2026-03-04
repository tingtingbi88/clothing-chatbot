# Clothing Chatbot

A wardrobe and outfit helper with **two versions**:
- A TypeScript (Node/Express) CLI + web server
- A cute, pastel Streamlit (Python) app with weather and outfit suggestions

---

## Contents

- [Features](#features)
- [TypeScript Version](#typescript-version)
- [Streamlit Version](#streamlit-version)
- [CSV Format](#csv-format)
- [Customization](#customization)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- CSV-based wardrobe management
- CLI and web UI (TypeScript)
- Cute, pastel Streamlit web app (Python)
- Weather info and today’s date (Streamlit)
- Lottie animation (Streamlit)
- Dress disables bottoms logic (Streamlit)
- Outfit combinations and suggestions
- Easy to extend and customize

---

## TypeScript Version

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

## Streamlit Version

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

---

## CSV Format

The app expects a CSV file at  
`/Users/tingtingbi/Downloads/Clothes Inventory - 2026 Clothes.csv`  
with at least these columns:

```
Category,"Description (Brand)",Primary Color,Secondary Color,Type,Frequency
```

Example row:
```
Athletic,Lululemon green tank,Green,Not Applicable,Shirts,Weekly
```

You can edit the path in `app.py` if your CSV is elsewhere.

---

## Customization

- **Change the Lottie animation:**  
  Edit the `lottie_url` in `app.py` to use any [LottieFiles](https://lottiefiles.com/) animation you like.
- **Change the wardrobe CSV path:**  
  Edit the `csv_path` variable in `app.py`.
- **Change the city for weather:**  
  Edit the `city` variable in `app.py`.
- **Add more clothing types:**  
  Update the `tops_types` and `bottoms_types` lists in `app.py`.

---

## Screenshots

*(Add screenshots of both UIs here for extra cuteness!)*

---

## Contributing

Pull requests are welcome!  
Feel free to open issues for suggestions or bugs.

---

## License

MIT

---