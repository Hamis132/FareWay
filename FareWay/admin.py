from django.contrib import admin
from .models import Attraction, Category,Route
from django.conf import settings


class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'latitude', 'longitude',)
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'category', 'latitude', 'longitude', 'time', 'description','image' )
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )


admin.site.register(Attraction, AttractionAdmin)
admin.site.register(Category)
admin.site.register(Route)
