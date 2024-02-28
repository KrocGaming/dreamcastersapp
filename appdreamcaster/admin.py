from django.contrib import admin
from django.apps import apps
from .models import *


app_name = 'appdreamcaster' 


app_models = apps.get_app_config(app_name).get_models()

class DynamicListDisplayAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
    
        model_fields = [field.name for field in self.model._meta.fields]
        return model_fields

for model in app_models:
    try:
        admin.site.register(model, DynamicListDisplayAdmin)
    except admin.sites.AlreadyRegistered:
        pass

