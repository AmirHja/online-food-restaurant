from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import User, Address



class AddressInLineAdmin(admin.StackedInline):
    model = Address
    fields = ['province', 'city', 'address']
    extra = 1


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('personal info'), {'fields': ('first_name', 'last_name', 'gender', 'phone_number' ,'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'fields': ('username', 'phone_number', 'email', '<PASSWORD>', '<PASSWORD>')
            'fields': ('username', 'password1', 'password2', 'phone_number')
        }),
    )
    list_display = ('username', 'phone_number', 'email', 'is_staff')
    search_fields = ('username__exact',)
    ordering = ('-id',)
    inlines = [AddressInLineAdmin]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(phone_number=search_term_as_int)
        return queryset, may_have_duplicates

admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Site)
