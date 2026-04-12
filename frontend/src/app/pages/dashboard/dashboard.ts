import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, NavigationEnd } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApplicationService } from '../../services/application';
import { Subscription, filter } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit, OnDestroy {
  applications: any[] = [];
  loading = false;
  error = '';
  searchQuery = '';
  private routerSub?: Subscription;

  constructor(
    private appService: ApplicationService,
    public auth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    if (!this.auth.isLoggedIn()) { this.router.navigate(['/login']); return; }
    this.loadApplications();
    // Перезагружать при каждом заходе на дашборд
    this.routerSub = this.router.events.pipe(
      filter(e => e instanceof NavigationEnd && e.url === '/dashboard')
    ).subscribe(() => this.loadApplications());
  }

  ngOnDestroy() {
    this.routerSub?.unsubscribe();
  }

  onSearch() {
    this.loadApplications(this.searchQuery);
  }

  loadApplications(search = '') {
    this.loading = true;
    this.appService.getApplications(search).subscribe({
      next: (data) => { this.applications = data; this.loading = false; this.cdr.detectChanges(); },
      error: () => { this.error = 'Ошибка загрузки заявок'; this.loading = false; this.cdr.detectChanges(); },
    });
  }

  approve(id: string) {
    this.appService.approveApplication(id).subscribe({
      next: (u) => this.replaceApp(u),
      error: () => { this.error = 'Ошибка при одобрении'; },
    });
  }

  reject(id: string) {
    this.appService.rejectApplication(id).subscribe({
      next: (u) => this.replaceApp(u),
      error: () => { this.error = 'Ошибка при отклонении'; },
    });
  }

  delete(id: string) {
    this.appService.deleteApplication(id).subscribe({
      next: () => { this.applications = this.applications.filter(a => a.id !== id); this.cdr.detectChanges(); },
      error: () => { this.error = 'Ошибка при удалении'; },
    });
  }

  private replaceApp(updated: any) {
    const idx = this.applications.findIndex(a => a.id === updated.id);
    if (idx !== -1) { this.applications[idx] = updated; this.applications = [...this.applications]; this.cdr.detectChanges(); }
  }

  getStatusLabel(s: string | null): string {
    return ({approved:'Одобрено', rejected:'Отклонено', pending:'На рассмотрении'} as any)[s ?? ''] ?? 'Новая';
  }

  getStatusClass(s: string | null): string {
    return ({approved:'status-approved', rejected:'status-rejected', pending:'status-pending'} as any)[s ?? ''] ?? 'status-new';
  }

  goToApply() { this.router.navigate(['/apply']); }
  logout() { this.auth.logout(); }
}
