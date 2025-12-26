from django import forms
from core.models import UserCard, Skill, Service, Portfolio
from django.core.validators import MinLengthValidator, MaxLengthValidator


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

        }


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
                'class': 'form-control',
                'placeholder': 'عنوان خدمت',
                'dir': 'rtl',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
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
                'class': 'form-control',
                'placeholder': 'عنوان پروژه',
                'dir': 'rtl',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'توضیح پروژه',
                'rows': 3,
                'dir': 'rtl',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
                'dir': 'ltr',
            }),
        }


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
