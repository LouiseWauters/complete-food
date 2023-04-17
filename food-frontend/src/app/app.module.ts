import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { IngredientFormComponent } from './components/ingredient-form/ingredient-form.component';
import {ReactiveFormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";
import { LoadSpinnerComponent } from './components/load-spinner/load-spinner.component';
import {FoodItemFormComponent} from "./components/food-item-form/food-item-form.component";
import { FoodItemChipComponent } from './components/food-item-chip/food-item-chip.component';
import { FoodItemPageComponent } from './components/food-item-page/food-item-page.component';
import { SearchFoodComponent } from './components/search-food/search-food.component';

@NgModule({
  declarations: [
    AppComponent,
    IngredientFormComponent,
    LoadSpinnerComponent,
    FoodItemFormComponent,
    FoodItemChipComponent,
    FoodItemPageComponent,
    SearchFoodComponent
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        ReactiveFormsModule,
        HttpClientModule
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
