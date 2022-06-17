from django.contrib import admin
from .models import (
    Research,
    PHenology,
    Production,
    Plants,
    Photo,
    ProductTypes,
    Protect,
    AllData,
    Experiment,
    Note,
    ProductionMany,
    Countries,
    Months,
    
 
)
# Register your models here.
admin.site.register(Countries)
admin.site.register(Months)
admin.site.register(Research)
admin.site.register(PHenology)
admin.site.register(Production)
admin.site.register(Plants)

admin.site.register(Photo)
admin.site.register(ProductTypes)
admin.site.register(Protect)
admin.site.register(AllData)
admin.site.register(Experiment)
admin.site.register(Note)
admin.site.register(ProductionMany)


