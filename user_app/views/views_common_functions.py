from home.models import Profile

# General functions which will be used in many views 

# Function to convert bonus amount 
def bonus_percent_function(a,b):
    divided_amount = a/100
    return divided_amount * b

# Function to commission amount 
def commission_amount_function(a,b):
    divided_amount = a/100
    return divided_amount * b


# Function of Converting data in Million, Kilo
def convert_userdata_in_MK(a):
    if a > 10000 and a < 1000000:
        converted_data = a / 1000
        round_data = round(converted_data,2)
        b = f"{round_data} K"
    elif a > 1000000 and a < 1000000000:
        converted_data = a / 1000000
        round_data = round(converted_data,2)
        b = f"{round_data} M"
    elif a > 1000000000:
        converted_data = a / 1000000000
        round_data = round(converted_data,2)
        b = f"{round_data} B"
    else:
        b = round(a,2)
    return (b)


        # Functions of Getting Referrer account access
def getting_referrer_profile_function(a):
    referrer_check = Profile.objects.filter(user = a)
    return Profile.objects.get(user = a) if referrer_check.exists() else None

def getting_referrer_referral_rewards_function(a):
    referrer_check = Profile.objects.filter(user = a)
    if referrer_check.exists():
        referrer_profile = Profile.objects.get(user = a)
        referral_rewards = referrer_profile.referral_rewards
    else:
        referrer_profile = None
        referral_rewards = 0
    return referral_rewards

def getting_referrer_exp_function(a):
    referrer_check = Profile.objects.filter(user = a)
    if referrer_check.exists():
        referrer_profile = Profile.objects.get(user = a)
        referrer_exp = referrer_profile.exp
    else:
        referrer_profile = None
        referrer_exp = 0
    return referrer_exp

def getting_referrer_uid_function(a):
    referrer_check = Profile.objects.filter(user = a)
    if referrer_check.exists():
        referrer_profile = Profile.objects.get(user = a)
        referrer_uid = referrer_profile.uid
    else:
        referrer_profile = None
        referrer_uid = None
    return referrer_uid


def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    return (
        user_ip_address.split(',')[0]
        if user_ip_address
        else request.META.get('REMOTE_ADDR')
    )