from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

# 사용자 정보를 받아, '임시 기간 동안 인증에 사용'되는 '토큰'을 생성
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
