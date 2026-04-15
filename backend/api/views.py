import uuid
import hashlib
import requests
from datetime import datetime

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AgroUser as AgroUserModel, SubsidyTask, SubsidyResult, Subsidy, RegionBudget
from .serializers import (
    LoginSerializer, SubmitApplicationSerializer,
    SubsidyTaskSerializer, SubsidySerializer, RegionBudgetSerializer
)

HARDCODED_USERS = {
    'admin': {'password': 'admin', 'role': 'admin'},
}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── FBV: login ─────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    if username in HARDCODED_USERS:
        hc = HARDCODED_USERS[username]
        if hc['password'] != password:
            return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken()
        refresh['username'] = username
        refresh['role'] = hc['role']
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': username,
            'role': hc['role'],
        })

    try:
        user = AgroUserModel.objects.get(username=username, password_hash=hash_password(password))
    except AgroUserModel.DoesNotExist:
        return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken()
    refresh['username'] = user.username
    refresh['role'] = user.role
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
        'role': user.role,
    })


# ── FBV: submit application ─────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_application(request):
    serializer = SubmitApplicationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    username = request.user.username
    task_id = str(uuid.uuid4())
    now = datetime.now()

    task = SubsidyTask(
        id=task_id,
        farmer_id=username,
        application_number=data.get('application_number', f"APP-{task_id[:8].upper()}"),
        region_code=data['region_code'],
        region_priority=data.get('region_priority', 3),
        amount_requested=data['amount_requested'],
        amount_norm=data.get('amount_norm', 0),
        application_date=now,
        crop_type=data['crop_type'],
        farm_size_ha=data.get('farm_size_ha', 0),
        previous_subsidies_count=0,
        meta={
            'akimat': data.get('akimat', ''),
            'district': data.get('district', ''),
            'direction': data.get('direction', ''),
            'subsidy_name': data.get('subsidy_name', ''),
            'date_received': data.get('date_received', ''),
        },
        created_at=now,
    )
    task.save()

    try:
        ml_payload = {
            'app_num': task_id,
            'oblast': data['region_code'],
            'district': data.get('district', ''),
            'sector': data.get('direction', data['crop_type']),
            'subsidy_name': data.get('subsidy_name', data['crop_type']),
            'amount': float(data['amount_requested']),
            'norm': float(data.get('amount_norm', 0)),
            'date': now.strftime('%Y-%m-%d'),
            'status': 'Подана',
            'dept': data.get('akimat', ''),
            'applicant_name': username,
            'org_type': '',
        }
        ml_resp = requests.post(f"{settings.ML_SERVICE_URL}/score", json=[ml_payload], timeout=10)
        ml_data = ml_resp.json()[0]
        score = ml_data.get('score', 50.0)
        ai_comment = ml_data.get('tier', '')
    except Exception:
        score = 50.0
        ai_comment = 'ML сервис недоступен'

    SubsidyResult(
        id=task, score=score, shap_values={}, flags=[],
        admin_status='pending', ai_comment=ai_comment,
        processed_at=now, updated_at=now,
    ).save()

    return Response(SubsidyTaskSerializer(task).data, status=status.HTTP_201_CREATED)


# ── CBV: applications ──────────────────────────────────────────────────────

class ApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = SubsidyTask.objects.all().order_by('-created_at')
        search = request.query_params.get('search', '').strip()
        if search:
            tasks = tasks.filter(region_code__icontains=search)
        return Response(SubsidyTaskSerializer(tasks, many=True).data)


class ApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            result = SubsidyResult.objects.get(id=pk)
        except SubsidyResult.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'approve':
            result.admin_status = 'approved'
        elif action == 'reject':
            result.admin_status = 'rejected'
        else:
            return Response({'error': 'action must be approve or reject'}, status=status.HTTP_400_BAD_REQUEST)

        result.admin_comment = request.data.get('comment', '')
        result.updated_at = datetime.now()
        result.save()

        return Response(SubsidyTaskSerializer(SubsidyTask.objects.get(id=pk)).data)

    def delete(self, request, pk):
        try:
            task = SubsidyTask.objects.get(id=pk)
        except SubsidyTask.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── CBV: subsidies list ────────────────────────────────────────────────────

class SubsidyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subsidies = Subsidy.objects.all().order_by('direction', 'name')
        return Response(SubsidySerializer(subsidies, many=True).data)


# ── CBV: budget ─────────────────────────────────────────────────────────────

class BudgetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = RegionBudget.objects.all().order_by('-allocated_budget')
        return Response(RegionBudgetSerializer(budgets, many=True).data)

    def patch(self, request, pk=None):
        try:
            budget = RegionBudget.objects.get(pk=pk)
        except RegionBudget.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=status.HTTP_404_NOT_FOUND)

        budget.allocated_budget = request.data.get('allocated_budget', budget.allocated_budget)
        budget.updated_by = request.user.username
        budget.updated_at = datetime.now()
        budget.save()
        return Response(RegionBudgetSerializer(budget).data)
