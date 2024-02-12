from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from home.models import *
from user_app.views.views_common_functions import *


@login_required(login_url='login')
def history(request):
    return render(request , "user/history.html")