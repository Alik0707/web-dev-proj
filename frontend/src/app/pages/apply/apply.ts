import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApplicationService } from '../../services/application';
import { SubsidyService } from '../../services/subsidy';

@Component({
  selector: 'app-apply',
  imports: [FormsModule, CommonModule],
  templateUrl: './apply.html',
  styleUrl: './apply.css',
})
export class Apply implements OnInit {
  currentStep = 1;
  submitting = false;
  error = '';
  submitted = false;
  result: any = null;

  // Step 1
  dateReceived = '';
  regionCode = '';
  akimat = '';
  pastureType = '';

  // Step 2
  subsidies: any[] = [];
  selectedSubsidy: any = null;
  subsidyId = '';

  // Step 3
  quantity: number | null = null;
  get amountRequested(): number {
    if (!this.selectedSubsidy || !this.quantity) return 0;
    return this.selectedSubsidy.normative * this.quantity;
  }

  regionAkimat: Record<string, string> = {
    'Абайская область': 'ГУ "Управление сельского хозяйства области Абай"',
    'Акмолинская область': 'ГУ "Управление сельского хозяйства и земельных отношений Акмолинской области"',
    'Актюбинская область': 'ГУ "Управление сельского хозяйства и земельных отношений Актюбинской области"',
    'Алматинская область': 'ГУ "Управление сельского хозяйства Алматинской области"',
    'Атырауская область': 'ГУ "Управление сельского хозяйства и земельных отношений Атырауской области"',
    'Восточно-Казахстанская область': 'ГУ "Управление сельского хозяйства Восточно-Казахстанской области"',
    'Жамбылская область': 'КГУ "Управление сельского хозяйства акимата Жамбылской области"',
    'Жетысуская область': 'ГУ "Управление сельского хозяйства области Жетісу"',
    'Западно-Казахстанская область': 'ГУ "Управление сельского хозяйства Западно-Казахстанской области"',
    'Карагандинская область': 'ГУ "Управление сельского хозяйства и земельных отношений Карагандинской области"',
    'Костанайская область': 'ГУ "Управление сельского хозяйства и земельных отношений акимата Костанайской области"',
    'Кызылординская область': 'ГУ "Управление сельского хозяйства Кызылординской области"',
    'Мангистауская область': 'ГУ "Управление сельского хозяйства Мангистауской области"',
    'Павлодарская область': 'ГУ "Управление сельского хозяйства Павлодарской области"',
    'Северо-Казахстанская область': 'КГУ "Управление сельского хозяйства и земельных отношений акимата Северо-Казахстанской области"',
    'Туркестанская область': 'ГУ "Управление сельского хозяйства Туркестанской области"',
    'Улытауская область': 'ГУ "Управление сельского хозяйства и земельных отношений области Ұлытау"',
  };
  get regions() { return Object.keys(this.regionAkimat); }

  pastureTypes = [
    'Умеренно-засушливая степь', 'Засушливая степь', 'Умеренно-сухая степь',
    'Сухая степь', 'Опустыненная степь', 'Остепненная пустыня (полупустыня)',
    'Настоящая (средняя) пустыня', 'Предгорья', 'Горные пастбища',
  ];

  constructor(
    private appService: ApplicationService,
    private subsidyService: SubsidyService,
    public auth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    if (!this.auth.isLoggedIn()) { this.router.navigate(['/login']); return; }
    this.subsidyService.getSubsidies().subscribe({
      next: (data) => this.subsidies = data,
      error: () => this.error = 'Ошибка загрузки субсидий',
    });
  }

  onRegionChange() {
    this.akimat = this.regionAkimat[this.regionCode] ?? '';
  }

  onSubsidyChange() {
    this.selectedSubsidy = this.subsidies.find(s => s.id === this.subsidyId) ?? null;
  }

  isStepValid(): boolean {
    switch (this.currentStep) {
      case 1: return !!(this.dateReceived && this.regionCode && this.pastureType);
      case 2: return !!(this.subsidyId && this.selectedSubsidy);
      case 3: return !!(this.quantity && this.quantity > 0);
      default: return false;
    }
  }

  nextStep() {
    if (this.currentStep < 3) this.currentStep++;
    else this.onSubmit();
  }

  prevStep() {
    if (this.currentStep > 1) this.currentStep--;
    else this.router.navigate(['/dashboard']);
  }

  onSubmit() {
    this.submitting = true;
    this.error = '';
    this.appService.submitApplication({
      date_received: this.dateReceived,
      region_code: this.regionCode,
      akimat: this.akimat,
      district: this.pastureType,
      subsidy_name: this.selectedSubsidy?.name ?? '',
      crop_type: this.selectedSubsidy?.direction ?? '',
      direction: this.selectedSubsidy?.direction ?? '',
      amount_norm: this.selectedSubsidy?.normative ?? 0,
      amount_requested: this.amountRequested,
    }).subscribe({
      next: (res) => { this.result = res; this.submitted = true; this.submitting = false; this.cdr.detectChanges(); },
      error: () => { this.error = 'Ошибка при подаче заявки'; this.submitting = false; },
    });
  }

  goToDashboard() { this.router.navigate(['/dashboard']); }
  logout() { this.auth.logout(); }

  getScoreClass(score: number): string {
    if (score >= 80) return 'score-high';
    if (score >= 55) return 'score-mid';
    return 'score-low';
  }

  getScoreLabel(score: number): string {
    if (score >= 80) return 'Высокий приоритет';
    if (score >= 55) return 'Средний приоритет';
    return 'Низкий приоритет';
  }
}
