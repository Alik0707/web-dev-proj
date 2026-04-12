from rest_framework import serializers
from .models import SubsidyTask, SubsidyResult, Subsidy, RegionBudget


# ── serializers.Serializer ──────────────────────────────────────────────────

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True)


class SubmitApplicationSerializer(serializers.Serializer):
    # Step 1 — Местоположение
    date_received = serializers.CharField(max_length=20, required=False, default='')
    region_code = serializers.CharField(max_length=100)
    akimat = serializers.CharField(max_length=255, required=False, default='')
    district = serializers.CharField(max_length=100, required=False, default='')
    # Step 2 — Заявка
    application_number = serializers.CharField(max_length=100, required=False, default='')
    direction = serializers.CharField(max_length=100, required=False, default='')
    subsidy_name = serializers.CharField(max_length=255, required=False, default='')
    crop_type = serializers.CharField(max_length=100, required=False, default='')
    # Step 3 — Расчет
    amount_norm = serializers.DecimalField(max_digits=15, decimal_places=2, required=False, default=0)
    amount_requested = serializers.DecimalField(max_digits=15, decimal_places=2)
    farm_size_ha = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    region_priority = serializers.IntegerField(min_value=1, max_value=5, default=3)


# ── serializers.ModelSerializer ────────────────────────────────────────────

class SubsidyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsidyResult
        fields = ['score', 'admin_status', 'admin_comment', 'ai_comment', 'processed_at']


class SubsidyTaskSerializer(serializers.ModelSerializer):
    result = SubsidyResultSerializer(source='subsidyresult', read_only=True)

    class Meta:
        model = SubsidyTask
        fields = [
            'id', 'farmer_id', 'application_number', 'region_code',
            'crop_type', 'farm_size_ha', 'amount_requested', 'amount_norm',
            'application_date', 'previous_subsidies_count', 'created_at', 'result'
        ]


class SubsidySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsidy
        fields = ['id', 'name', 'normative', 'unit', 'direction']


class RegionBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionBudget
        fields = ['id', 'region_name', 'allocated_budget', 'updated_at', 'updated_by']
