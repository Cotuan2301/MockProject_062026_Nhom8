from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Assessment, LOCClassification
from apps.residents.models import Resident
from apps.billing.models import LOCRate

class LOCClassificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='nurse', password='password')
        self.resident = Resident.objects.create(
            resident_id='RES_TEST',
            first_name='Test',
            last_name='Resident',
            date_of_birth='1950-01-01'
        )
        self.assessment = Assessment.objects.create(
            resident=self.resident,
            assessed_by=self.user,
            total_adl_score=20,
            care_level='Level 3'
        )
        LOCRate.objects.create(loc_level='Level 3', daily_rate='248.00')

    def test_loc_detail_view(self):
        self.client.login(username='nurse', password='password')
        response = self.client.get(reverse('medical:loc_detail', args=[self.assessment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '20 / 32')
        self.assertContains(response, 'Level 3')

    def test_loc_confirm(self):
        self.client.login(username='nurse', password='password')
        self.client.get(reverse('medical:loc_detail', args=[self.assessment.id])) # Trigger get_or_create
        response = self.client.post(reverse('medical:loc_confirm', args=[self.assessment.id]))
        self.assertEqual(response.status_code, 302)
        
        loc = LOCClassification.objects.get(assessment=self.assessment)
        self.assertEqual(loc.status, 'Confirmed')
        self.assertEqual(loc.final_loc, 'Level 3')

    def test_loc_override(self):
        self.client.login(username='nurse', password='password')
        self.client.get(reverse('medical:loc_detail', args=[self.assessment.id])) # Trigger get_or_create
        response = self.client.post(reverse('medical:loc_override', args=[self.assessment.id]), {
            'override_loc': 'Level 4',
            'override_reason': 'Needs more help'
        })
        self.assertEqual(response.status_code, 302)
        
        loc = LOCClassification.objects.get(assessment=self.assessment)
        self.assertEqual(loc.status, 'Confirmed')
        self.assertTrue(loc.is_overridden)
        self.assertEqual(loc.final_loc, 'Level 4')

    def test_loc_chart_lock(self):
        LOCClassification.objects.create(
            assessment=self.assessment,
            calculated_score=20,
            suggested_loc='Level 3',
            final_loc='Level 3',
            status='Confirmed'
        )
        
        self.client.login(username='nurse', password='password')
        response = self.client.post(reverse('medical:loc_confirm', args=[self.assessment.id]))
        self.assertEqual(response.status_code, 400) 

        response = self.client.post(reverse('medical:loc_override', args=[self.assessment.id]), {
            'override_loc': 'Level 4',
            'override_reason': 'test'
        })
        self.assertEqual(response.status_code, 400)

class AssessmentHistoryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='nurse2', password='password123')
        
        self.resident = Resident.objects.create(
            resident_id='RES_TEST2',
            first_name='Robert',
            last_name='Hayes',
            date_of_birth='1950-01-01'
        )

        self.assessment_v1 = Assessment.objects.create(
            resident=self.resident,
            version=1,
            assessment_type='initial',
            assessed_by=self.user,
            total_adl_score=14,
            care_level='Level 2',
            is_locked=True
        )

    def test_assessment_history_view(self):
        self.client.login(username='nurse2', password='password123')
        response = self.client.get(reverse('medical:assessment_history', args=[self.resident.resident_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assessment History — Robert Hayes')
        self.assertContains(response, 'v1')
        self.assertContains(response, 'Initial')

    def test_create_reassessment_api(self):
        self.client.login(username='nurse2', password='password123')
        response = self.client.post(reverse('medical:create_reassessment', args=[self.resident.resident_id]))
        # Should redirect back to history
        self.assertEqual(response.status_code, 302)
        
        # Verify new assessment was created
        new_assessment = Assessment.objects.filter(resident=self.resident).order_by('-version').first()
        self.assertEqual(new_assessment.version, 2)
        self.assertEqual(new_assessment.assessment_type, 'reassessment')
        self.assertEqual(new_assessment.total_adl_score, 14) # Copied from v1
        self.assertFalse(new_assessment.is_locked) # New draft is unlocked
