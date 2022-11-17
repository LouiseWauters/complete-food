import {AbstractControl, ValidationErrors, ValidatorFn} from "@angular/forms";

export function followRegexValidator(regex: RegExp): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const forbidden = !regex.test(control.value);
    return forbidden ? {followRegex: {value: control.value}} : null;
  };
}
