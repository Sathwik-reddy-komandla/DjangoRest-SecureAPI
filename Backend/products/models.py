from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,default=1,null=True)
    title=models.CharField(max_length=255)
    content=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=12,decimal_places=2,default=99.99) 
    
    @property
    def sale_price(self):
        return "%.2f"%(float(self.price)*0.8)
    
    def get_discount(self):
        return 122
    
    def __str__(self) -> str:
        return f'title :{self.title}, content : {self.content}'