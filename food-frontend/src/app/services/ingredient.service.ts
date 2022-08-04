import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Ingredient} from "../models/ingredient";
import {API_URL} from "../env";

@Injectable({
  providedIn: 'root'
})
export class IngredientService {

  constructor(
    private http: HttpClient
  ) { }

  createIngredient(newIngredient: Ingredient) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    const body = JSON.stringify(newIngredient);
    return this.http.post<Ingredient>(`${API_URL}/ingredients`, body, httpOptions);
  }
}
