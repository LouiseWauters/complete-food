import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FoodItemPageComponent } from './food-item-page.component';

describe('FoodItemPageComponent', () => {
  let component: FoodItemPageComponent;
  let fixture: ComponentFixture<FoodItemPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FoodItemPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FoodItemPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
