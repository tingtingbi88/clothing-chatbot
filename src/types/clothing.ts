export interface ClothingItem {
    id: string;
    category: string;
    color: string;
    type: string;
    description: string;
}

export interface ClothingCategory {
    id: string;
    name: string;
}

export interface PrimaryColor {
    id: string;
    name: string;
}

export interface ClothingType {
    id: string;
    name: string;
}