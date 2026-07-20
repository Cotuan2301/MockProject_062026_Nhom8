from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.residents.models import Resident
from apps.medical.models import ResidentCareLevelHistory
import datetime

class ResidentCareLevelHistoryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='nurse_anna', password='password123')
        self.user.first_name = "Anna"
        self.user.last_name = "Lee"
        self.user.save()

        self.resident = Resident.objects.create(
            resident_id='RES-00089',
            full_name='Robert Hayes',
            room_number='204B',
            date_of_birth=datetime.date(1943, 4, 15),
            admission_date=datetime.date(2025, 1, 1)
        )

        self.history1 = ResidentCareLevelHistory.objects.create(
            resident=self.resident,
            action='Overridden',
            previous_tier='Level 1',
            new_tier='Level 2',
            actor=self.user,
            note='Post-fall mobility decline'
        )

        self.history2 = ResidentCareLevelHistory.objects.create(
            resident=self.resident,
            action='Confirmed',
            previous_tier='Level 2',
            new_tier='Level 3',
            actor=self.user,
            note='Suggested tier accepted'
        )

    def test_history_list_api(self):
        url = reverse('medical:loc-history-list', args=[self.resident.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        # Should be ordered by date descending
        self.assertEqual(data[0]['action'], 'Confirmed')
        self.assertEqual(data[1]['action'], 'Overridden')
        self.assertEqual(data[0]['actor_name'], 'Anna Lee')

    def test_history_export_api(self):
        url = reverse('medical:loc-history-export', args=[self.resident.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        
        content = response.content.decode('utf-8')
        self.assertIn('Date,Action,Previous Tier,New Tier,Actor,Note', content)
        self.assertIn('Confirmed,Level 2,Level 3,Anna Lee,Suggested tier accepted', content)
        self.assertIn('Overridden,Level 1,Level 2,Anna Lee,Post-fall mobility decline', content)

    def test_loc_history_view(self):
        url = reverse('medical:loc-history', args=[self.resident.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Robert Hayes')
        self.assertContains(response, 'RES-00089')
        self.assertContains(response, 'Print/Export')
