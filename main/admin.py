from django.contrib import admin
from main.models import Report


# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = ('createdDay', 'beginDay', 'beginHour', 'endDay', 'endHour')

    filter_horizontal = ()
    list_filter = ()
    ordering = ('createdDay',)  # Contain only fields in your `custom-user-model` intended to ordering
    fieldsets = ()


admin.site.register(Report, ReportAdmin)
