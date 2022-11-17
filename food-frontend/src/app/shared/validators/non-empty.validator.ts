import {AbstractControl, ValidationErrors, ValidatorFn} from "@angular/forms";

export function nonEmptyValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    return control.value?.trim()?.length == 0 ? {nonEmpty: {value: control.value}} : null;
  };
}
