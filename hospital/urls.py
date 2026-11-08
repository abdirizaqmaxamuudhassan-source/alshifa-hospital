from django.urls import path
from django.contrib.auth import views as av
from . import views as v
urlpatterns = [
 path("", v.home, name="home"), path("about/", v.about, name="about"),
 path("departments/", v.departments, name="departments"), path("doctors/", v.doctors, name="doctors"),
 path("services/", v.services, name="services"), path("contact/", v.contact, name="contact"),
 path("appointments/book/", v.book, name="book"),
 path("register/", v.register, name="register"), path("portal/", v.portal, name="portal"),
 path("login/", av.LoginView.as_view(template_name="login.html"), name="login"),
 path("logout/", av.LogoutView.as_view(), name="logout"),
 path("lang/", v.set_lang, name="set_lang"),
 path("dashboard/", v.dashboard, name="dashboard"),
 path("dashboard/appointment/<int:pk>/<str:status>/", v.set_status, name="set_status"),
 path("dashboard/report.csv", v.report, name="report"),
]
