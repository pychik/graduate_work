from apps.offer.models import Subscription
from django.contrib import admin


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'currency', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_editable = ('type', 'price', 'currency')
    list_filter = ('type', 'currency',)
    search_fields = ('name',)
