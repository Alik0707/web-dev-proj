from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # FBV
    path('login/', views.login_view, name='login'),
    path('submit/', views.submit_application, name='submit'),

    # CBV
    path('applications/', views.ApplicationListView.as_view(), name='applications'),
    path('applications/<str:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('budget/', views.BudgetListView.as_view(), name='budget'),
    path('budget/<int:pk>/', views.BudgetListView.as_view(), name='budget-detail'),

    path('subsidies/', views.SubsidyListView.as_view(), name='subsidies'),

    # JWT refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
