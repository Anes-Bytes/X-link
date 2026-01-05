from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # Always allow auto signup to avoid the signup form.
        # If signup fails (e.g. due to missing fields or conflicts), 
        # it will trigger on_authentication_error.
        return True

    def on_authentication_error(self, request, provider, error=None, exception=None, extra_context=None):
        """
        Handle social authentication errors and redirect to the login page
        with a Persian message.
        """
        # Log the error for debugging
        logger.error(f"Social authentication error: provider={provider}, error={error}, exception={exception}")

        # Default Persian error message
        error_message = "خطایی در هنگام ورود با حساب اجتماعی رخ داد. لطفاً دوباره تلاش کنید."
        
        if error == 'access_denied':
            error_message = "ورود توسط کاربر لغو شد یا دسترسی داده نشد."
        elif error == 'connection_error':
            error_message = "خطا در برقراری ارتباط با سرویس‌دهنده. لطفاً اتصال اینترنت خود را بررسی کنید."
        elif exception:
            exc_str = str(exception)
            # Handle specific exceptions if needed
            if "SocialAccount already exists" in exc_str:
                error_message = "این حساب اجتماعی قبلاً به حساب دیگری متصل شده است."
            elif "Email address already exists" in exc_str:
                error_message = "ایمیل مربوط به این حساب اجتماعی قبلاً در سایت ثبت شده است."

        messages.error(request, error_message)
        
        # Redirect to the login page instead of showing Allauth's error page
        raise ImmediateHttpResponse(redirect(reverse('login')))

    def authentication_error(self, request, provider=None, error=None, exception=None, extra_context=None):
        # Some versions of allauth might call this or on_authentication_error
        self.on_authentication_error(request, provider, error, exception, extra_context)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return reverse('dashboard')

    def get_logout_redirect_url(self, request):
        return reverse('home')
