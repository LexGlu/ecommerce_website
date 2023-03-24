from django.contrib import admin
from django.utils.html import format_html

from .models import *
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse


@admin.display(description='email')
def email(obj):
    return obj.user.email


@admin.display(description='full name')
def full_name(obj):
    return f'{obj.user.first_name} {obj.user.last_name}'


@admin.display(description='total value')
def total_value(obj):
    return obj.total_value


class AdminCustomer(admin.ModelAdmin):

    class OrderInline(admin.TabularInline):
        model = Order
        extra = 0
        readonly_fields = ['formatted_total_value', 'order_link']
        fields = ['status', 'transaction_id', 'formatted_total_value', 'order_link']

        def order_link(self, obj):
            return format_html('<a href="{}">View Order</a>', reverse('admin:store_order_change', args=[obj.id]))

        def formatted_total_value(self, obj):
            return f'{obj.total_value:,.2f} UAH'

        formatted_total_value.short_description = 'Total value'
        order_link.short_description = 'Order'

    list_display = [full_name, email, 'phone', 'city', 'np_office']
    fields = ['user', 'phone', 'city', 'np_office']
    inlines = [OrderInline]
    search_fields = ('phone', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ['city']


class MyUserAdmin(admin.ModelAdmin):

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


class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        exclude = ['customer']


class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['date_ordered', 'total_value']


class AdminOrder(admin.ModelAdmin):

    class OrderItemInline(admin.TabularInline):
        model = OrderItem
        extra = 0

    class ShippingInfoInline(admin.StackedInline):
        model = ShippingInfo
        form = ShippingInfoForm
        extra = 0

    readonly_fields = ['date_ordered', 'formatted_total_value']
    form = AdminOrderForm
    list_display = ['id', 'customer', 'status', 'formatted_total_value', 'transaction_id', 'date_ordered']
    list_filter = ['status']
    search_fields = ['customer__user__email', 'id', 'transaction_id']
    inlines = [OrderItemInline, ShippingInfoInline]

    def formatted_total_value(self, obj):
        return f'{obj.total_value:,.2f} UAH'

    formatted_total_value.short_description = 'Total value'


class AdminProduct(admin.ModelAdmin):

    list_display = ['name', 'category', 'price', 'digital']
    list_filter = ['category']
    search_fields = ['name', 'description']


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(Customer, AdminCustomer)
admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Order, AdminOrder)
admin.site.register(ShippingInfo)
