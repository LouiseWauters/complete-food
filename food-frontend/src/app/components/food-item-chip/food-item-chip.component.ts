import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FoodItem} from "../../shared/models/food-item";
import {Router} from "@angular/router";

@Component({
  selector: 'app-food-item-chip',
  templateUrl: './food-item-chip.component.html',
  styleUrls: ['./food-item-chip.component.css']
})
export class FoodItemChipComponent implements OnInit {

  @Input() foodItem!: FoodItem;
  @Output() removeItem = new EventEmitter<string>();

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
  }

  remove() {
    this.removeItem.emit(this.foodItem.name);
  }

  goToRecipeLink() {
    if (this.foodItem.recipe_link) {
      window.open(this.foodItem.recipe_link, "_blank");
    }
  }

  goToFoodItemPage() {
    this.router.navigate([`food-item/${this.foodItem.id}`]);
  }

}
