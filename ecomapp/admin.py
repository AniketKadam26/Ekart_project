from django.contrib import admin # type: ignore
from .models import Product
# Register your models here.
#need to register Product model
class ProductAdmin(admin.ModelAdmin):
    list_display=["id","name","price","category","pdetails","is_active","pimage"]
    list_filter=["category","is_active"]

admin.site.register(Product,ProductAdmin)
