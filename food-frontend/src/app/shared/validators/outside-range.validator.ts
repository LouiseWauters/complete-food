/* Value should be in given range */
import {AbstractControl, ValidationErrors, ValidatorFn} from "@angular/forms";

export function outsideRangeValidator(min: number, max: number): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const forbidden = !(min <= control.value && control.value <= max);
    return forbidden ? {outsideRange: {value: control.value}} : null;
  };
}
