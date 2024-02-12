from home.models import Setting, Profile
from user_app.views.views_common_functions import convert_userdata_in_MK
from django.db.models import Q

def website_details(request):

    users = Profile.objects.all()
    total_users = len(list(users))


    # Getting Settings 
    website_name_setting = Setting.objects.get( setting_name = "website_name" )
    website_description_setting = Setting.objects.get( setting_name = "website_description" )
    website_total_tokens_claimed_setting = Setting.objects.get( setting_name = "website_total_tokens_claimed" )



    # Converting Settings Value 
    website_name = website_name_setting.setting_value
    website_description = website_description_setting.setting_value
    website_total_users = convert_userdata_in_MK(total_users)
    website_total_tokens_claimed = convert_userdata_in_MK(float(website_total_tokens_claimed_setting.setting_value))

    return { 
            'website_name' : website_name,
            'website_description' : website_description,
            'website_total_users': website_total_users,
            'website_total_tokens_claimed': website_total_tokens_claimed,
        
        }