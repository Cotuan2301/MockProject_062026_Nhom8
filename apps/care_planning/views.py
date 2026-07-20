from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count, Q
from .models import CarePlan

class CarePlanListView(ListView):
    model = CarePlan
    template_name = 'care_planning/care_plan_list.html'
    context_object_name = 'care_plans'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('resident', 'assigned_to')
        
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(resident__full_name__icontains=search) | 
                Q(resident__resident_id__icontains=search)
            )

        status_filter = self.request.GET.get('status', 'all')
        if status_filter and status_filter != 'all':
            queryset = queryset.filter(status=status_filter)
            
        review_filter = self.request.GET.get('review', 'all')
        if review_filter == 'due':
            queryset = queryset.filter(status=CarePlan.Status.REVIEW_DUE)

        return queryset.order_by('next_review_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_plans = CarePlan.objects.count()
        draft_plans = CarePlan.objects.filter(status=CarePlan.Status.DRAFT).count()
        pending_plans = CarePlan.objects.filter(status=CarePlan.Status.PENDING_REVIEW).count()
        review_due_plans = CarePlan.objects.filter(status=CarePlan.Status.REVIEW_DUE).count()

        context['summary'] = {
            'total': total_plans,
            'draft': draft_plans,
            'pending': pending_plans,
            'review_due': review_due_plans
        }
        
        context['current_search'] = self.request.GET.get('search', '')
        context['current_status'] = self.request.GET.get('status', 'all')
        context['current_review'] = self.request.GET.get('review', 'all')
        context['active_menu'] = 'care_planning'
        
        return context
