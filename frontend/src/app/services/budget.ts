import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API = 'http://localhost:8001/api';

@Injectable({ providedIn: 'root' })
export class BudgetService {
  constructor(private http: HttpClient) {}

  getBudgets(): Observable<any[]> {
    return this.http.get<any[]>(`${API}/budget/`);
  }

  updateBudget(id: number, allocated_budget: number): Observable<any> {
    return this.http.patch<any>(`${API}/budget/${id}/`, { allocated_budget });
  }
}
