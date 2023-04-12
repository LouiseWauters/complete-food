import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FoodItemFormComponent } from './food-item-form.component';

describe('IngredientFormComponent', () => {
  let component: FoodItemFormComponent;
  let fixture: ComponentFixture<FoodItemFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FoodItemFormComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FoodItemFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
