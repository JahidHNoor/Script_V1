from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from home.models import Profile


@login_required(login_url='login')
def profile(request):
    profile = Profile.objects.get(user = request.user)
    user_uid = profile.uid
    level = profile.level
    exp = profile.exp
    levelx = level - 1

    level_up_button = "hide"
    if level < 25:
        total_exp_required = 5 + 10*level*level + 5*(levelx)*level
        exp_required_for_next_level = total_exp_required - exp
        level_message = "There will be upgrade button once you have enough exp points. Level up to earn more rewards."
        if exp >= total_exp_required:
            exp_required_for_next_level = 0
            level_message = "You are able to level up."
            level_up_button = "show"
    else:
        total_exp_required = 1
        exp_required_for_next_level = 0
        level_message = "You have reached the maximum level."
    

    progress_percent = int((exp/total_exp_required) * 100)
    progress_percent = min(progress_percent, 100)

    context = {
        "total_exp_required" : total_exp_required,
        "exp_required_for_next_level" : exp_required_for_next_level,
        "level_message" : level_message,
        "progress_percent" : progress_percent,
        "level_up_button" : level_up_button,
    }

    if request.method == 'POST':


        # Updating values to send to Database 
        new_level = level + 1
        updated_exp = exp - total_exp_required


        if total_exp_required > exp:
            Profile.objects.filter( uid = user_uid ).update(
                is_account_banned = True ,
            )
            messages.error(request, "Cheating Detected.")

        else:
            # Updating User Account in Database
            Profile.objects.filter( uid = user_uid ).update(  
                level = new_level,
                exp = updated_exp,
            )
            messages.success(request, f"Level upgraded from {level} to {new_level}.")
        return HttpResponseRedirect(request.path_info)

    return render(request , "user/profile.html" , context )