import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FoodItemChipComponent } from './food-item-chip.component';

describe('FoodItemChipComponent', () => {
  let component: FoodItemChipComponent;
  let fixture: ComponentFixture<FoodItemChipComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FoodItemChipComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FoodItemChipComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
