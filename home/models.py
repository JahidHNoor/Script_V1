from django.db import models
from django.contrib.auth.models import User
from core.models import core_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
import uuid
from core.emails import *

# Create your models here.

class Profile(core_model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="profile")
    balance = models.FloatField(max_length=20 , default=0)
    advertiser_balance = models.FloatField(max_length=20 , default=0)
    energy = models.FloatField(max_length=20 , default=0 , blank=True, null=True)
    level = models.IntegerField(default=0 , blank=True, null=True)
    exp = models.IntegerField(default=0 , blank=True, null=True)
    ip_address = models.CharField( max_length=100 , null=True , blank=True )
    country = models.CharField( max_length=100 , null=True , blank=True )
    referral_rewards = models.FloatField(max_length=20 , default=0 , blank=True, null=True)
    referral_code = models.CharField( max_length=100 , null=True , blank=True )
    referred_by = models.ForeignKey(User, on_delete= models.CASCADE, blank=True, null=True, related_name='ref_by')
    is_email_verified = models.BooleanField(default=False)
    is_account_banned = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    password_reset_token = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True )
    last_rps_played = models.IntegerField( default = 1683179400 )
    last_tic_tac_toe_played = models.IntegerField( default = 1683179400 )


    def __str__(self):
        return self.user.username
    

    def get_referred_porfiles(self):
        qs = Profile.objects.all()

        return [profile for profile in qs if profile.referred_by == self.user]
    

    def save(self, *args, **kwargs):
        if self.email_token is None:
            email_token = str(uuid.uuid4())[:20]
            self.email_token = email_token

        if self.referral_code is None:
            referral_code = str(uuid.uuid4())[:20]
            self.referral_code = referral_code

        super().save(*args, **kwargs)


@receiver( post_save, sender = User)
def send_email_token( sender, instance , created , **kwargs):
    current_site = Site.objects.get_current()
    try:
        if created:
            email_token = str(uuid.uuid4())[:20]
            Profile.objects.create(
                user=instance,
                email_token=email_token,
                referral_code=email_token,
            )
            email = instance.email
            send_account_activation_email(email, email_token, current_site)
    except Exception as e:
        print(e)


class Setting(models.Model):
    setting_name = models.CharField( max_length=100 , null=True , blank=True, default= "setting name")
    setting_value = models.TextField( null=True , blank=True, default= "setting value" )


    def __str__(self):
        return self.setting_name



class Available_country(models.Model):
    name = models.CharField(max_length=100 , null=True , blank=True)

    def __str__(self):
        return self.name

