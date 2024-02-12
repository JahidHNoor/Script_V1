from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from home.models import Profile, Available_country, Setting, send_password_reset_email
from home.forms import CaptchaVerify
from user_app.models import Feature, Blocked_ip
from user_app.views.views_common_functions import get_ip_address, getting_referrer_profile_function, getting_referrer_uid_function, getting_referrer_exp_function
from home.ip_check import ip_check
from django.contrib.sites.models import Site
import uuid

# Create your views here.


                        #  Home View 

def home(request, *args, **kwargs):
    referral_code = str(kwargs.get('referral_code'))

    # Getting Features for Home Page
    features = Feature.objects.filter( is_on = True )

    context = { 
                'features': features,
               }
    try:
        profile = Profile.objects.get(referral_code = referral_code)
        request.session['ref_profile'] = str(profile.uid)
        print('id', profile.uid)

    except Exception as e:
        pass
    return render(request , "home/index.html", context)



                        # Errors Views 

def error404(request, exception):
    return render(request , "home/error_pages/error404.html")

def error500(request):
    return render(request , "home/error_pages/error500.html")

def error403(request, exception):
    return render(request , "home/error_pages/error403.html")



                        #    Register View 

def register(request):    # sourcery skip: extract-method, low-code-quality

    profile_id = request.session.get('ref_profile')
    captcha_field = CaptchaVerify()


    context = { 
                'captcha' : captcha_field,
               }
     
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('manager_dashboard')
        else:
            return redirect('dashboard')
        
    elif request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        ip_address = get_ip_address(request)
        captcha = CaptchaVerify(request.POST)
        
        if not captcha.is_valid():
            messages.error(request, "Captcha Failed.")
            return HttpResponseRedirect(request.path_info)

        # Filternig username and email 
        username_check = User.objects.filter( username = username )
        email_check = User.objects.filter( email = email )
        ip_address_check = Profile.objects.filter( ip_address = ip_address )

        #Check for errorneous inputs
        if pass1 != pass2 :
            messages.error(request, "Passwords don't match")
            return HttpResponseRedirect(request.path_info)
        
        else:

            if len(pass1) < 8 :
                messages.error(request, "Password must contains at least 8 characters.")
                return HttpResponseRedirect(request.path_info)
            
            if not username.isalnum():
                messages.error(request, "Your username can only contains letters and numbers.")
                return HttpResponseRedirect(request.path_info)
            
            if len(username) > 10:
                messages.error(request, "Your username must be under 10 characters.")
                return HttpResponseRedirect(request.path_info)
            
            if username_check.exists():
                messages.error(request, "This username is already taken.")
                return HttpResponseRedirect(request.path_info)
            
            if email_check.exists():
                messages.error(request, "This email is already taken.")
                return HttpResponseRedirect(request.path_info)

            if ip_address_check.exists():
                messages.error(request, "This IP Address is already registered.")
                return HttpResponseRedirect(request.path_info)
            
            # IP protection 
            data = ip_check(ip_address)
            

            if data['status'] == 'error':
                messages.error(request, "Something went wrong. Please try again later.")
                return HttpResponseRedirect(request.path_info)
                
            else:
                country = data[ip_address]['country']

                if data[ip_address]['vpn'] == 'yes':
                    block_ip = Blocked_ip( 
                        ip_address = ip_address,
                        block_reason = "VPN Detected",
                    )
                    block_ip.save()
                    messages.error(request, "VPN and Proxy IP are not allowed.")
                    return HttpResponseRedirect(request.path_info)

                if data[ip_address]['proxy'] == 'yes':
                    block_ip = Blocked_ip( 
                        ip_address = ip_address,
                        block_reason = "Proxy Detected"
                    )
                    block_ip.save()
                    messages.error(request, "VPN and Proxy IP are not allowed.")
                    return HttpResponseRedirect(request.path_info)
                #Create the User
            newuser = User.objects.create_user(

                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,

                )
            newuser.set_password(pass1)
            newuser.save()

            created_user = User.objects.get(username = username)
            Profile.objects.filter( user = created_user ).update(  
                ip_address = ip_address,
                country = country,
            )

            country_check = Available_country.objects.filter( name = country )

            if not country_check.exists():
                
                new_country = Available_country( 
                name = country,
                )
                new_country.save()

                # Referral system 
            if profile_id is not None:
                referred_by_profile = Profile.objects.get(uid = profile_id)
                registered_user = User.objects.get(username = username)
                registered_profile = Profile.objects.get(user = registered_user)
                registered_profile.referred_by = referred_by_profile.user
                registered_profile.save()
            messages.success(request, "Your account has been created. Please go to your email inbox and activate your account.")
            return redirect('home')

    else:
    
        return render(request , "home/register.html", context)
    



                # Login View 


def login(request):

    captcha_field = CaptchaVerify()

    context = { 
                'captcha' : captcha_field,
               }

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('manager_dashboard')
        else:
            return redirect('dashboard')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha = CaptchaVerify(request.POST)

        if not captcha.is_valid():
            messages.error(request, "Captcha Failed.")
            return HttpResponseRedirect(request.path_info)

        log_user = User.objects.filter(username = username)

        # Check for errorneous inputs

        if not log_user.exists():
            messages.error(request, "Account not Found.")
            return HttpResponseRedirect(request.path_info)

        if not log_user[0].profile.is_email_verified:
            messages.warning(request, "Your account is not verified.")
            return HttpResponseRedirect(request.path_info)

        log_user = authenticate(request, username = username, password = password)

        if log_user is not None:
            if log_user.is_staff:
                auth_login(request, log_user)
                messages.success(request, "Logged in successfully, Admin.")
                return redirect('manager_dashboard')

            else:
                request.session.set_expiry(86400)
                auth_login(request, log_user)
                messages.success(request, "Logged in successfully.")
                return redirect('dashboard')

        else:
            messages.error(request, "Invalid Credentials, Please try again.")
            return HttpResponseRedirect(request.path_info)

    else:
        return render(request , "home/login.html", context)
    



            #   Activate Email View 


def activate_email(request , email_token):
    try:
        # Getting User Ip Address 
        ip_address = get_ip_address(request)
        referral_exp_setting = Setting.objects.get( setting_name = "referral_exp_reward" )
        referral_exp = int(referral_exp_setting.setting_value)

        user = Profile.objects.get(email_token = email_token)
        referred_by = user.referred_by
        user.is_email_verified = True
        user.ip_address = ip_address
        user.save()
        referrer_profile = getting_referrer_profile_function(referred_by)
        referrer_uid = getting_referrer_uid_function(referred_by)
        referrer_exp = getting_referrer_exp_function(referred_by)
        updated_referrer_exp = referrer_exp + referral_exp
        if referrer_profile is not None:
            Profile.objects.filter( uid = referrer_uid ).update(
                exp = updated_referrer_exp
            )
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid token")
    


            # Logout View 
            
@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


# Password Reset View
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        email_check = User.objects.filter(email=email)
        if not email_check.exists():
            messages.error(request, "Account not Found.")
            return HttpResponseRedirect(request.path_info)

        user = User.objects.get( email = email)
        user_id = user.pk
        profile = Profile.objects.get( user = user_id )
        user_uid = profile.uid
        current_site = Site.objects.get_current()
        try:
            password_reset_token = str(uuid.uuid4())[:20]
            Profile.objects.filter( uid = user_uid ).update( 

                password_reset_token = password_reset_token,

            )
            send_password_reset_email(email, password_reset_token, current_site)
            messages.success(request, "Email sent successfully.")
            return HttpResponseRedirect(request.path_info)
        except Exception as e:
            print(e)
            return HttpResponse("Email address not found.")

    return render(request , "home/password_reset.html")

def reset_your_password(request, password_reset_token):
    userprofile = Profile.objects.get(password_reset_token = password_reset_token)
    user = User.objects.get(username = userprofile)
    fm = SetPasswordForm( user = user)
    if request.method == 'POST':
        fm = SetPasswordForm(user = user , data = request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request, "Your Password was reset successfully.")
            return redirect('/')
    return render(request , "home/change_password.html", {"form" : fm})