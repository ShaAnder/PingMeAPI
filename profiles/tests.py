from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile


class ProfileSignalTestCase(TestCase):
  def setUp(self):
    """Create a test user before each test."""
    self.user = User.objects.create_user(
        username='testuser',
        password='securepassword123'
    )

  def tearDown(self):
    """Delete test user and related profile after each test."""
    self.user.delete()

  def test_profile_created_on_user_creation(self):
    """TEST 1:
      Testing to see if a user profile created on user creation
    """
    self.assertTrue(
    hasattr(self.user, 'user_profile'),
    msg="User should have a related profile."
    )
    self.assertIsInstance(
    self.user.user_profile, Profile,
    msg="User.user_profile should be an instance of Profile model."
    )
