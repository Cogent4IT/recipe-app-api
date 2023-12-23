"""Tests for Django admin modifications."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        # Create super/Admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        # Create Regular user
        self.user = get_user_model().objects.create_user(
            email="user@exampe.ocm",
            password="testpass123",
            name="Test User"
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        # Views are accessible using Django's URL reversing system.
        url = reverse("admin:core_user_changelist")
        # getting response from the url
        res = self.client.get(url)

        # checking for the regular user - user@exmample.com
        self.assertContains(res, self.user.name)
        self .assertContains(res, self.user.email)

    # test case for edit user
    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


    # create user
    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)