from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from home.models import Profile, Setting
from user_app.views.views_common_functions import convert_userdata_in_MK


@login_required(login_url='login')
def dashboard(request):
    profile = Profile.objects.get(user = request.user)
    current_site = Site.objects.get_current()

    # Getting User data from database
    my_referrals = profile.get_referred_porfiles()
    total_referrals = len(my_referrals)
    get_user_balance = profile.balance
    get_user_advertiser_balance = profile.advertiser_balance
    get_user_energy = profile.energy
    get_user_referral_rewards = profile.referral_rewards
    website_total_tokens_claimed_setting = Setting.objects.get( setting_name = "website_total_tokens_claimed" )


    website_total_tokens_claimed = float(website_total_tokens_claimed_setting.setting_value)
    updated_website_total_tokens_claimed = website_total_tokens_claimed + get_user_referral_rewards
    updated_total_tokens = str(updated_website_total_tokens_claimed)

    # Converting data in Million, Kilo
    balance = convert_userdata_in_MK(get_user_balance)
    advertiser_balance = convert_userdata_in_MK(get_user_advertiser_balance)
    energy = convert_userdata_in_MK(get_user_energy)
    referral_rewards = convert_userdata_in_MK(get_user_referral_rewards)
    

    # Sending user data by context  
    context = { 
                'my_referrals': my_referrals,
                'total_referrals': total_referrals,
                'current_site' : current_site,
                'balance' : balance,
                'advertiser_balance' : advertiser_balance,
                'energy' : energy,
                'referral_rewards' : referral_rewards,
               }
    
    if request.method == 'POST':

        user_uid = profile.uid
        update_user_balance_by_referral_rewards = get_user_balance + get_user_referral_rewards
        update_user_referral_rewards = 0

        Profile.objects.filter( uid = user_uid ).update(  

            balance = update_user_balance_by_referral_rewards,
            referral_rewards = update_user_referral_rewards,
        )

        Setting.objects.filter( setting_name = "website_total_tokens_claimed" ).update(
                setting_value = updated_total_tokens
        )
        messages.success(request, f"{referral_rewards} tokens have been added to your balance.")
        return HttpResponseRedirect(request.path_info)

    return render(request , "user/dashboard.html" , context)