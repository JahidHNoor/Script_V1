from django.db import models
from core.models import core_model
from django.contrib.auth.models import User

# Create your models here.


class Rps_history(core_model):
    user_uid = models.CharField(max_length=100 , null=True , blank=True)
    rps_claim_time = models.DateTimeField(auto_now_add=True, null=True, blank=True )

    def __str__(self):
        return f"{self.uid}"

class Tic_tac_toe_history(core_model):
    user_uid = models.CharField(max_length=100 , null=True , blank=True)
    opponent_uid = models.CharField(max_length=100 , null=True , blank=True)
    match_status = models.CharField(max_length=100 , null=True , blank=True)
    tic_tac_toe_match_time = models.DateTimeField(auto_now_add=True, null=True, blank=True )

    def __str__(self):
        return f"{self.uid}"

        
class Feature(models.Model):
    feature_name = models.CharField(max_length=100, default="Name of feature. Must be in lowercase." )
    feature_title = models.CharField(max_length=100, default="Title of feature. It will shown in Home features." )
    feature_description = models.TextField(default="Write your Feature description here. It will be shown on the HomePage.")
    feature_icon = models.CharField(max_length=100, default="Icon of the feature." )
    is_on = models.BooleanField(default=True)


    def __str__(self):
        return self.feature_name
    
class Blocked_ip(models.Model):
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    block_reason = models.CharField(max_length=100, default="Blocked by Admin." )

    def __str__(self):
        return self.ip_address