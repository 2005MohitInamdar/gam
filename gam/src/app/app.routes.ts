import { Routes } from '@angular/router';
import { Login } from './auth/login/login';
import { Signup } from './auth/signup/signup';
import { CheckEmail } from './auth/check-email/check-email'; 
import { Dashboard } from './components/dashboard/dashboard';
import { NewFraudCase } from './components/new-fraud-case/new-fraud-case';
export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'signup', component: Signup },
  { path: 'checkEmail', component: CheckEmail },
  { path: 'dashboard', component: Dashboard },
  { path: 'newFraudCase', component: NewFraudCase }
];
