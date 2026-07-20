from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.residents.models import Resident
from apps.care_planning.models import CarePlan
import datetime

User = get_user_model()

class CarePlanTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='nurse_anna', password='password123')
        
        # Create residents
        self.resident1 = Resident.objects.create(
            resident_id='R001',
            full_name='Susan Wright',
            room_number='114B',
            date_of_birth=datetime.date(1950, 1, 1),
            admission_date=datetime.date(2025, 1, 1),
            loc_tier=Resident.LocTier.TIER_2
        )
        self.resident2 = Resident.objects.create(
            resident_id='R002',
            full_name='James Porter',
            room_number='210B',
            date_of_birth=datetime.date(1945, 5, 5),
            admission_date=datetime.date(2025, 2, 1),
            loc_tier=Resident.LocTier.TIER_4
        )

        # Create Care Plans
        self.plan1 = CarePlan.objects.create(
            resident=self.resident1,
            status=CarePlan.Status.NEEDS_UPDATE,
            next_review_date=datetime.date(2026, 7, 3),
            assigned_to=self.user
        )
        self.plan2 = CarePlan.objects.create(
            resident=self.resident2,
            status=CarePlan.Status.REVIEW_DUE,
            next_review_date=datetime.date(2026, 7, 3),
            assigned_to=self.user
        )
        self.plan3 = CarePlan.objects.create(
            resident=self.resident1,
            status=CarePlan.Status.DRAFT,
            next_review_date=datetime.date(2026, 8, 1)
        )

    def test_care_plan_creation(self):
        self.assertEqual(CarePlan.objects.count(), 3)
        self.assertEqual(self.plan1.resident.full_name, 'Susan Wright')

    def test_list_view_status_code(self):
        url = reverse('care_planning:care_plan_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_context(self):
        url = reverse('care_planning:care_plan_list')
        response = self.client.get(url)
        self.assertTrue('care_plans' in response.context)
        self.assertEqual(len(response.context['care_plans']), 3)
        
        # Check summary stats
        summary = response.context['summary']
        self.assertEqual(summary['total'], 3)
        self.assertEqual(summary['draft'], 1)
        self.assertEqual(summary['review_due'], 1)

    def test_search_filter(self):
        url = reverse('care_planning:care_plan_list')
        response = self.client.get(url, {'search': 'James'})
        care_plans = response.context['care_plans']
        self.assertEqual(len(care_plans), 1)
        self.assertEqual(care_plans[0].resident.full_name, 'James Porter')

    def test_status_filter(self):
        url = reverse('care_planning:care_plan_list')
        response = self.client.get(url, {'status': 'draft'})
        care_plans = response.context['care_plans']
        self.assertEqual(len(care_plans), 1)
        self.assertEqual(care_plans[0].status, CarePlan.Status.DRAFT)

    def test_review_filter(self):
        url = reverse('care_planning:care_plan_list')
        response = self.client.get(url, {'review': 'due'})
        care_plans = response.context['care_plans']
        self.assertEqual(len(care_plans), 1)
        self.assertEqual(care_plans[0].status, CarePlan.Status.REVIEW_DUE)
