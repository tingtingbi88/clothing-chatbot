export default class ChatBot {
    private categories: Array<{ id: number; name: string }>;
    private colors: Array<{ id: number; name: string }>;
    private types: Array<{ id: number; name: string }>;
    // now an array of strings for each key
    private descriptions: { [key: string]: string[] };

    constructor(
        categories: Array<{ id: number; name: string }>,
        colors: Array<{ id: number; name: string }>,
        types: Array<{ id: number; name: string }>,
        descriptions: { [key: string]: string[] }
    ) {
        this.categories = categories;
        this.colors = colors;
        this.types = types;
        this.descriptions = descriptions;
    }

    selectCategory(id: number) {
        return this.categories.find(category => category.id === id);
    }

    selectColor(id: number) {
        return this.colors.find(color => color.id === id);
    }

    selectType(id: number) {
        return this.types.find(type => type.id === id);
    }

    private normalise(s: string) {
        return s.trim().toLowerCase();
    }

    getDescription(categoryId: number, colorId: number, typeId: number) {
        const category = this.selectCategory(categoryId);
        const color = this.selectColor(colorId);
        const type = this.selectType(typeId);
        if (!category || !color || !type) {
            return ["Invalid selection."];
        }
        const key = `${this.normalise(category.name)}-${this.normalise(
            color.name
        )}-${this.normalise(type.name)}`;
        return this.descriptions[key] || ["Description not found."];
    }
}