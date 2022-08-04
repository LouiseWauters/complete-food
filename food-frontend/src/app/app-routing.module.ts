import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {IngredientFormComponent} from "./ingredient-form/ingredient-form.component";

const routes: Routes = [
  { path: '', component: IngredientFormComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
