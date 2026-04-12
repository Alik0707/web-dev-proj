import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { BudgetService } from '../../services/budget';

@Component({
  selector: 'app-budget',
  imports: [FormsModule, CommonModule],
  templateUrl: './budget.html',
  styleUrl: './budget.css',
})
export class Budget implements OnInit {
  budgets: any[] = [];
  loading = false;
  error = '';
  editingId: number | null = null;
  editValue: number | null = null;

  constructor(
    private budgetService: BudgetService,
    public auth: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }
    this.loadBudgets();
  }

  loadBudgets() {
    this.loading = true;
    this.budgetService.getBudgets().subscribe({
      next: (data) => { this.budgets = data; this.loading = false; },
      error: () => { this.error = 'Ошибка загрузки бюджетов'; this.loading = false; },
    });
  }

  startEdit(budget: any) {
    this.editingId = budget.id;
    this.editValue = budget.allocated_budget;
  }

  saveEdit(id: number) {
    if (this.editValue === null) return;
    this.budgetService.updateBudget(id, this.editValue).subscribe({
      next: (updated) => {
        const idx = this.budgets.findIndex(b => b.id === id);
        if (idx !== -1) this.budgets[idx] = updated;
        this.editingId = null;
      },
      error: () => { this.error = 'Ошибка при сохранении'; },
    });
  }

  cancelEdit() {
    this.editingId = null;
    this.editValue = null;
  }

  goToDashboard() {
    this.router.navigate(['/dashboard']);
  }

  logout() {
    this.auth.logout();
  }

  getTotalBudget(): number {
    return this.budgets.reduce((sum, b) => sum + Number(b.allocated_budget), 0);
  }
}
