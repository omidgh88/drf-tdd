from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with email is successful
        """
        email = "test@example.com"
        password = "pass1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email of new user is normalized
        """
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(email, "pass1234")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test createing new user with no email will raise error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "pass1234")

    def test_create_new_superuser(self):
        """test creating a new super user
        """
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "pass1234"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
