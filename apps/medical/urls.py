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
)


urlpatterns = [

    # ==========================
    # SC027 - UI
    # ==========================

    path(
        "care-plans/create/",
        care_plan_create_page,
        name="care_plan_create",
    ),



    # ==========================
    # Care Level API
    # ==========================

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




    # ==========================
    # Care Plan API
    # ==========================

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





    # ==========================
    # Care Goal API
    # ==========================

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

]