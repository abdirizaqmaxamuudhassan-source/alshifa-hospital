from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .models import *

class Styled:
    def style(self):
        for f in self.fields.values(): f.widget.attrs["class"] = "form-control"

class AppointmentForm(forms.ModelForm, Styled):
    class Meta:
        model = Appointment; fields = ["name","phone","department","doctor","date","time","reason"]
        widgets = {"date":forms.DateInput(attrs={"type":"date"}),"time":forms.TimeInput(attrs={"type":"time"}),
                   "reason":forms.Textarea(attrs={"rows":2})}
    def __init__(self,*a,**k): super().__init__(*a,**k); self.style()
    def clean(self):
        d = super().clean(); dt, doc, dep, t = d.get("date"), d.get("doctor"), d.get("department"), d.get("time")
        if dt and dt < timezone.localdate(): self.add_error("date","Date cannot be in the past.")
        if doc and dep and doc.department_id != dep.id: self.add_error("doctor","Doctor is not in that department.")
        if doc and dt and t and Appointment.objects.filter(doctor=doc,date=dt,time=t).exclude(status="rejected").exists():
            self.add_error("time","That slot is already booked.")
        return d

class ContactForm(forms.ModelForm, Styled):
    class Meta: model = ContactMessage; fields = ["name","email","message"]
    def __init__(self,*a,**k): super().__init__(*a,**k); self.style()

class RegisterForm(UserCreationForm, Styled):
    phone = forms.CharField(max_length=20, validators=[phone_v])
    class Meta(UserCreationForm.Meta):
        model = User; fields = ["username","first_name","last_name","email"]
    def __init__(self,*a,**k): super().__init__(*a,**k); self.style()
    def save(self, commit=True):
        u = super().save(commit=True)
        Patient.objects.create(user=u, phone=self.cleaned_data["phone"])
        u.groups.add(Group.objects.get_or_create(name="Patient")[0]); return u
