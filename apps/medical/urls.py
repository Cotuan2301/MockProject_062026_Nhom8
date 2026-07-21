from django.urls import path, include
from . import views

from django.urls import path

from apps.medical.views import (
    CareLevelListCreateView,
    CareLevelDetailView,
    CarePlanListCreateView,
    CarePlanDetailView,
    CareGoalListCreateView,
    CareGoalDetailView,
    care_plan_create_page,
    care_plan_locked_page,
    care_plan_detail_page,
)



app_name = "medical"

urlpatterns = [
    # SC032
    path('daily-tasks/', views.daily_tasks, name='daily_tasks'),
    path('api/update-task/', views.update_task_status, name='update_task_status'),

    # SC033
    path('bedside-vitals/', views.bedside_vitals, name='bedside_vitals'),
    path('api/save-vitals/', views.save_bedside_vitals, name='save_bedside_vitals'),

    # SC034
    path('reassessments/', views.reassessments, name='reassessments'),
    path('api/start-reassessment/', views.start_reassessment, name='start_reassessment'),

    path(
        "assessments/<int:assessment_id>/loc/",
        views.loc_classification_detail,
        name="loc_detail",
    ),
    path(
        "assessments/<int:assessment_id>/loc/confirm/",
        views.loc_classification_confirm,
        name="loc_confirm",
    ),
    path(
        "assessments/<int:assessment_id>/loc/override/",
        views.loc_classification_override,
        name="loc_override",
    ),

    # ==========================
    # SC027 - UI
    # ==========================

    path(
        "care-plans/create/",
        care_plan_create_page,
        name="care_plan_create",
    ),

    # SC028
    path(
        "care-plans/locked/",
        care_plan_locked_page,
        name="care_plan_locked",
    ),

    # SC029
    path(
        "care-plans/detail/",
        care_plan_detail_page,
        name="care_plan_detail",
    ),

    # Care Level API
    path(
        "api/care-levels/",
        CareLevelListCreateView.as_view(),
        name="carelevel-list",
    ),
    path(
        "api/care-levels/<int:pk>/",
        CareLevelDetailView.as_view(),
        name="carelevel-detail",
    ),

    # Care Plan API
    path(
        "api/care-plans/",
        CarePlanListCreateView.as_view(),
        name="careplan-list",
    ),
    path(
        "api/care-plans/<int:pk>/",
        CarePlanDetailView.as_view(),
        name="careplan-detail",
    ),

    # Care Goal API
    path(
        "api/care-goals/",
        CareGoalListCreateView.as_view(),
        name="caregoal-list",
    ),
    path(
        "api/care-goals/<int:pk>/",
        CareGoalDetailView.as_view(),
        name="caregoal-detail",
    ),
    path(
        "care-plans/locked/",
        care_plan_locked_page,
        name="care_plan_locked",
    ),
    path(
        "care-plans/detail/",
        care_plan_detail_page, 
        name="care_plan_detail",
    ),

    path(
        'initial-assessment/<int:pk>/',
        views.initial_assessment,
        name='initial_assessment',
    ),
    path(
        'initial-assessment/<int:pk>/<int:assessment_id>/',
        views.initial_assessment,
        name='initial_assessment',
    ),
    path(
        'api/assessment/<int:assessment_id>/diagnosis/add/',
        views.api_add_diagnosis,
        name='api_add_diagnosis',
    ),
    path(
        'api/assessment/<int:assessment_id>/diagnosis/<int:diagnosis_id>/remove/',
        views.api_remove_diagnosis,
        name='api_remove_diagnosis',
    ),
]