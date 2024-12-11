from django.test import TestCase

# Create your tests here.

# test for veryfiying the email
from django.core import mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Attender
from django.core.mail import send_mail

class EmailVerificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',   
        )
        self.attender = Attender.objects.create(
            name='Test',
            surname='User',
            code='12345',
            email = 'roxierba@gmail.com'
        )

    def test_email_verification(self):
        # send the email to the user
        send_mail(
            'Subject here',
            'Here is the message.',
            settings.EMAIL_HOST_USER,
            [self.attender.email],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
        self.assertEqual(mail.outbox[0].body, 'Here is the message.')
        