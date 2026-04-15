


from django.db import models
from django.contrib.postgres.fields import ArrayField


class AgroUser(models.Model):
    id = models.UUIDField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=20, default='user')
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username


class Subsidy(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    normative = models.IntegerField()
    unit = models.TextField()
    direction = models.TextField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(
        AgroUser, null=True, blank=True,
        on_delete=models.SET_NULL, db_column='updated_by'
    )

    class Meta:
        managed = False
        db_table = 'subsidies'

    def __str__(self):
        return self.name


class SubsidyTask(models.Model):
    id = models.UUIDField(primary_key=True)
    farmer_id = models.CharField(max_length=100)
    application_number = models.CharField(max_length=100, default='')
    region_code = models.CharField(max_length=50)
    region_priority = models.IntegerField()
    amount_requested = models.DecimalField(max_digits=15, decimal_places=2)
    amount_norm = models.DecimalField(max_digits=15, decimal_places=2)
    application_date = models.DateTimeField()
    crop_type = models.CharField(max_length=100)
    farm_size_ha = models.DecimalField(max_digits=10, decimal_places=2)
    previous_subsidies_count = models.IntegerField(default=0)
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'subsidy_tasks'

    def __str__(self):
        return f"{self.application_number} - {self.farmer_id}"


class SubsidyResult(models.Model):
    id = models.OneToOneField(
        SubsidyTask, primary_key=True,
        on_delete=models.CASCADE, db_column='id'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    shap_values = models.JSONField(default=dict)
    flags = ArrayField(models.TextField(), default=list)
    admin_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    admin_comment = models.TextField(null=True, blank=True)
    admin_status = models.CharField(max_length=50, null=True, blank=True)
    ai_comment = models.TextField(null=True, blank=True)
    return_deadline = models.DateTimeField(null=True, blank=True)
    budget_returned_at = models.DateTimeField(null=True, blank=True)
    processed_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'subsidy_results'


class RegionBudget(models.Model):
    id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=100, unique=True)
    allocated_budget = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'region_budgets'

    def __str__(self):
        return self.region_name


class UserProfile(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    region = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')
    akimat = models.CharField(max_length=255, default='')
    entity_type = models.CharField(max_length=50, default='')
    pasture_type = models.CharField(max_length=100, default='')
    has_account_number = models.BooleanField(default=False)
    has_land = models.BooleanField(default=False)
    land_area_ha = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    livestock_count = models.IntegerField(default=0)
    registered_isj = models.BooleanField(default=False)
    registered_ibspr = models.BooleanField(default=False)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_profiles'
