from django import forms


class GetEmailForm(forms.Form):
    email_field = forms.EmailField(required=True)


class ResetPasswordForm(forms.Form):
    password_field = forms.CharField(
        max_length=32, label="Reset Password:", widget=forms.PasswordInput)
    confirm_field = forms.CharField(
        max_length=32, label="Confirm Password:", widget=forms.PasswordInput)
