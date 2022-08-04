import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {Ingredient} from "../models/ingredient";
import {outsideRangeValidator} from "../shared/outside-range-validator.directive";
import {followRegexValidator} from "../shared/follow-regex-validator.directive";
import {nonEmptyValidator} from "../shared/non-empty-validator.directive";

@Component({
  selector: 'app-ingredient-form',
  templateUrl: './ingredient-form.component.html',
  styleUrls: ['./ingredient-form.component.css']
})
export class IngredientFormComponent implements OnInit {

  form!: FormGroup;
  errorMessage!: string | null;

  constructor() {
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

  submit(form: Ingredient) {
    this.errorMessage = null;
    if(this.form.valid) {
      console.log(form);
      this.form.reset();
      this.form.markAsPristine();
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

}
