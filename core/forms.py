from django import forms
from core.models import UserCard, Skill


class UserCardForm(forms.ModelForm):
    class Meta:
        model = UserCard
        fields = [
            'username',
            'name',
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
                'class': 'form-control',
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
        self.extra = 1  # Allow adding one new skill


# Create formset factory
SkillInlineFormSet = forms.inlineformset_factory(
    UserCard,
    Skill,
    form=SkillForm,
    formset=SkillFormSet,
    extra=1,
    can_delete=True,
)
