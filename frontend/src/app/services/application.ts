import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API = 'http://localhost:8001/api';

@Injectable({ providedIn: 'root' })
export class ApplicationService {
  constructor(private http: HttpClient) {}

  getApplications(search = ''): Observable<any[]> {
    const params = search ? `?search=${encodeURIComponent(search)}` : '';
    return this.http.get<any[]>(`${API}/applications/${params}`);
  }

  submitApplication(data: any): Observable<any> {
    return this.http.post<any>(`${API}/submit/`, data);
  }

  approveApplication(id: string, comment: string = ''): Observable<any> {
    return this.http.patch<any>(`${API}/applications/${id}/`, { action: 'approve', comment });
  }

  rejectApplication(id: string, comment: string = ''): Observable<any> {
    return this.http.patch<any>(`${API}/applications/${id}/`, { action: 'reject', comment });
  }

  deleteApplication(id: string): Observable<any> {
    return this.http.delete<any>(`${API}/applications/${id}/`);
  }
}
