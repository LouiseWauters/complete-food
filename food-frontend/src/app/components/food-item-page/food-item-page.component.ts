import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, NavigationEnd, Router} from "@angular/router";
import {FoodItemService} from "../../shared/services/food-item.service";
import {FoodItem} from "../../shared/models/food-item";

@Component({
  selector: 'app-food-item-page',
  templateUrl: './food-item-page.component.html',
  styleUrls: ['./food-item-page.component.css']
})
export class FoodItemPageComponent implements OnInit {

  foodItem: FoodItem | null = null;
  allBaseItems: FoodItem[] | null = null;
  allExtensionItems: FoodItem[] | null = null;
  ready: boolean = false;
  onlyShowFringe: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private foodItemApi: FoodItemService
  ) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        const foodItemId = this.route.snapshot.paramMap.get('id');
        if (foodItemId && this.foodItem && +foodItemId !== this.foodItem.id) {
          this.allExtensionItems = null;
          this.allBaseItems = null;
          this.foodItem = null;
          this.ready = false;
          this.ngOnInit();
        }
      }
    })
  }

  ngOnInit(): void {
    const foodItemId = this.route.snapshot.paramMap.get('id');
    if (foodItemId) {
      this.foodItemApi.getFoodItemById(+foodItemId).subscribe(data => {
        this.foodItem = data;
        this.foodItemApi.getAllFoodItemBases(this.foodItem.id).subscribe(bases => {
          this.allBaseItems = bases;
          this.countVegetables();
          this.foodItemApi.getAllFoodItemExtensions(+foodItemId).subscribe(extensions => {
            this.allExtensionItems = extensions;
            this.ready = true;
          })
        });
      }, error => this.router.navigate(['']));
    } else {
      this.router.navigate(['']);
    }
  }

  clickFringe(): void {
    this.onlyShowFringe = !this.onlyShowFringe;
  }

  countVegetables(): void {
    if (this.foodItem && this.allBaseItems) {
      if (this.foodItem.base_food_items.length === 0) {
        this.foodItem.vegetable_count = this.foodItem.food_category === 'Vegetables' ? 1 : 0;
      } else {
        this.foodItem.vegetable_count = this.allBaseItems.filter(base =>
          base.base_food_items.length === 0 && base.food_category === 'Vegetables'
        ).length
      }
    }
  }

  openExtensionsInTabs(): void {
    if (this.allExtensionItems) {
      this.allExtensionItems.forEach(item => {
        if (!this.onlyShowFringe || item.extension_food_items.length === 0) {
          window.open(`food-item/${item.id}`, "_blank");
        }
      })
    }
  }

}
