from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm

from cards.models import UserCard, Skill, Service, Portfolio
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import CustomUser
from .services.subdomains import check_subdomain_availability

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور',
            'dir': 'ltr',
        }),
        validators=[MinLengthValidator(8)]
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری',
                'dir': 'ltr',
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کامل',
                'dir': 'rtl',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل (اختیاری)',
                'dir': 'ltr',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        result = check_subdomain_availability(username)
        if not result.available:
            raise forms.ValidationError(f"ساب‌دامین معتبر نیست: {result.reason}")
        return result.name

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'نام کاربری',
        'dir': 'ltr',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'رمز عبور',
        'dir': 'ltr',
    }))

class UserCardForm(forms.ModelForm):
    username = forms.CharField(
        min_length=3,
        max_length=32,
        validators=[MinLengthValidator(3), MaxLengthValidator(32)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری (3 تا 32 کاراکتر، بدون فاصله)',
            'dir': 'ltr',
        })
    )
    class Meta:
        model = UserCard
        fields = [
            'username',
            'name',
            "phone_number",
            "profile_picture",
            'short_bio',
            'description',
            'email',
            'website',
            'instagram_username',
            'telegram_username',
            'linkedin_username',
            'youtube_username',
            'twitter_username',
            'color',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری (بدون فاصله)',
                'dir': 'ltr',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کامل',
                'dir': 'rtl',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس',
                'dir': 'rtl',
            }),
            'short_bio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'توضیح مختصر درباره خود',
                'maxlength': '255',
                'dir': 'rtl',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات تفصیلی',
                'rows': 4,
                'dir': 'rtl',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com',
                'dir': 'ltr',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
                'dir': 'ltr',
            }),
            'instagram_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username',
                'dir': 'ltr',
            }),
            'telegram_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username',
                'dir': 'ltr',
            }),
            'linkedin_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn profile URL',
                'dir': 'ltr',
            }),
            'youtube_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username',
                'dir': 'ltr',
            }),
            'twitter_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username',
                'dir': 'ltr',
            }),
            'color': forms.Select(attrs={
                'class': 'form-control color-select',
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'profile_picture_input'
            }),
        }
    
    # Hidden field to persist image data across form errors
    profile_picture_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        result = check_subdomain_availability(username, user=getattr(self.instance, "user", None))
        if not result.available:
            raise forms.ValidationError(f"ساب‌دامین معتبر نیست: {result.reason}")
        return result.name


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control skill-input',
                'placeholder': 'نام مهارت',
                'dir': 'rtl',
            }),
        }


class SkillFormSet(forms.BaseInlineFormSet):
    """FormSet for managing multiple skills"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra = 0  # No extra forms by default - add via JavaScript


# Create formset factory
SkillInlineFormSet = forms.inlineformset_factory(
    UserCard,
    Skill,
    form=SkillForm,
    formset=SkillFormSet,
    extra=0,
    can_delete=True,
)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description']  # Removed 'icon' field
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control service-input',
                'placeholder': 'عنوان خدمت',
                'dir': 'rtl',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control service-input',
                'placeholder': 'توضیح خدمت',
                'rows': 3,
                'dir': 'rtl',
            }),
        }


class ServiceFormSet(forms.BaseInlineFormSet):
    """FormSet for managing multiple services"""
    pass


ServiceInlineFormSet = forms.inlineformset_factory(
    UserCard,
    Service,
    form=ServiceForm,
    formset=ServiceFormSet,
    extra=0,
    can_delete=True,
)


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'image', 'url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control portfolio-input',
                'placeholder': 'عنوان پروژه',
                'dir': 'rtl',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control portfolio-input',
                'placeholder': 'توضیح پروژه',
                'rows': 3,
                'dir': 'rtl',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control portfolio-input',
                'accept': 'image/*',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control portfolio-input',
                'placeholder': 'https://example.com',
                'dir': 'ltr',
            }),
        }

    # Hidden field to persist image data across form errors
    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)


class PortfolioFormSet(forms.BaseInlineFormSet):
    """FormSet for managing multiple portfolio items"""
    pass


PortfolioInlineFormSet = forms.inlineformset_factory(
    UserCard,
    Portfolio,
    form=PortfolioForm,
    formset=PortfolioFormSet,
    extra=0,
    can_delete=True,
)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_username(self):
        return self.cleaned_data.get("username") or ""

    def clean_email(self):
        return self.cleaned_data.get("email") or ""
