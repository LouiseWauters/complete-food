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

  constructor(
    private ingredientApi: IngredientService
  ) {
  }

  ngOnInit(): void {
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
        ])
    })
  }

  submit(newIngredient: Ingredient) {
    this.errorMessage = null;
    this.successMessage = null;
    if(this.form.valid) {
      console.log(newIngredient);
      this.ingredientApi.createIngredient(newIngredient)
        .subscribe({
          next: data => {
            this.successMessage = `Successfully created ingredient ${data.name} with rating ${data.rating}.`;
            // Reset form to be empty
            this.form.reset();
            this.form.markAsPristine();
            // Put cursor back in first input field of the form
            document.getElementById(`${this.className}Form`)?.firstElementChild?.getElementsByTagName("input")[0].focus();
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
