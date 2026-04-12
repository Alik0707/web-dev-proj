import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API = 'http://localhost:8001/api';

@Injectable({ providedIn: 'root' })
export class SubsidyService {
  constructor(private http: HttpClient) {}

  getSubsidies(): Observable<any[]> {
    return this.http.get<any[]>(`${API}/subsidies/`);
  }
}
