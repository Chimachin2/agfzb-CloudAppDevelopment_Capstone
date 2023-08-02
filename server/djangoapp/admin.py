from django.contrib import admin
from .models import CarMake,CarModel


# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_id', 'make', 'Name', "Dealerid", "Type", "Year", )

class CarMakeAdmin(admin.ModelAdmin):
    inlines=[CarModelInline]
    list_display=("Name", "Description")

# Register models here
admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake,CarMakeAdmin)



