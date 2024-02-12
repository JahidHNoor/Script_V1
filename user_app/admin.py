from django.contrib import admin
from user_app.models import *



class RpsAdmin(admin.ModelAdmin):
    readonly_fields = ('rps_claim_time', )

class Tic_tac_toeAdmin(admin.ModelAdmin):
    readonly_fields = ('tic_tac_toe_match_time', )

class FeatureAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )

class Blocked_ipAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


# Register your models here.
admin.site.register(Rps_history, RpsAdmin),
admin.site.register(Tic_tac_toe_history, Tic_tac_toeAdmin),
admin.site.register(Feature, FeatureAdmin),
admin.site.register(Blocked_ip, Blocked_ipAdmin),
