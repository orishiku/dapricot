from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, commenter, timestamp):
        return (
            six.text_type(commenter.pk) + six.text_type(timestamp) +
            six.text_type(commenter.status)
        )

account_activation_token = AccountActivationTokenGenerator()