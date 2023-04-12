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
  allBaseItems: FoodItem[] | null = null; // TODO change to extensions!

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private foodItemApi: FoodItemService
  ) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.allBaseItems = null;
        this.foodItem = null;
        this.ngOnInit();
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
        });
      }, error => this.router.navigate(['']));
    } else {
      this.router.navigate(['']);
    }
  }

}
