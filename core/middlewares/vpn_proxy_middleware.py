from user_app.views.views_common_functions import get_ip_address
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from user_app.models import Blocked_ip


def vpn_proxy_checker(get_response):
    def checking(request):
        if request.method == 'POST':
            ip_address = get_ip_address(request)
            ip_check = Blocked_ip.objects.filter(ip_address = ip_address)
            if ip_check.exists():
                auth_logout(request)
                messages.error(request, "This IP Address is not allowed.")
                return redirect('/')
        response = get_response(request)
        return response
    return checking
