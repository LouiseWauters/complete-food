import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {IngredientFormComponent} from "./components/ingredient-form/ingredient-form.component";
import {FoodItemFormComponent} from "./components/food-item-form/food-item-form.component";
import {FoodItemPageComponent} from "./components/food-item-page/food-item-page.component";

const routes: Routes = [
  { path: '', component: FoodItemFormComponent},
  { path: 'food-item/:id', component: FoodItemPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
