"""medical_appointment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from medicalapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index),
    path('login', views.login),
    path('registration', views.registration),

    path('adminhome', views.adminhome),

    path('admindoctor', views.admindoctor),
    path('adminupdatedoctor', views.adminupdatedoctor),
    path('admindeletedoctor', views.admindeletedoctor),
    path('adminupdatePharmacist', views.adminupdatePharmacist),
    path('adminPharmacist', views.adminPharmacist),
    path('admindeletePharmacist', views.admindeletePharmacist),
    path('adminpatient', views.adminpatient),
    path('adminbookings', views.adminbookings),
    path('adminviewpres', views.adminviewpres),
    path('adminviewmedpres', views.adminviewmedpres),


    path('userhome', views.userhome),
    path('usersearch', views.usersearch),
    path('userbookingdate', views.userbookingdate),
    path('payment', views.payment),
    path('userbooking', views.userbooking),
    path('userbookinghistory', views.userbookinghistory),
    path('userviewpres', views.userviewpres),
    path('userviewmedpres', views.userviewmedpres),
    path('userbuymedicine', views.userbuymedicine),


    path('doctorhome', views.doctorhome),
    path('doctorbooking', views.doctorbooking),
    path('doctorpatient', views.doctorpatient),
    path('doctorviewprescription', views.doctorviewprescription),
    path('doctorprescription', views.doctorprescription),
    path('doctorprescribemed', views.doctorprescribemed),
    path('doctorbookingstatus', views.doctorbookingstatus),
    path('doctorbookinghistory', views.doctorbookinghistory),
    path('doctorpatienthistory', views.doctorpatienthistory),
    path('doctorviewmedpres', views.doctorviewmedpres),



    path('pharmacisthome', views.pharmacisthome),
    path('pharmacistAddMed', views.pharmacistAddMed),
    path('pharmacistViewMed', views.pharmacistViewMed),
    path('pharmacistupdatemedicine', views.pharmacistupdatemedicine),
    path('pharmacistdeletemedicine', views.pharmacistdeletemedicine),
]
