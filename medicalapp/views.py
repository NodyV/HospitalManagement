import re
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models import Count, Max
from django.db.models import Q


def index(request):

    return render(request, 'index.html')


def login(request):

    if request.POST:
        email = request.POST['txtEmail']
        pwd = request.POST['txtPassword']

        user = authenticate(username=email, password=pwd)
        if user is None:
            messages.info(request, 'Username or password incorrect')
        else:
            user_data = CustomUser.objects.get(username=email)
            if user_data.is_superuser == 1:
                return redirect("/adminhome")
            elif user_data.user_type == "Client":
                r = Registration.objects.get(email=email)
                request.session["id"] = r.id
                request.session["name"] = r.name
                data = Registration.objects.values('name')
                print(data)
                return redirect("/userhome")
            elif user_data.user_type == "Doctor":
                r = Doctor.objects.get(email=email)
                request.session["id"] = r.id
                request.session["name"] = r.name
                return redirect("/doctorhome")
            elif user_data.user_type == "Pharmacist":
                r = Pharmacist.objects.get(email=email)
                request.session["id"] = r.id
                request.session["name"] = r.name
                return redirect("/pharmacisthome")

                
    return render(request, 'login.html')


def registration(request):

    if request.POST:
        name = request.POST['txtName']
        gender = request.POST['gender']
        house = request.POST['txtHouse']
        place = request.POST['txtPlace']
        phone = request.POST['txtPhone']
        email = request.POST['txtEmail']
        pwd = request.POST['txtPassword']
        user = authenticate(username=email, password=pwd)
        if user is None:
            try:
                u = CustomUser.objects.create_user(
                        password=pwd, username=email,user_type='Client')
                u.save()
                r = Registration.objects.create(
                    name=name, gender=gender, house=house, place=place, phone=phone, email=email,user=u)
                r.save()
            except:
                messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'User already registered')
    return render(request, 'registration.html')


def adminhome(request):

    return render(request, 'adminhome.html')

def admindoctor(request):

    if request.POST:
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        phone = request.POST['txtContact']
        qual = request.POST['txtQualification']
        exp = request.POST['txtExperience']
        email = request.POST['txtEmail']
        specialization = request.POST['txtSpecialization']
        pwd = request.POST['txtPassword']
        user = authenticate(username=email, password=pwd)
        if user is None:
            try:
                u = CustomUser.objects.create_user(
                        password=pwd, username=email,user_type="Doctor")
                u.save()
                r = Doctor.objects.create(
                    name=name, address=address, phone=phone, email=email, qualification=qual, experience=exp,user=u,specialization=specialization)
                r.save()
            except:
                messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'User already registered')
    data = Doctor.objects.filter(user__is_active=True)
    return render(request, 'admindoctor.html', {"data": data})

def adminupdatedoctor(request):
    id = request.GET['id']
    data = Doctor.objects.get(id=id)
    if request.POST:
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        phone = request.POST['txtContact']
        qual = request.POST['txtQualification']
        exp = request.POST['txtExperience']
        email = request.POST['txtEmail']
        specialization = request.POST['txtSpecialization']
        # pwd = request.POST['txtPassword']
        data.name = name
        data.address = address
        data.phone = phone
        data.email = email
        data.qualification = qual
        data.experience = exp
        data.specialization=specialization
        uid = data.user.id
        user =CustomUser.objects.get(id = uid)
        user.username = email
        # user.set_password(pwd)
        data.save()
        user.save()
        return redirect("/admindoctor")
    return render(request, 'adminupdatedoctor.html', {"data":data})

def admindeletedoctor(request):
    id = request.GET['id']
    data = CustomUser.objects.get(id=id)
    data.is_active = 0
    data.save()
    return redirect("/admindoctor")

def adminPharmacist(request):

    if request.POST:
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        phone = request.POST['txtContact']
        qual = request.POST['txtQualification']
        exp = request.POST['txtExperience']
        email = request.POST['txtEmail']
        pwd = request.POST['txtPassword']
        user = authenticate(username=email, password=pwd)
        if user is None:
            try:
                u = CustomUser.objects.create_user(
                        password=pwd, username=email,user_type="Pharmacist")
                u.save()
                r = Pharmacist.objects.create(
                    name=name, address=address, phone=phone, email=email, qualification=qual, experience=exp,user=u)
                r.save()
            except:
                messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'User already registered')
    data = Pharmacist.objects.filter(user__is_active=True)
    return render(request, 'adminPharmacist.html', {"data": data})

def adminupdatePharmacist(request):
    id = request.GET['id']
    data = Pharmacist.objects.get(id=id)
    if request.POST:
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        phone = request.POST['txtContact']
        qual = request.POST['txtQualification']
        exp = request.POST['txtExperience']
        email = request.POST['txtEmail']
        # pwd = request.POST['txtPassword']
        data.name = name
        data.address = address
        data.phone = phone
        data.email = email
        data.qualification = qual
        data.experience = exp
        uid = data.user.id
        user =CustomUser.objects.get(id = uid)
        user.username = email
        # user.set_password(pwd)
        data.save()
        user.save()
        return redirect("/adminPharmacist")
    return render(request, 'adminupdatePharmacist.html', {"data":data})

def admindeletePharmacist(request):
    id = request.GET['id']
    data = CustomUser.objects.get(id=id)
    data.is_active = 0
    data.save()
    return redirect("/adminPharmacist")

def adminpatient(request):
    patient_data = Registration.objects.filter()
    return render(request, 'adminpatient.html', {"patient": patient_data})

def adminbookings(request):
    booking = Booking.objects.filter(status='Consulted')
    return render(request, 'adminbookings.html', {"booking": booking})

def adminviewpres(request):
    id = request.GET.get('id')
    booking = Prescription.objects.get(bid__id=id)
    return render(request, 'adminviewpres.html', {"prescription": booking})

def adminviewmedpres(request):
    id = request.GET.get('id')
    medData = PresMedicine.objects.filter(prescription__id=id)
    status = medData[0].status
    total = 0
    for m in medData:
        rate = int(m.medicine.rate)
        qty = int(m.qty)
        cost = rate * qty
        total += cost
    return render(request, 'adminviewmedpres.html', {"medData":medData, "status":status,"prescription":id, "total":total})

def userhome(request):

    return render(request, 'userhome.html')

def usersearch(request):
    doctor_data = Doctor.objects.filter(user__is_active=1)
    if request.POST:
        search = request.POST['search']
        doctor_data = Doctor.objects.filter(Q(user__is_active=1)&Q(Q(name__contains=search)|Q(specialization__contains=search)))

    return render(request, 'usersearch.html', {"doctor_data": doctor_data})

def userbookingdate(request):
    did = request.GET.get("id")
    doc = Doctor.objects.get(id=did)
    id = request.session["id"]
    rid = Registration.objects.get(id=id)
    if request.POST:
        bdate = request.POST.get('txtDate')
        amt = 200
        pdate = Booking.objects.filter(regid=id).order_by('-bookingdate')[:1]
        if pdate is not None:
            amt = 200
        else:
            from datetime import datetime
            bdate = datetime.strptime(bdate, '%d/%m/%y %H:%M:%S')
            pdate = datetime.strptime(pdate, '%d/%m/%y %H:%M:%S')
            diff = bdate-pdate
            if diff <= 14:
                amt = 0
            else:
                amt = 200
        token = 1
        if Booking.objects.filter(docid=did,bookingdate=bdate).exists():
            tokmax = Booking.objects.filter(docid=did,bookingdate=bdate).order_by("-id")[0]
            token += tokmax.token
        b = Booking.objects.create(
            regid=rid, docid=doc, bookingdate=bdate, status='Booked',token=token)
        b.save()
        if amt != 0:
            return redirect('/payment?amt='+str(amt))
        else:
            return redirect('/userbooking')
    return render(request, 'userbookingdate.html')

def payment(request):
    amt = request.GET.get('amt')
    if request.POST:
        bid = Booking.objects.aggregate(bid_max=Max('id'))
        print(bid)
        bid = Booking.objects.get(id=bid['bid_max'])
        print(bid)
        try:
            p = Payment.objects.create(bid=bid, status='Booked')
            p.save()
        except:
            import sys
            e = sys.exc_info()[0]
            print(e)
            messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'Payment success')
            return redirect('/userbooking')
    return render(request, 'payment.html', {"amt": amt})

def userbooking(request):
    id = request.session["id"]
    rid = Registration.objects.get(id=id)
    booking = Booking.objects.filter(regid=rid,status='Booked')
    return render(request, 'userbooking.html', {"booking": booking})

def userbookinghistory(request):
    id = request.session["id"]
    rid = Registration.objects.get(id=id)
    booking = Booking.objects.filter(regid=rid,status='Consulted')
    return render(request, 'userbookinghistory.html', {"booking": booking})


def userviewpres(request):
    id = request.GET.get('id')
    booking = Prescription.objects.get(bid__id=id)
    return render(request, 'userviewpres.html', {"prescription": booking})

def userviewmedpres(request):
    id = request.GET.get('id')
    medData = PresMedicine.objects.filter(prescription__id=id)
    status = medData[0].status
    total = 0
    for m in medData:
        rate = int(m.medicine.rate)
        qty = int(m.qty)
        cost = rate * qty
        total += cost
    return render(request, 'userviewmedpres.html', {"medData":medData, "status":status,"prescription":id, "total":total})

def userbuymedicine(request):
    amt = request.GET.get('amt')
    pid = request.GET.get('id')
    if request.POST:
        remed = PresMedicine.objects.filter(prescription__id=pid).update(status='Bought')
        return redirect('/userbookinghistory')
    return render(request, 'payment.html', {"amt": amt})

def doctorhome(request):

    return render(request, 'doctorhome.html')

def doctorbooking(request):
    id = request.session["id"]
    rid = Doctor.objects.get(id=id)
    booking = Booking.objects.filter(docid=rid, status='Booked')
    return render(request, 'doctorbooking.html', {"booking": booking})


def doctorpatient(request):
    id = request.GET.get('id')
    booking = Booking.objects.get(id=id)
    regid = booking.regid
    pbooking = Booking.objects.filter(regid=regid).exclude(id=id).order_by('-bookingdate')
    if request.POST:
        return redirect('/doctorprescription?id='+str(id))
    return render(request, 'doctorpatient.html', {"booking": booking, "pbooking": pbooking})


def doctorviewprescription(request):
    id = request.GET.get('id')
    booking = Prescription.objects.get(bid__id=id)
    return render(request, 'doctorviewprescription.html', {"prescription": booking})


def doctorprescription(request):
    bookingid = request.GET.get('id')
    bid = Booking.objects.get(id=bookingid)
    if request.POST:
        diagnosis = request.POST.get('txtDiagnosis')
        try:
            p = Prescription.objects.create(
                bid=bid, diagnosis=diagnosis)
            p.save()
        except:
            import sys
            e = sys.exc_info()[0]
            print(e)
            messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'Prescription added')
            return redirect(f'/doctorprescribemed?id={p.id}')
    return render(request, 'doctorprescription.html')

def doctorprescribemed(request):
    pid = request.GET['id']
    pre = Prescription.objects.get(id=pid)
    if request.POST:
        me = request.POST['txtMed']
        desc = request.POST['txtDesc']
        qty = request.POST['txtQty']
        med = Medicine.objects.get(id=me)
        ins = PresMedicine.objects.create(prescription=pre,medicine=med,desc=desc,qty=qty)
        ins.save()
    data = Medicine.objects.all()
    medData = PresMedicine.objects.filter(prescription=pid)
    bookid = pre.bid.id
    return render(request, 'doctorprescribemed.html', {"data": data, "medData": medData, "bookid": bookid})

def doctorbookingstatus(request):
    id = request.GET['id']
    booking = Booking.objects.get(id=id)
    booking.status = 'Consulted'
    booking.save()
    return redirect('/doctorbooking')

def doctorbookinghistory(request):
    id = request.session["id"]
    rid = Doctor.objects.get(id=id)
    booking = Booking.objects.filter(docid=rid, status='Consulted')
    return render(request, 'doctorbookinghistory.html', {"booking": booking})


def doctorpatienthistory(request):
    id = request.GET.get('id')
    booking = Booking.objects.get(id=id)
    regid = booking.regid
    pbooking = Booking.objects.filter(regid=regid).order_by('-bookingdate')
    if request.POST:
        return redirect('/doctorprescription?id='+str(id))
    return render(request, 'doctorpatienthistory.html', {"booking": booking, "pbooking": pbooking})

def doctorviewmedpres(request):
    id = request.GET.get('id')
    medData = PresMedicine.objects.filter(prescription__id=id)
    return render(request, 'doctorviewmedpres.html', {"medData":medData})
















def pharmacisthome(request):

    return render(request, 'pharmacisthome.html')

def pharmacistAddMed(request):
    msg = ""
    if request.POST:
        name = request.POST['txtName']
        desc = request.POST['txtDesc']
        rate = request.POST['txtRate']
        data = Medicine.objects.create(name=name, desc=desc, rate=rate)
        data.save()
        msg = "Medicine Details Added"
    return render(request, 'pharmacistAddMed.html',{"msg":msg})

def pharmacistViewMed(request):
    data = Medicine.objects.all()
    return render(request, 'pharmacistViewMed.html',{"data":data})

def pharmacistupdatemedicine(request):
    id = request.GET['id']
    data = Medicine.objects.get(id=id)
    if request.POST:
        name = request.POST['txtName']
        desc = request.POST['txtDesc']
        rate = request.POST['txtRate']
        data.name = name
        data.rate = rate
        data.desc = desc
        data.save()
        return redirect("/pharmacistViewMed")
    return render(request, 'pharmacistupdatemedicine.html',{"data":data})

def pharmacistdeletemedicine(request):
    id = request.GET['id']
    status = request.GET['status']
    data = Medicine.objects.get(id=id)
    data.status = status
    data.save()
    return redirect("/pharmacistViewMed")



















































































































