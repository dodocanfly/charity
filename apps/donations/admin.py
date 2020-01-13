from django.contrib import admin

from .models import Category, Institution, Donation


class InstitutionAdmin(admin.ModelAdmin):
    model = Institution
    list_display = ('name', 'type', 'description',)
    search_fields = ('name', 'description',)
    ordering = ('name',)


admin.site.register(Category)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Donation)
