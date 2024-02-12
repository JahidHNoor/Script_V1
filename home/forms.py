from django import forms
from captcha.fields import ReCaptchaField

class CaptchaVerify(forms.Form):
    captcha = ReCaptchaField()