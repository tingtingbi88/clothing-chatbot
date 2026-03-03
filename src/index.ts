// filepath: src/index.ts
import fs from "fs";
import csv from "csv-parser";
import express, { Request, Response } from "express";    // ← typed
import ChatBot from "./chatbot";
import prompt from "prompt-sync";

const input = prompt();
const csvPath =
  "/Users/tingtingbi/Downloads/Clothes Inventory - 2026 Clothes.csv";

console.log("starting up…");
console.log("looking for CSV at", csvPath);

fs.access(csvPath, fs.constants.R_OK, (err) => {
  if (err) {
    console.error("cannot read CSV file:", err.message);
    process.exit(1);
  }
});

interface ClothingItem {
  Category: string;
  "Description (Brand)": string;
  "Primary Color": string;
  "Secondary Color": string;
  Type: string;
  Frequency: string;
}

const normalise = (s: string) => s.trim().toLowerCase();

const clothingData: ClothingItem[] = [];
const categories = new Map<number, { id: number; name: string }>();
const colors = new Map<number, { id: number; name: string }>();
const types = new Map<number, { id: number; name: string }>();
const descriptions: { [key: string]: string[] } = {};
const readableCombos: string[] = [];

let categoryId = 1;
let colorId = 1;
let typeId = 1;

fs.createReadStream(csvPath)
  .on("error", (err) => {
    console.error("stream error:", err.message);
  })
  .pipe(csv())
  .on("data", (row: any) => {
    clothingData.push(row);
  })
  .on("end", () => {
    console.log("finished reading CSV – rows =", clothingData.length);

    clothingData.forEach((item) => {
      const catKey = normalise(item.Category);
      if (
        !Array.from(categories.values()).find(
          (c) => normalise(c.name) === catKey
        )
      ) {
        categories.set(categoryId, { id: categoryId, name: item.Category });
        categoryId++;
      }

      const colKey = normalise(item["Primary Color"]);
      if (
        !Array.from(colors.values()).find(
          (c) => normalise(c.name) === colKey
        )
      ) {
        colors.set(colorId, { id: colorId, name: item["Primary Color"] });
        colorId++;
      }

      const typeKey = normalise(item.Type);
      if (
        !Array.from(types.values()).find((t) => normalise(t.name) === typeKey)
      ) {
        types.set(typeId, { id: typeId, name: item.Type });
        typeId++;
      }

      const cat = Array.from(categories.values()).find(
        (c) => normalise(c.name) === catKey
      );
      const col = Array.from(colors.values()).find(
        (c) => normalise(c.name) === colKey
      );
      const typ = Array.from(types.values()).find(
        (t) => normalise(t.name) === typeKey
      );

      if (cat && col && typ) {
        const key = `${normalise(cat.name)}-${normalise(col.name)}-${normalise(
          typ.name
        )}`;
        const desc = item["Description (Brand)"].trim();
        if (!descriptions[key]) {
          descriptions[key] = [];
          readableCombos.push(`${cat.name}-${col.name}-${typ.name}`);
        }
        descriptions[key].push(desc);
      }
    });

    console.log("available combinations:", readableCombos.join(", "));

    const chatbot = new ChatBot(
      Array.from(categories.values()),
      Array.from(colors.values()),
      Array.from(types.values()),
      descriptions
    );

    // start web server
    const app = express();
    app.use(express.static("public"));

    app.get("/api/options", (req: Request, res: Response) => {
      res.json({
        categories: Array.from(categories.values()),
        colors: Array.from(colors.values()),
        types: Array.from(types.values()),
      });
    });

    app.get("/api/describe", (req: Request, res: Response) => {
      const cat = parseInt(req.query.cat as string);
      const col = parseInt(req.query.col as string);
      const ty = parseInt(req.query.type as string);
      const result = chatbot.getDescription(cat, col, ty);
      res.json(result);
    });

    app.listen(3000, () => {
      console.log("web UI available at http://localhost:3000");
    });

    // keep CLI prompt if you still want it
    console.log("\nWelcome to the Clothing Chatbot (CLI)!\n");
    console.log(
      "Categories:",
      Array.from(categories.values())
        .map((c) => `${c.id}=${c.name}`)
        .join(", ")
    );
    console.log(
      "Colors:",
      Array.from(colors.values())
        .map((c) => `${c.id}=${c.name}`)
        .join(", ")
    );
    console.log(
      "Types:",
      Array.from(types.values())
        .map((t) => `${t.id}=${t.name}`)
        .join(", ")
    );
    console.log();

    const categoryInput = parseInt(input("Select Category ID: "));
    const colorInput = parseInt(input("Select Color ID: "));
    const typeInput = parseInt(input("Select Type ID: "));

    const results = chatbot.getDescription(
      categoryInput,
      colorInput,
      typeInput
    );
    console.log("\nClothing Description(s):");
    results.forEach((r) => console.log(" -", r));
  });