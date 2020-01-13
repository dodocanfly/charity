from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    min_admin_objects = 1
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Uprawnienia'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Dodatkowe'), {'fields': ('first_name', 'last_name', 'city')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def has_delete_permission(self, request, obj=None):
        queryset = self.model.objects.filter(is_superuser=True)
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
        if selected:
            queryset = queryset.exclude(pk__in=selected)
        if queryset.count() < self.min_admin_objects:
            message = 'There should be at least {} object(s) left.'
            self.message_user(request, message.format(self.min_admin_objects))
            return False
        return super().has_delete_permission(request, obj)

# admin.site.register(CustomUser, CustomUserAdmin)
