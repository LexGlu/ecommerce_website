from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


@admin.display(description='email')
def email(obj):
    return obj.user.email


@admin.display(description='full name')
def full_name(obj):
    return f'{obj.user.first_name} {obj.user.last_name}'


class AdminCustomer(admin.ModelAdmin):
    """
    - The @admin.display decorator is used to create custom fields to display in the Django admin panel.
    - The email and full_name functions are used to display the customer's email and full name respectively in the
    AdminCustomer class.
    """
    list_display = [full_name, email, 'phone', 'city']


class MyUserAdmin(admin.ModelAdmin):
    """
    - The MyUserAdmin class is used to customize the user model in the Django admin panel.
    - The list_display attribute is used to display the desired fields of the user model in the admin panel.
    - The search_fields attribute is used to allow searching for users by email, first name, and last name.
    - The get_search_results method is overridden to also allow searching for users by ID.
    """
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff',
                    'is_superuser', 'date_joined', ]

    search_fields = ('email', 'first_name', 'last_name')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(id=search_term_as_int)
        except ValueError:
            pass
        return queryset, use_distinct


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(Customer, AdminCustomer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
