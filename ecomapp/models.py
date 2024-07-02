from django.db import models # type: ignore
 

# Create your models here.
class Product(models.Model):
    CAT=((1,"shoes"),(2,"mobile"),(3,"cloths"))
    name=models.CharField(max_length=30,verbose_name="Product Name")
    price=models.IntegerField()
    category=models.IntegerField(choices=CAT,verbose_name="Category")
    pdetails=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True, verbose_name="Is_Active")
    pimage=models.ImageField(upload_to='zimage')
    def __str__(self):
        return self.name
    
class Cart(models.Model):
        
        userid=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="userid")
        pid=models.ForeignKey("Product",on_delete=models.CASCADE,db_column="pid")
        qty=models.IntegerField(default=1)

class Order(models.Model):
     order_id=models.CharField(max_length=50)
     user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="user_id")
     p_id=models.ForeignKey("Product",on_delete=models.CASCADE,db_column="p_id")
     qty=models.IntegerField(default=1)
     amt=models.IntegerField()