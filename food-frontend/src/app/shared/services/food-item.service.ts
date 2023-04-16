import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {API_URL} from "../../env";
import {FoodItem} from "../models/food-item";
import {FoodCategory} from "../models/food-category";

@Injectable({
  providedIn: 'root'
})
export class FoodItemService {

  constructor(
    private http: HttpClient
  ) { }

  getFoodItems(): Observable<FoodItem[]> {
    return this.http.get<FoodItem[]>(`${API_URL}/food-items`);
  }

  getFoodItemById(id: number): Observable<FoodItem> {
    return this.http.get<FoodItem>(`${API_URL}/food-items/${id}`);
  }

  getFoodCategories(): Observable<FoodCategory[]> {
    return this.http.get<FoodCategory[]>(`${API_URL}/food-categories`);
  }

  getAllFoodItemBases(foodItemId: number): Observable<FoodItem[]> {
    return this.http.get<FoodItem[]>(`${API_URL}/food-items/${foodItemId}/all-bases`);
  }

  getAllFoodItemExtensions(foodItemId: number): Observable<FoodItem[]> {
    return this.http.get<FoodItem[]>(`${API_URL}/food-items/${foodItemId}/all-extensions`);
  }

  createFoodItem(newFoodItem: FoodItem) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    const body = JSON.stringify(newFoodItem);
    return this.http.post<FoodItem>(`${API_URL}/food-items`, body, httpOptions);
  }

  addBase(originalFoodItem: FoodItem, baseFoodItem: FoodItem) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<any>(`${API_URL}/food-items/${baseFoodItem.id}/extensions/${originalFoodItem.id}`, httpOptions);
  }
}
