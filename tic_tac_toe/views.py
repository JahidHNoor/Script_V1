from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tic_tac_toe.models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from home.models import Profile, Setting
from django.contrib.sites.models import Site
from user_app.models import Tic_tac_toe_history, Feature
from user_app.views.views_common_functions import bonus_percent_function, getting_referrer_profile_function, getting_referrer_referral_rewards_function, getting_referrer_uid_function


# Create your views here.
@login_required(login_url='login')
def tic_tac_toe(request):

    # Getting user account access and user data
    profile = Profile.objects.get(user = request.user)
    user_uid = profile.uid
    user_balance = profile.balance
    user_energy = profile.energy
    user_level = profile.level
    user_exp = profile.exp
    last_tic_tac_toe_played = int(profile.last_tic_tac_toe_played)
    referred_by = profile.referred_by


    # Getting Referrer account access
    referrer_profile = getting_referrer_profile_function(referred_by)
    referral_rewards = getting_referrer_referral_rewards_function(referred_by)
    referrer_uid = getting_referrer_uid_function(referred_by)

    # Getting Settings 
    feature_tic_tac_toe = Feature.objects.get( feature_name = "tic_tac_toe" )
    tic_tac_toe_token_setting = Setting.objects.get( setting_name = "tic_tac_toe_token_bet" )
    tic_tac_toe_exp_setting = Setting.objects.get( setting_name = "tic_tac_toe_exp_reward" )
    tic_tac_toe_energy_cost_setting = Setting.objects.get( setting_name = "tic_tac_toe_energy_cost" )
    referral_commission_setting = Setting.objects.get( setting_name = "referral_commission" )
    website_total_tokens_claimed_setting = Setting.objects.get( setting_name = "website_total_tokens_claimed" )

    # Converting Settings Value 
    tic_tac_toe_token = float(tic_tac_toe_token_setting.setting_value)
    tic_tac_toe_exp = float(tic_tac_toe_exp_setting.setting_value)
    level_bonus = bonus_percent_function(tic_tac_toe_token, user_level)
    tic_tac_toe_win_rewards = (tic_tac_toe_token + level_bonus) * 2
    tic_tac_toe_energy_cost = float(tic_tac_toe_energy_cost_setting.setting_value)
    referral_commission = float(referral_commission_setting.setting_value)
    website_total_tokens_claimed = float(website_total_tokens_claimed_setting.setting_value)

    context = { 
                'feature_tic_tac_toe' : feature_tic_tac_toe,
                'tic_tac_toe_token' : tic_tac_toe_token,
                'level_bonus' : level_bonus,
                'tic_tac_toe_win_rewards' : tic_tac_toe_win_rewards,
                'tic_tac_toe_energy_cost' : tic_tac_toe_energy_cost,
               }


    if request.method == "POST":
        roomId = request.POST.get("room-id", None)
        username = request.POST.get("player-name", "Unknown Player")
        if(roomId):
            try:
                room = Tic_tac_toe_room.objects.get(id=roomId)
                return redirect(f"/user/tic_tac_toe/game/{username}/{room.id}/")
            except Tic_tac_toe_room.DoesNotExist:
                messages.error(request, "Room does not exist.")
                return redirect("tic_tac_toe")
                
        else:
            room = Tic_tac_toe_room.objects.create()
            return redirect(f"/user/tic_tac_toe/game/{username}/{room.id}/")
    return render(request , "user/tic_tac_toe.html" , context)




# Tic Tac Toe Game Page 

@login_required(login_url='login')
def tic_tac_toe2(request, id=None, username=None):
    current_site = Site.objects.get_current()
    feature_tic_tac_toe = Feature.objects.get( feature_name = "tic_tac_toe" )
    try:
        room = Tic_tac_toe_room.objects.get(id=id)
        context = { 
                "room": room,
                "name": username,
                "current_site" : current_site,
                'feature_tic_tac_toe' : feature_tic_tac_toe,
            }
        
        return render(request, "user/tic_tac_toe_game_page.html", context)
    
    
    except Tic_tac_toe_room.DoesNotExist:

        messages.error(request, "Room does not exist.")
        return HttpResponseRedirect(request.path_info)