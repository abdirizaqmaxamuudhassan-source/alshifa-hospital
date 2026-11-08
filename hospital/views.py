import csv, json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from .models import *
from .forms import *

def is_staff_role(u):
    return u.is_authenticated and (u.is_superuser or u.groups.filter(name__in=["Doctor","Receptionist"]).exists())
staff_only = user_passes_test(is_staff_role, login_url="login")

def home(r):
    return render(r,"home.html",{"departments":Department.objects.all()[:8],"doctors":Doctor.objects.select_related("user","department")[:4],
        "reviews":Testimonial.objects.all()[:3],"services":Service.objects.all()[:6]})
def about(r): return render(r,"about.html",{"doctors":Doctor.objects.select_related("user","department")[:8]})
def departments(r): return render(r,"departments.html",{"departments":Department.objects.annotate(n=Count("doctor"))})
def services(r): return render(r,"services.html",{"services":Service.objects.all()})
def doctors(r):
    qs = Doctor.objects.select_related("user","department"); q = r.GET.get("q",""); d = r.GET.get("dept","")
    if q: qs = qs.filter(Q(user__first_name__icontains=q)|Q(user__last_name__icontains=q)|Q(specialization__icontains=q))
    if d: qs = qs.filter(department_id=d)
    return render(r,"doctors.html",{"doctors":qs,"departments":Department.objects.all(),"q":q,"dept":d})
def contact(r):
    f = ContactForm(r.POST or None)
    if r.method=="POST" and f.is_valid():
        f.save(); messages.success(r,"Thank you! Your message has been received."); return redirect("contact")
    return render(r,"contact.html",{"form":f})

def book(r):
    init = {}
    if r.user.is_authenticated and hasattr(r.user,"patient"):
        init = {"name":r.user.get_full_name(),"phone":r.user.patient.phone}
    if r.GET.get("doctor"):
        doc = Doctor.objects.filter(pk=r.GET["doctor"]).first()
        if doc: init.update(doctor=doc, department=doc.department)
    f = AppointmentForm(r.POST or None, initial=init)
    if r.method=="POST" and f.is_valid():
        a = f.save(commit=False)
        if r.user.is_authenticated and hasattr(r.user,"patient"): a.patient = r.user.patient
        a.save(); messages.success(r,"Appointment requested. Status: Pending admin approval.")
        return redirect("portal" if a.patient else "home")
    return render(r,"book.html",{"form":f,"doctor_depts":{d.id:d.department_id for d in Doctor.objects.all()}})

def register(r):
    f = RegisterForm(r.POST or None)
    if r.method=="POST" and f.is_valid():
        login(r, f.save()); messages.success(r,"Welcome to Al-Shifa!"); return redirect("portal")
    return render(r,"register.html",{"form":f})

@login_required
def portal(r):
    p = getattr(r.user,"patient",None)
    ctx = {"patient":p}
    if p: ctx.update(appointments=p.appointment_set.select_related("doctor__user","department"),
        prescriptions=p.prescription_set.select_related("doctor__user"), labs=p.labresult_set.all(), payments=p.payment_set.all())
    return render(r,"portal.html",ctx)

def scoped(u):
    qs = Appointment.objects.select_related("doctor__user","department")
    if not u.is_superuser and hasattr(u,"doctor"): qs = qs.filter(doctor=u.doctor)
    return qs

@staff_only
def dashboard(r):
    qs = scoped(r.user); today = timezone.localdate()
    shown = qs; q = r.GET.get("q",""); s = r.GET.get("status","")
    if q: shown = shown.filter(Q(name__icontains=q)|Q(phone__icontains=q))
    if s: shown = shown.filter(status=s)
    monthly = qs.annotate(m=TruncMonth("date")).values("m").annotate(c=Count("id")).order_by("m")
    growth = Patient.objects.annotate(m=TruncMonth("user__date_joined")).values("m").annotate(c=Count("id")).order_by("m")
    revenue = Payment.objects.filter(paid=True).annotate(m=TruncMonth("date")).values("m").annotate(t=Sum("amount")).order_by("m")
    lab = lambda rows,k: json.dumps([[x["m"].strftime("%b %Y") for x in rows],[float(x[k]) for x in rows]])
    ctx = {"patients":Patient.objects.count(),"doctors":Doctor.objects.count(),"total":qs.count(),
      "today":qs.filter(date=today).count(),"depts":Department.objects.count(),
      "revenue":Payment.objects.filter(paid=True).aggregate(t=Sum("amount"))["t"] or 0,
      "appts":shown[:50],"q":q,"status":s,"monthly":lab(monthly,"c"),"growth":lab(growth,"c"),"rev":lab(revenue,"t"),
      "by_status":json.dumps([[l for _,l in Appointment.STATUS],[qs.filter(status=k).count() for k,_ in Appointment.STATUS]])}
    return render(r,"dashboard.html",ctx)

@staff_only
@require_POST
def set_status(r,pk,status):
    a = get_object_or_404(scoped(r.user),pk=pk)
    if status in dict(Appointment.STATUS): a.status = status; a.save(); messages.success(r,f"Appointment {status}.")
    return redirect("dashboard")

@staff_only
def report(r):
    resp = HttpResponse(content_type="text/csv"); resp["Content-Disposition"] = 'attachment; filename="appointments.csv"'
    w = csv.writer(resp); w.writerow(["Patient","Phone","Department","Doctor","Date","Time","Status"])
    for a in scoped(r.user): w.writerow([a.name,a.phone,a.department,a.doctor,a.date,a.time,a.status])
    return resp

@require_POST
def set_lang(r):
    r.session["lang"] = "so" if r.POST.get("lang") == "so" else "en"
    nxt = r.POST.get("next", "/")
    return redirect(nxt if url_has_allowed_host_and_scheme(nxt, allowed_hosts={r.get_host()}) else "home")
