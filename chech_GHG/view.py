from django.conf import settings
from datetime import datetime
from json import loads, dumps
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, View
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.db import IntegrityError
from product.models import Product
from .models import AboutUs,Timesheet
# Create your views here.
def home(request):

    return render(request, "index.html", {'title': "Baba Barghi"})


def about_us(request):
    about = AboutUs.objects.all()
    return render(request, "about-us.html", {"title": "درباره ما","about":about})


def contact_us(request):
    timesheet= Timesheet.objects.all()
    return render(request, "contact.html", {"title": "تماس با ما","timesheet":timesheet})


@require_http_methods(["POST"])
def send_comment(request):
    # if request.uesr.is_annonymos:
    #     author = request.POST.get("author", None)
    #
    # else:
    #     author = request.user
    try:
        email = request.POST.get("email", None)
        comment = request.POST.get("comment", None)
        current_site = get_current_site(request)
        # message = render_to_string('contact.html',{
        #     'user': email,
        #     'domain': current_site.domain})

        send_mail(email, comment, settings.EMAIL_HOST_USER, ["info.bababarghi@gmail.com",],auth_password="Qwert1234@",)

        # messages.success(request, "Register Successfully!")
        return HttpResponse('dame shoma babat feedbacket garm ')


    except IntegrityError as e:
        messages.error(request, f"{e}")
        return redirect('/')
