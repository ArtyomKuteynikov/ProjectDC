from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Customer, City, Grade, Spec, HR, Candidates


@admin.register(City)
class CitiesAdmin(admin.ModelAdmin):
    pass


@admin.register(Grade)
class GradesAdmin(admin.ModelAdmin):
    pass


@admin.register(Spec)
class SpecsAdmin(admin.ModelAdmin):
    pass

class SystemUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)


@admin.register(Candidates)
class CandidatesAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'is_active']

    exclude = ['last_login', 'username', 'is_superuser', 'is_staff', 'groups', 'role',
               'user_permissions', 'date_joined', 'uuid', 'show', 'password', 'is_active']

    actions = ['block', 'unblock']

    def block(self, request, queryset):
        for customer in queryset:
            customer.is_active = False
            customer.save()

    block.short_description = 'Заблокировать'

    def unblock(self, request, queryset):
        for customer in queryset:
            customer.is_active = True
            customer.save()

    unblock.short_description = 'Разблокировать'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='candidate')

    def save_model(self, request, obj, form, change):
        obj.role = 'candidate'
        obj.username = obj.email
        super().save_model(request, obj, form, change)


@admin.register(HR)
class HRAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'is_active']

    exclude = ['last_login', 'username', 'is_superuser', 'is_staff', 'groups', 'role',
               'user_permissions', 'date_joined', 'uuid', 'show', 'password', 'is_active']

    actions = ['block', 'unblock']

    def block(self, request, queryset):
        for customer in queryset:
            customer.is_active = False
            customer.save()

    block.short_description = 'Заблокировать'

    def unblock(self, request, queryset):
        for customer in queryset:
            customer.is_active = True
            customer.save()

    unblock.short_description = 'Разблокировать'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='candidate')

    def save_model(self, request, obj, form, change):
        obj.role = 'candidate'
        obj.username = obj.email
        super().save_model(request, obj, form, change)


admin.site.unregister(User)
admin.site.register(User, SystemUserAdmin)
