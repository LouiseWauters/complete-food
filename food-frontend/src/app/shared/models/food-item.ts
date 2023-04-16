export interface FoodItem {
  id: number;
  name: string;
  last_eaten: Date;
  times_eaten: number;
  is_full_meal: boolean;
  is_wfd: boolean;
  is_health_rotation: boolean;
  season: number;
  food_category_id: number;
  food_category: string;
  recipe_link: string;
  base_food_items: number[];
  extension_food_items: number[];
  vegetable_count?: number;
}
