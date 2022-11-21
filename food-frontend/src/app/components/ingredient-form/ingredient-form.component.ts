import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {Ingredient} from "../../shared/models/ingredient";
import {outsideRangeValidator} from "../../shared/validators/outside-range.validator";
import {followRegexValidator} from "../../shared/validators/follow-regex.validator";
import {nonEmptyValidator} from "../../shared/validators/non-empty.validator";
import {IngredientService} from "../../shared/services/ingredient.service";

@Component({
  selector: 'app-ingredient-form',
  templateUrl: './ingredient-form.component.html',
  styleUrls: ['./ingredient-form.component.css']
})
export class IngredientFormComponent implements OnInit {

  form!: FormGroup;
  errorMessage!: string | null;
  successMessage!: string | null;
  ingredients!: Ingredient[] | null;
  ready = false;

  constructor(
    private ingredientApi: IngredientService
  ) {
  }

  ngOnInit(): void {
    this.getIngredients();
    this.form = new FormGroup({
      name: new FormControl(
        null,
        [
          Validators.required,
          Validators.minLength(2),
          followRegexValidator(/^[a-z A-Z]+$/),
          nonEmptyValidator()
        ]),
      rating: new FormControl(
        null,
        [
          Validators.required,
          outsideRangeValidator(0, 10)
        ]),
      is_vegetable: new FormControl(
        false
      ),
      base_ingredient_id: new FormControl(
        null
      )
    })
  }

  submit(newIngredient: Ingredient) : void {
    this.errorMessage = null;
    this.successMessage = null;
    if(this.form.valid) {
      console.log(newIngredient);
      this.ingredientApi.createIngredient(newIngredient)
        .subscribe({
          next: data => {
            this.successMessage = this.createSuccessMessage(data);
            // Reset form to be empty, excluding default value for is_vegetable
            this.form.reset({'is_vegetable': false});
            // Put cursor back in first input field of the form
            document.getElementById(`${this.className}Form`)?.firstElementChild?.getElementsByTagName("input")[0].focus();
            // Add newly created ingredient to our list of ingredients
            this.ingredients?.push(data);
            this.sortIngredients();
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
      if (this.rating?.errors?.['required']) {
        this.errorMessage = "Rating is required.";
      }
      if (this.rating?.errors?.['outsideRange']) {
        this.errorMessage = "Rating must be in range [0, 10].";
      }
    }
  }

  createSuccessMessage(createdIngredient: Ingredient) : string {
    let message = `Successfully created ingredient ${createdIngredient.name} with rating ${createdIngredient.rating} (`;
    if (!createdIngredient.is_vegetable) {
      message = message.concat('not a ');
    }
    message = message.concat('vegetable, ');
    if (createdIngredient.base_ingredient_id) {
      const base_ingredient_name = this.ingredients?.find(obj => {
        return obj.id === createdIngredient.base_ingredient_id
      })?.name;
      message = message.concat(`specification of ${base_ingredient_name}).`);
    } else {
      message = message.concat('not a specification).')
    }
    return message
  }

  getIngredients() : void {
    this.ingredientApi.getIngredients()
      .subscribe(
        ingredients => {
          this.ingredients = ingredients;
          this.sortIngredients();
          this.ready = true;
        }
      );
  }

  sortIngredients() : void {
    this.ingredients?.sort((a, b) => a.name.localeCompare(b.name))
  }

  clearSelected() : void {
    this.form.controls['base_ingredient_id'].setValue(null);
  }

  get name() {
    return this.form.get('name');
  }

  get rating() {
    return this.form.get('rating');
  }

  get className() {
    return this.constructor.name;
  }

}
