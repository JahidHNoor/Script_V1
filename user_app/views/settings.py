from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from home.models import Profile
from django.contrib.auth.models import User



@login_required(login_url='login')
def settings(request):

    # Getting user account access
    profile = Profile.objects.get(user = request.user)
    user_username = profile.user



    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')


        User.objects.filter(username = user_username).update(
            first_name = first_name,
            last_name = last_name,
        )
        messages.success(request, "Account Updated Successfully.")
        return HttpResponseRedirect(request.path_info)

    return render(request , "user/settings.html")
