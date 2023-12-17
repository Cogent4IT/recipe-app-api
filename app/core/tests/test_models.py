"""
Tests for models.
"""

# importing relative package for testing
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models """

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful. """
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        # check_password is provided by django
        self.assertEqual(user.check_password(password), True)

    # user can give any format of email,
    # django should normalize it to standard email
    # after "@", everything should be lower case
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com","test1@example.com"],
            ["Test2@Example.com","Test2@example.com"],
            ["TEST3@EXAMPLE.com","TEST3@example.com"],
            ["test4@EXAMPLE.COM","test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    # Check if input email is blank or null
    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        # with statement is equivalent to using keyword in C#
        with self.assertRaises(ValueError):
            # here we are checking if email is null
            # or blank, pwd can be any dummy value.
            get_user_model().objects.create_user("","test123")

    def test_create_superuser(self):
        """Test creating a superuser"""
        # creating super user
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
