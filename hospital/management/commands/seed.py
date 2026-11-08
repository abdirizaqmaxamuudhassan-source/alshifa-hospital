from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from hospital.models import *
DEPTS = [("Cardiology","Heart and vascular care.","bi-heart-pulse"),("Pediatrics","Care for infants and children.","bi-emoji-smile"),
 ("Neurology","Brain, spine and nerve care.","bi-activity"),("Dentistry","Oral and dental health.","bi-emoji-grin"),
 ("Gynecology","Women's health and maternity.","bi-gender-female"),("Orthopedics","Bones, joints and sports injuries.","bi-bandaid"),
 ("Emergency Department","24/7 emergency and trauma care.","bi-truck-front"),("General Medicine","Primary and family care.","bi-clipboard2-pulse")]
SERVICES = [("Emergency Care","24/7 trauma and emergency response.","bi-lightning-charge"),("Laboratory","Accurate diagnostic testing.","bi-eyedropper"),
 ("Pharmacy","In-house pharmacy open daily.","bi-capsule"),("Surgery","Modern operating theatres.","bi-scissors"),
 ("Medical Checkups","Preventive health packages.","bi-clipboard-check"),("Ambulance Services","Fully equipped ambulances.","bi-truck")]
class Command(BaseCommand):
    help = "Create starter departments, services and roles. Doctors/testimonials: add via /admin/."
    def handle(self, *a, **k):
        for n,d,i in DEPTS: Department.objects.get_or_create(name=n, defaults={"description":d,"icon":i})
        for t,d,i in SERVICES: Service.objects.get_or_create(title=t, defaults={"description":d,"icon":i})
        for g in ("Doctor","Receptionist","Patient"): Group.objects.get_or_create(name=g)
        self.stdout.write(self.style.SUCCESS("Seeded. Now create a superuser and add doctors in /admin/."))
