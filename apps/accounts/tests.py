import time
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.signing import TimestampSigner

from apps.accounts.models import User, Role
from apps.accounts.utils import SC003_VERIFICATION_SALT

class SC001LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('accounts_api:login')
        
        # Create a test role
        self.role = Role.objects.create(role_name="Admin", description="Admin Role")
        
        # Create an ACTIVE user
        self.active_user = User.objects.create(
            employee_code="E001",
            email="active@facility.org",
            phone_number="+15550001234",
            password_hash=make_password("Password123!"),
            first_name="Active",
            last_name="User",
            role=self.role,
            status=User.Status.ACTIVE,
            mfa_enabled=False
        )
        
        # Create an INACTIVE user
        self.inactive_user = User.objects.create(
            employee_code="E002",
            email="inactive@facility.org",
            phone_number="+15550002222",
            password_hash=make_password("Password123!"),
            first_name="Inactive",
            last_name="User",
            role=self.role,
            status=User.Status.INACTIVE
        )
        
        # Removed locked user creation as the requested tests only deal with ACTIVE, INACTIVE, and LOCKED. Wait, INACTIVE and LOCKED are requested.
        # Create a LOCKED user
        self.locked_user = User.objects.create(
            employee_code="E003",
            email="locked@facility.org",
            phone_number="+15550003333",
            password_hash=make_password("Password123!"),
            first_name="Locked",
            last_name="User",
            role=self.role,
            status=User.Status.LOCKED
        )
        
        # Create an ACTIVE user with no phone
        self.nophone_user = User.objects.create(
            employee_code="E004",
            email="nophone@facility.org",
            phone_number="",
            password_hash=make_password("Password123!"),
            first_name="NoPhone",
            last_name="User",
            role=self.role,
            status=User.Status.ACTIVE
        )

    def test_active_email_success(self):
        response = self.client.post(self.login_url, {
            "identifier": "active@facility.org",
            "password": "Password123!"
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check masked phone
        self.assertEqual(response.data["phone_number"], "******1234")
        
        # Check mfa_required is explicitly True regardless of user.mfa_enabled
        self.assertTrue(response.data["mfa_required"])
        
        # Check token exists and contains no sensitive data
        token = response.data["verification_token"]
        signer = TimestampSigner(salt=SC003_VERIFICATION_SALT)
        payload = signer.unsign_object(token)
        self.assertEqual(payload['user_id'], self.active_user.id)
        self.assertEqual(payload['purpose'], 'otp_verification')
        self.assertNotIn('password', payload)
        self.assertNotIn('email', payload)
        
        # Check no access/refresh JWT returned
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        
        # Check no authenticated session
        self.assertFalse('_auth_user_id' in self.client.session)
        
        # Check no last-login update
        self.active_user.refresh_from_db()
        self.assertIsNone(self.active_user.last_login_at)

    def test_active_phone_success(self):
        response = self.client.post(self.login_url, {
            "identifier": "+15550001234",
            "password": "Password123!"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "******1234")

    def test_identical_public_401_response(self):
        # 1. Unknown email
        res1 = self.client.post(self.login_url, {"identifier": "unknown@facility.org", "password": "Password123!"}, format='json')
        
        # 2. Unknown phone
        res2 = self.client.post(self.login_url, {"identifier": "+19999999999", "password": "Password123!"}, format='json')
        
        # 3. Wrong password
        res3 = self.client.post(self.login_url, {"identifier": "active@facility.org", "password": "WrongPassword!"}, format='json')
        
        # 4. INACTIVE user
        res4 = self.client.post(self.login_url, {"identifier": "inactive@facility.org", "password": "Password123!"}, format='json')
        
        # 5. LOCKED user
        res5 = self.client.post(self.login_url, {"identifier": "locked@facility.org", "password": "Password123!"}, format='json')
        
        # 6. Unusable phone (ACTIVE user without phone)
        res6 = self.client.post(self.login_url, {"identifier": "nophone@facility.org", "password": "Password123!"}, format='json')
        
        expected_response = {"detail": "Invalid email/phone or password."}
        
        for idx, res in enumerate([res1, res2, res3, res4, res5, res6], start=1):
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED, f"Failed at {idx}")
            self.assertEqual(res.data, expected_response, f"Failed at {idx}")

    def test_missing_fields(self):
        # Missing identifier
        response1 = self.client.post(self.login_url, {
            "password": "Password123!"
        }, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response1.data, {"detail": "Identifier and password are required."})

        # Missing password
        response2 = self.client.post(self.login_url, {
            "identifier": "active@facility.org"
        }, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data, {"detail": "Identifier and password are required."})

    def test_identifier_boundaries(self):
        # Oversized identifier returns controlled 400
        long_email = "a" * 250 + "@test.com" # 259 chars
        res_email = self.client.post(self.login_url, {"identifier": long_email, "password": "Password123!"}, format='json')
        self.assertEqual(res_email.status_code, status.HTTP_400_BAD_REQUEST)
        
        long_phone = "+1" + "5" * 256 # 258 chars
        res_phone = self.client.post(self.login_url, {"identifier": long_phone, "password": "Password123!"}, format='json')
        self.assertEqual(res_phone.status_code, status.HTTP_400_BAD_REQUEST)

    def test_case_insensitive_email_login(self):
        # active_user's email is "active@facility.org" (lowercase)
        response = self.client.post(self.login_url, {
            "identifier": "AcTiVe@fAcIlItY.oRg",
            "password": "Password123!"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("verification_token" in response.data)
        self.assertTrue(response.data.get("mfa_required"))

    def test_identifier_whitespace_trimming(self):
        # Email with trailing and leading spaces
        response = self.client.post(self.login_url, {
            "identifier": "  active@facility.org  ",
            "password": "Password123!"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("verification_token" in response.data)

    def test_password_whitespace_preservation(self):
        # active_user's password hash corresponds to "Password123!" (no spaces)
        response = self.client.post(self.login_url, {
            "identifier": "active@facility.org",
            "password": " Password123! "
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Invalid email/phone or password."})

