from django.contrib import admin
from django.utils.html import format_html
from . import models as m

@admin.register(m.Appointment)
class A(admin.ModelAdmin):
    list_display = ("name","phone","doctor","department","date","time","badge")
    list_filter = ("status","department","date"); search_fields = ("name","phone"); date_hierarchy = "date"
    actions = ["approve","reject","complete"]
    @admin.display(description="Status", ordering="status")
    def badge(self, o): return format_html('<span class="badge b-{}">{}</span>', o.status, o.get_status_display())
    @admin.action(description="Approve selected appointments")
    def approve(self, req, qs): qs.update(status="approved")
    @admin.action(description="Reject selected appointments")
    def reject(self, req, qs): qs.update(status="rejected")
    @admin.action(description="Mark selected as completed")
    def complete(self, req, qs): qs.update(status="completed")

@admin.register(m.Doctor)
class D(admin.ModelAdmin):
    list_display = ("pic","__str__","department","specialization","experience"); list_filter = ("department",)
    search_fields = ("user__first_name","user__last_name","specialization")
    @admin.display(description="Photo")
    def pic(self, o): return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover">', o.photo.url) if o.photo else "-"

@admin.register(m.Patient)
class P(admin.ModelAdmin): list_display=("__str__","phone","blood_group"); search_fields=("user__first_name","user__last_name","phone")
@admin.register(m.Payment)
class Pay(admin.ModelAdmin): list_display=("patient","description","amount","paid","date"); list_filter=("paid","date"); list_editable=("paid",)
@admin.register(m.Medicine)
class Med(admin.ModelAdmin): list_display=("name","stock","price"); search_fields=("name",); list_editable=("stock","price")
for mod in (m.Department,m.Service,m.Testimonial,m.Prescription,m.LabResult,m.ContactMessage): admin.site.register(mod)
