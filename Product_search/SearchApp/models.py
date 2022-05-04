from django.db import models
from datetime import datetime
# Create your models here.

class installer(models.Model):  # installer table #
    hmac = models.CharField(max_length=2000)
    shop = models.CharField(max_length=2000)
    code = models.CharField(max_length=2000)
    access_token = models.CharField(max_length=2000)
    install_date = models.DateTimeField(default=datetime.now())

class product_detailmst(models.Model):
    shop = models.CharField(max_length=200)
    product_id = models.CharField(max_length=50)
    variant_id = models.CharField(max_length=60)
    product_title = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='')
    product_img = models.ImageField(upload_to='',default='')
    