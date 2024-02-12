from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from home.models import Profile, Setting
from user_app.models import Rps_history, Feature
from user_app.views.views_common_functions import bonus_percent_function, getting_referrer_profile_function, getting_referrer_referral_rewards_function, getting_referrer_uid_function


@login_required(login_url='login')
def rps(request):
   # sourcery skip: hoist-statement-from-if, merge-else-if-into-elif, remove-redundant-fstring

    # Getting user account access and user data
    profile = Profile.objects.get(user = request.user)
    user_uid = profile.uid
    user_balance = profile.balance
    user_energy = profile.energy
    user_level = profile.level
    user_exp = profile.exp
    last_rps_played = int(profile.last_rps_played)
    referred_by = profile.referred_by


    # Getting Referrer account access
    referrer_profile = getting_referrer_profile_function(referred_by)
    referral_rewards = getting_referrer_referral_rewards_function(referred_by)
    referrer_uid = getting_referrer_uid_function(referred_by)

    # Getting Settings 
    feature_rps = Feature.objects.get( feature_name = "rps" )
    rps_token_setting = Setting.objects.get( setting_name = "rps_token_reward" )
    rps_exp_setting = Setting.objects.get( setting_name = "rps_exp_reward" )
    rps_energy_cost_setting = Setting.objects.get( setting_name = "rps_energy_cost" )
    referral_commission_setting = Setting.objects.get( setting_name = "referral_commission" )
    website_total_tokens_claimed_setting = Setting.objects.get( setting_name = "website_total_tokens_claimed" )

    # Converting Settings Value 
    rps_token = float(rps_token_setting.setting_value)
    rps_exp = float(rps_exp_setting.setting_value)
    level_bonus = bonus_percent_function(rps_token, user_level)
    rps_energy_cost = float(rps_energy_cost_setting.setting_value)
    referral_commission = float(referral_commission_setting.setting_value)
    website_total_tokens_claimed = float(website_total_tokens_claimed_setting.setting_value)

    context = { 
                'feature_rps' : feature_rps,
                'rps_token' : rps_token,
                'level_bonus' : level_bonus,
                'rps_energy_cost' : rps_energy_cost,
               }


    if request.method == 'POST':
        current_time = request.POST.get('current_time')
        rps_result = request.POST.get('rps_result')

        # Updating values to send to Database 
        commission_amount = bonus_percent_function(rps_token, referral_commission)
        update_referral_rewards = referral_rewards + commission_amount
        rps_violation_checker = last_rps_played + 2
        update_last_rps_played = int(current_time)
        update_user_energy = user_energy - rps_energy_cost
        update_user_exp = user_exp + rps_exp
        update_user_balance = user_balance + rps_token + level_bonus
        updated_website_total_tokens_claimed = website_total_tokens_claimed + rps_token
        updated_total_tokens = str(updated_website_total_tokens_claimed)


        if rps_violation_checker > update_last_rps_played:
            Profile.objects.filter( uid = user_uid ).update(
                is_account_banned = True ,
            )
            return_message = "Cheating has been detected in your activities."
            icon_type = "error"
            message_type = "Violation detected..."

        elif rps_result == "Draw":
                Profile.objects.filter( uid = user_uid ).update(  
                    last_rps_played = update_last_rps_played,
                )
                return_message = "Draw, Very close."
                icon_type = "warning"
                message_type = "Opps..."
                
                #Create the log
                create_rps_log = Rps_history( user_uid = user_uid )
                create_rps_log.save()

        elif rps_result == "Lose":
            
            if rps_energy_cost > user_energy:
                # If user don't have enough energy 
                Profile.objects.filter( uid = user_uid ).update(  
                last_rps_played = update_last_rps_played,
                )
                return_message = "Not enough energy."
                icon_type = "warning"
                message_type = "Opps..."
            
            else:
                Profile.objects.filter( uid = user_uid ).update(  
                    energy = update_user_energy,
                    exp = update_user_exp,
                    last_rps_played = update_last_rps_played,
                )
                return_message = "You lose, Better luck next time."
                icon_type = "warning"
                message_type = "Opps..."

                #Create the log
                create_rps_log = Rps_history( user_uid = user_uid )
                create_rps_log.save()
        
        else:

            if rps_energy_cost > user_energy:
                # If user don't have enough energy 
                Profile.objects.filter( uid = user_uid ).update(  
                last_rps_played = update_last_rps_played,
                )
                return_message = "Not enough energy."
                icon_type = "warning"
                message_type = "Opps..."

            else:
                # Updating User Account in Database
                Profile.objects.filter( uid = user_uid ).update(  

                    balance = update_user_balance,
                    energy = update_user_energy,
                    exp = update_user_exp,
                    last_rps_played = update_last_rps_played,

                )
                
                Setting.objects.filter( setting_name = "website_total_tokens_claimed" ).update(
                setting_value = updated_total_tokens
                )

                #Create the log
                create_rps_log = Rps_history( user_uid = user_uid )
                create_rps_log.save()

                if referrer_profile is not None:
                    Profile.objects.filter( uid = referrer_uid ).update(
                        referral_rewards = update_referral_rewards
                    )
                return_message = f"{rps_token + level_bonus} tokens have been added to your balance."
                message_type = "Congratulaions..."
                icon_type = "success"
        return JsonResponse({"return_message": return_message, "message_type": message_type, "icon_type": icon_type,})


    return render(request , "user/rps.html" , context)
