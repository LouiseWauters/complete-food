export interface Ingredient {
  id: number;
  name: string;
  rating: number;
  last_eaten: Date;
  is_vegetable: boolean;
  base_ingredient_id: number;
  base_ingredient?: Ingredient;
}
