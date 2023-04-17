import { Component, OnInit } from '@angular/core';
import {FoodItemService} from "../../shared/services/food-item.service";
import {FoodItem} from "../../shared/models/food-item";

@Component({
  selector: 'app-search-food',
  templateUrl: './search-food.component.html',
  styleUrls: ['./search-food.component.css']
})
export class SearchFoodComponent implements OnInit {

  foodItems: FoodItem[] | null = null;
  ready: boolean = false;

  constructor(
    private foodItemApi: FoodItemService
  ) { }

  ngOnInit(): void {
  }

  getFoodItems() : void {
    this.foodItemApi.getFoodItems()
      .subscribe(
        foodItems => {
          this.foodItems = foodItems;
          this.sortFoodItems();
          this.countVegetables();
          this.ready = true;
        }
      );
  }

  sortFoodItems() : void {
    this.foodItems?.sort((a, b) => a.name.localeCompare(b.name))
  }

  countVegetables() : void {
    if (this.foodItems) {
      this.foodItems.forEach(item => {
        if (item.base_food_items.length === 0) {
          item.vegetable_count = item.food_category === 'Vegetables' ? 1 : 0;
        } else {
          item.vegetable_count = this.foodItems?.filter(base =>
            item.base_food_items.includes(base.id) &&  // TODO this doesn't work because I need all fringe bases, not just bases
            base.base_food_items.length === 0 &&
            base.food_category === 'Vegetables'
          ).length
        }
      })
    }
  }

}
