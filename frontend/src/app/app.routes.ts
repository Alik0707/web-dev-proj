import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Dashboard } from './pages/dashboard/dashboard';
import { Apply } from './pages/apply/apply';
import { Budget } from './pages/budget/budget';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'dashboard', component: Dashboard },
  { path: 'apply', component: Apply },
  { path: 'budget', component: Budget },
  { path: '**', redirectTo: '/login' },
];
