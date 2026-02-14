from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from core.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # Always allow auto signup to avoid the signup form.
        # If signup fails (e.g. due to missing fields or conflicts), 
        # it will trigger on_authentication_error.
        return True

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        
        This is used to connect a social account to an existing user if the email matches.
        """
        # Log the beginning of the process
        logger.info(f"pre_social_login started: provider={sociallogin.account.provider}, user={sociallogin.user}")

        # Social account already exists, so this is a login, not a signup.
        if sociallogin.is_existing:
            logger.info(f"pre_social_login: Social account already exists for {sociallogin.user}")
            return

        # Check if we have a user with the same email
        email = sociallogin.user.email
        
        # If email is not in user object, try to get it from extra_data
        if not email and 'email' in sociallogin.account.extra_data:
            email = sociallogin.account.extra_data.get('email')
        
        # Some providers might have nested email info (like GitHub)
        if not email and sociallogin.account.provider == 'github':
            # GitHub email might be in extra_data or fetched via API by allauth
            email = sociallogin.account.extra_data.get('email')
            if not email:
                # GitHub user profile might have email field
                email = sociallogin.account.extra_data.get('user', {}).get('email')
        
        # If still no email, allauth might have it in sociallogin.email_addresses
        if not email and sociallogin.email_addresses:
            for email_obj in sociallogin.email_addresses:
                if email_obj.primary:
                    email = email_obj.email
                    break
            if not email:
                email = sociallogin.email_addresses[0].email

        logger.info(f"pre_social_login: Final email identified: '{email}'")
        
        if not email:
            logger.error(f"pre_social_login: No email found for provider {sociallogin.account.provider}. Extra data: {sociallogin.account.extra_data}")
            # If email is required but missing, we must stop here to avoid IntegrityError during auto-signup
            error_message = "ایمیل شما توسط سرویس‌دهنده بازگردانده نشد. لطفاً دسترسی به ایمیل را در تنظیمات حساب خود بررسی کنید."
            messages.error(request, error_message)
            raise ImmediateHttpResponse(redirect(reverse('login')))

        try:
            # Find the existing user by email
            user = CustomUser.objects.get(email=email)
            logger.info(f"pre_social_login: Found existing user {user} with ID {user.id} for email {email}")
            
            # Connect the social account to the existing user
            sociallogin.connect(request, user)
            
            # Ensure the social account is saved so allauth knows this is an existing login
            # This prevents the flow from proceeding to process_signup
            if not sociallogin.account.pk:
                sociallogin.account.save()
                logger.info(f"pre_social_login: Saved social account for existing user {user}")
            
            # Update the sociallogin object state
            logger.info(f"pre_social_login: Connected and verified social account for existing user {sociallogin.user}")
        except CustomUser.DoesNotExist:
            logger.info(f"pre_social_login: No existing user found for email {email}. Proceeding with auto-signup.")
        except Exception as e:
            logger.error(f"pre_social_login: Error during connection: {e}", exc_info=True)

    def on_authentication_error(self, request, provider, error=None, exception=None, extra_context=None):
        """
        Handle social authentication errors and redirect to the login page
        with a Persian message.
        """
        # Log the error for debugging
        logger.error(f"Social authentication error: provider={provider}, error={error}, exception={exception}")
        if extra_context:
            logger.error(f"Extra context: {extra_context}")

        # Default Persian error message
        error_message = "خطایی در هنگام ورود با حساب اجتماعی رخ داد. لطفاً دوباره تلاش کنید."
        
        if error == 'access_denied':
            error_message = "ورود توسط کاربر لغو شد یا دسترسی داده نشد."
        elif error == 'connection_error':
            error_message = "خطا در برقراری ارتباط با سرویس‌دهنده. لطفاً اتصال اینترنت خود را بررسی کنید."
        elif exception:
            exc_str = str(exception)
            logger.error(f"Exception details: {exc_str}")
            
            # Handle specific exceptions if needed
            if "SocialAccount already exists" in exc_str:
                error_message = "این حساب اجتماعی قبلاً به حساب دیگری متصل شده است."
            elif "Email address already exists" in exc_str:
                error_message = "ایمیل مربوط به این حساب اجتماعی قبلاً در سایت ثبت شده است."
            elif "invalid_grant" in exc_str:
                error_message = "خطا در تأیید هویت (invalid_grant). احتمالاً تنظیمات اپلیکیشن در پنل گوگل/گیت‌هاب با دامنه سایت مطابقت ندارد."
            elif "timed out" in exc_str:
                error_message = "زمان پاسخ‌گویی سرویس‌دهنده به پایان رسید. لطفاً دوباره تلاش کنید."

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
