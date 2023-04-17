import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {outsideRangeValidator} from "../../shared/validators/outside-range.validator";
import {followRegexValidator} from "../../shared/validators/follow-regex.validator";
import {nonEmptyValidator} from "../../shared/validators/non-empty.validator";
import {MONTHS} from "../../shared/data/months";
import {Month} from "../../shared/models/month";
import {FoodItem} from "../../shared/models/food-item";
import {FoodCategory} from "../../shared/models/food-category";
import {FoodItemService} from "../../shared/services/food-item.service";
import {logMessages} from "@angular-devkit/build-angular/src/builders/browser-esbuild/esbuild";

@Component({
  selector: 'app-food-item-form',
  templateUrl: './food-item-form.component.html',
  styleUrls: ['./food-item-form.component.css']
})
export class FoodItemFormComponent implements OnInit {

  form!: FormGroup;
  basesForm!: FormGroup;
  errorMessage!: string | null;
  successMessage!: string | null;
  foodItems!: FoodItem[] | null;
  foodCategories!: FoodCategory[] | null;
  ready: boolean = false;
  bases: FoodItem[] = [];

  constructor(
    private foodItemApi: FoodItemService
  ) {
  }

  ngOnInit(): void {
    this.getFoodItems();
    this.getFoodCategories();
    this.form = new FormGroup({
      name: new FormControl(
        null,
        [
          Validators.required,
          Validators.minLength(2),
          followRegexValidator(/^[a-z A-Z]+$/),
          nonEmptyValidator()
        ]),
      is_full_meal: new FormControl(
        false
      ),
      is_health_rotation: new FormControl(
        false
      ),
      is_wfd: new FormControl(
        false
      ),
      season: new FormControl(
        null
      ),
      food_category_id: new FormControl(
        null
      ),
      recipe_link: new FormControl(
        null
      )
    })

    this.basesForm = new FormGroup({
      base_food_item_name: new FormControl(
        null
      )
    })
  }

  submit(newFoodItem: FoodItem) : void {
    this.clearMessage();
    newFoodItem.season = this.monthsToNumber(this.getSelectedMonths());
    if(this.form.valid) {
      this.foodItemApi.createFoodItem(newFoodItem)
        .subscribe({
          next: data => {
            this.successMessage = this.createSuccessMessage(data);
            // Reset form to be empty, excluding default value for is_vegetable
            this.form.reset({
              'is_full_meal': false,
              'is_wfd': false,
              'is_health_rotation': false
            })
            // Put cursor back in first input field of the form
            document.getElementById(`${this.className}Form`)?.firstElementChild?.getElementsByTagName("input")[0].focus();
            // Add newly created ingredient to our list of ingredients
            this.foodItems?.push(data);
            this.sortFoodItems();
            // Reset season buttons
            this.unselectAllMonths();
            // Make api calls for food extensions
            this.bases.forEach(base => this.foodItemApi.addBase(data, base).subscribe(data => console.log("gelukt!", data), error => this.errorMessage = 'Could not link base.'));
            this.bases = [];
          },
          error: error => {
            this.errorMessage = error.error;
          }
        });
    } else {
      console.log(this.name?.errors);
      if (this.name?.errors?.['required']) {
        this.errorMessage = "Name is required.";
      }
      if (this.name?.errors?.['minlength']) {
        this.errorMessage = "Name should be at least 2 characters long.";
      }
      if (this.name?.errors?.['followRegex']) {
        this.errorMessage = "Name should only contain letters.";
      }
      if (this.name?.errors?.['nonEmpty']) {
        this.errorMessage = "Name cannot be empty.";
      }
    }
  }

  createSuccessMessage(createdFoodItem: FoodItem) : string {
    let message = `Successfully created ingredient ${createdFoodItem.name}.`;
    return message
  }

  getFoodItems() : void {
    this.foodItemApi.getFoodItems()
      .subscribe(
        foodItems => {
          this.foodItems = foodItems;
          this.sortFoodItems();
          this.ready = this.foodCategories != null;
        }
      );
  }

  getFoodCategories() : void {
    this.foodItemApi.getFoodCategories()
      .subscribe(
        foodCategories => {
          this.foodCategories = foodCategories;
          this.sortFoodItems();
          this.ready = this.foodItems != null;
        }
      );
  }

  sortFoodItems() : void {
    this.foodItems?.sort((a, b) => a.name.localeCompare(b.name))
  }

  clearSelectedCategory() : void {
    this.form.controls['food_category_id'].setValue(null);
  }

  clearMessage() : void {
    this.errorMessage = null;
    this.successMessage = null;
  }

  clickSeason(month: string) : void {
    const seasonButton = document.getElementById(`${month}Button`);
    if (seasonButton?.classList.contains('is-primary')) {
      seasonButton.classList.remove('is-primary');
    } else {
      seasonButton?.classList.add('is-primary');
    }
  }

  unselectAllMonths() : void {
    const elems = document.getElementById("seasonButtons")?.getElementsByTagName("button");
    if (elems) {
      for (let i = 0; i < elems.length; i++) {
        elems[i].classList.remove('is-primary');
      }
    }
  }

  selectAllMonths() : void {
    const elems = document.getElementById("seasonButtons")?.getElementsByTagName("button");
    if (elems) {
      for (let i = 0; i < elems.length; i++) {
        elems[i].classList.add('is-primary');
      }
    }
  }

  getSelectedMonths(): Month[] {
    const monthIndices: number[] = [];
    const elems = document.getElementById("seasonButtons")?.getElementsByTagName("button");
    if (elems) {
      for (let i = 0; i < elems.length; i++) {
        if (elems[i].classList.contains('is-primary')) {
          monthIndices.push(i);
        }
      }
    }
    return MONTHS.filter(month => monthIndices.includes(month.index));
  }

  monthsToNumber(months: Month[]): number {
    // const monthIndices = months.map(month => month.index);
    // let season = 0;
    // monthIndices.forEach(i => season += (1 << i));
    return months.map(month => month.index).reduce((season, index) => season + (1 << index), 0);
  }

  addBase() {
    const baseFoodItemName = this.basesForm.controls['base_food_item_name'].value;
    if (!this.bases.map(item => item.name).includes(baseFoodItemName)) {
      const baseFoodItems = this.foodItems?.filter(item => item.name == baseFoodItemName);
      if (baseFoodItems && baseFoodItems.length > 0) {
        this.bases.push(baseFoodItems[0]);
      }
    }
    this.basesForm.controls['base_food_item_name'].setValue(null);
  }

  removeBase(baseName: string) {
    this.bases = this.bases.filter(base => base.name != baseName);
  }

  get name() {
    return this.form.get('name');
  }

  get months() {
    return MONTHS;
  }

  get className() {
    return this.constructor.name;
  }

}
