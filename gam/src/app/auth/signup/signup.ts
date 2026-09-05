import { Component, inject } from '@angular/core';
import { RouterLink,Router } from '@angular/router';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { environment } from '../../environment';


interface SignupResponse {
  message?: string;
  access_token?: string;
}


@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [RouterLink, ReactiveFormsModule],
  templateUrl: './signup.html',
  styleUrl: './signup.scss',
})
export class Signup {
  private http = inject(HttpClient);
  private router = inject(Router);

  form = new FormGroup({
    email: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.email] }),
    password: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.minLength(4)] }),
  });

  /** Feedback state shown in the template */
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  /** Shorthand getters for cleaner template access */
  get email() { return this.form.get('email')!; }
  get password() { return this.form.get('password')!; }

  async onSignup(): Promise<void> {
    // if (this.form.invalid) return;
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage = '';
    this.successMessage = '';
    this.isLoading = true;

    try {
      const response = await firstValueFrom(
        this.http.post<SignupResponse>(`${environment.apiBaseUrl}/auth/createAccount`, {
          email: this.email.value,
          password: this.password.value,
        })
      );

      console.log('Signup successful:', response);
      this.successMessage = 'Account created! Please check your email.';

      // TODO: navigate to login or dashboard after signup
      this.form.reset();
      if(response){
        this.router.navigate(['/checkEmail']);
      }

    } catch (error: any) {
      console.error('Signup failed:', error);
      // this.errorMessage =
      //   error?.error?.detail ?? 'Signup failed. Please try again.';
      if (error instanceof HttpErrorResponse) {
        const detail = error.error?.detail;
        this.errorMessage = typeof detail === 'string' ? detail : 'Signup failed. Please try again.';
      }
      else {
        this.errorMessage = 'An unexpected error occurred. Please try again.';
      }
    } 
    finally {
      this.isLoading = false;
    }
  }
}
