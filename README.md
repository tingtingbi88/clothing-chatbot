# Clothing Chatbot

This project is a chatbot application that allows users to select clothing categories, primary colors, and types to receive descriptions of clothing items. 

## Project Structure

```
clothing-chatbot
├── src
│   ├── index.ts          # Entry point of the application
│   ├── chatbot.ts        # ChatBot class with selection methods
│   ├── categories        # Contains clothing categories
│   │   └── index.ts
│   ├── colors            # Contains primary colors
│   │   └── index.ts
│   ├── types             # Defines types and interfaces for clothing
│   │   ├── clothing.ts
│   │   └── index.ts
│   └── descriptions      # Maps combinations to clothing descriptions
│       └── index.ts
├── package.json          # npm configuration file
├── tsconfig.json         # TypeScript configuration file
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd clothing-chatbot
   ```
3. Install the dependencies:
   ```
   npm install
   ```

## Usage

To run the chatbot, execute the following command:
```
npm start
```

Follow the prompts to select a category, primary color, and type of clothing. The chatbot will then provide a description based on your selections.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.