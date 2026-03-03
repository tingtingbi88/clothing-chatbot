# clothing‑chatbot

Small TypeScript project that reads a CSV of clothes and lets you look
up a description by category / colour / type.  It can be used from the
command line **and** via a tiny web page.

## Install

```bash
npm install
```

## Usage

### Command‑line

The same command that starts the web server also runs the CLI prompts.

```bash
npm start      # runs ts-node src/index.ts
```

After the CSV has been read you’ll see the available categories, colours
and types printed to the terminal, then you’ll be asked to enter three
numeric IDs.  Enter them and press Enter to get a description.

You can keep using the CLI even when the web UI is running; just cancel
the process with **Ctrl‑C** when you’re done.

### Web UI

A tiny Express server is started by `npm start`.  
Open your browser at [http://localhost:3000](http://localhost:3000) and
you’ll get a simple page with three dropdowns and a **Describe** button.

The page uses two API endpoints:

* **`/api/options`** – returns the lists of categories, colours and types.
* **`/api/describe?cat=…&col=…&type=…`** – returns one or more
  descriptions matching the selected combination.

You can style or extend the HTML in `public/index.html`, or replace it
with a more sophisticated front‑end if you like.

## CSV format

The code expects a file at the path configured in
`src/index.ts` (currently
`/Users/tingtingbi/Downloads/Clothes Inventory - 2026 Clothes.csv`).
Adjust that path or move your CSV if necessary.

The CSV must have these headers (only the first three are used):

```
Category,"Description (Brand)",Primary Color,Secondary Color,Type,Frequency
```

Any number of rows may be present; rows with the same category/colour/type
will all be returned by the chatbot.

## Development

* The project uses `ts-node` – modify files under `src/` and rerun
  `npm start` to see changes.
* Add or edit rows in the CSV and restart `npm start` to pick them up.
* To stop the server, press **Ctrl‑C** in the terminal where it’s running.
* Commit your changes and push to your GitHub repository as usual.

Feel free to expand this README further with screenshots, build
instructions, or deployment notes if you publish the app somewhere.
```// filepath: README.md
# clothing‑chatbot

Small TypeScript project that reads a CSV of clothes and lets you look
up a description by category / colour / type.  It can be used from the
command line **and** via a tiny web page.

## Install

```bash
npm install
```

## Usage

### Command‑line

The same command that starts the web server also runs the CLI prompts.

```bash
npm start      # runs ts-node src/index.ts
```

After the CSV has been read you’ll see the available categories, colours
and types printed to the terminal, then you’ll be asked to enter three
numeric IDs.  Enter them and press Enter to get a description.

You can keep using the CLI even when the web UI is running; just cancel
the process with **Ctrl‑C** when you’re done.

### Web UI

A tiny Express server is started by `npm start`.  
Open your browser at [http://localhost:3000](http://localhost:3000) and
you’ll get a simple page with three dropdowns and a **Describe** button.

The page uses two API endpoints:

* **`/api/options`** – returns the lists of categories, colours and types.
* **`/api/describe?cat=…&col=…&type=…`** – returns one or more
  descriptions matching the selected combination.

You can style or extend the HTML in `public/index.html`, or replace it
with a more sophisticated front‑end if you like.

## CSV format

The code expects a file at the path configured in
`src/index.ts` (currently
`/Users/tingtingbi/Downloads/Clothes Inventory - 2026 Clothes.csv`).
Adjust that path or move your CSV if necessary.

The CSV must have these headers (only the first three are used):

```
Category,"Description (Brand)",Primary Color,Secondary Color,Type,Frequency
```

Any number of rows may be present; rows with the same category/colour/type
will all be returned by the chatbot.

## Development

* The project uses `ts-node` – modify files under `src/` and rerun
  `npm start` to see changes.
* Add or edit rows in the CSV and restart `npm start` to pick them up.
* To stop the server, press **Ctrl‑C** in the terminal where it’s running.
* Commit your changes and push to your GitHub repository as usual.

Feel free to expand this README further with screenshots, build
instructions, or deployment notes if you publish the app somewhere.