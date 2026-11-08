from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
phone_v = RegexValidator(r"^\+?[0-9 \-]{7,20}$", "Enter a valid phone number.")

class Department(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=40, default="bi-heart-pulse", help_text="Bootstrap Icons class")
    def __str__(self): return self.name

class Service(models.Model):
    title = models.CharField(max_length=80); description = models.TextField()
    icon = models.CharField(max_length=40, default="bi-plus-circle")
    def __str__(self): return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=80); text = models.TextField()
    def __str__(self): return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years")
    availability = models.CharField(max_length=100, default="Mon-Fri, 9:00-17:00")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="doctors/", blank=True)
    def __str__(self): return "Dr. " + (self.user.get_full_name() or self.user.username)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, validators=[phone_v])
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=3, blank=True)
    medical_history = models.TextField(blank=True)
    def __str__(self): return self.user.get_full_name() or self.user.username

class Appointment(models.Model):
    STATUS = [("pending","Pending"),("approved","Approved"),("rejected","Rejected"),("completed","Completed")]
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, validators=[phone_v])
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    date = models.DateField(); time = models.TimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-date", "-time"]
    def __str__(self): return f"{self.name} - {self.date}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    medication = models.CharField(max_length=200); instructions = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __str__(self): return f"{self.medication} for {self.patient}"

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.CharField(max_length=120); result = models.TextField()
    date = models.DateField()
    def __str__(self): return f"{self.test} - {self.patient}"

class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    def __str__(self): return f"{self.description} ({self.amount})"

class Medicine(models.Model):
    name = models.CharField(max_length=120); stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self): return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100); email = models.EmailField()
    message = models.TextField(); created = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} - {self.created:%Y-%m-%d}"
