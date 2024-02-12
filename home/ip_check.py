from home.models import Setting
import requests

# Create your views here.

# Password Reset View
def ip_check(ip_address):

        # Getting Settings 
    proxycheck_setting = Setting.objects.get( setting_name = "proxycheck_api" )

    proxycheck_api = proxycheck_setting.setting_value

    # Call proxycheck.io API to check the IP address
    url = f'https://proxycheck.io/v2/{ip_address}?key={proxycheck_api}&vpn=3&asn=1&cur=1&risk=1&tag=UserCheck'
    response = requests.get(url)
    return response.json()


