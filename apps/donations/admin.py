from django.contrib import admin

from .models import Category, InstitutionType, Institution, Donation


class InstitutionAdmin(admin.ModelAdmin):
    model = Institution
    list_display = ('name', 'type', 'description',)
    search_fields = ('name', 'description',)
    ordering = ('name',)


admin.site.register(Category)
admin.site.register(InstitutionType)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Donation)
