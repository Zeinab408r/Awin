from django.db import models
from FirstApi.models import BaseModel
from networks_app.models import AwinProductLink


class ProductMerchant(BaseModel):
    def __init__(self, awin_merchant_id, loader_link, name):
        self.awin_merchant_id= awin_merchant_id
        self.loader_link = loader_link
        self.name= name

    name = models.CharField(max_length=255)
    loader_link = models.ForeignKey(
        AwinProductLink, blank=True, null=True, on_delete=models.PROTECT
    )
    awin_merchant_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'PMerchant|ID:{self.id}|Name:{self.name}'


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    icon_url = models.CharField(max_length=1000, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'PCategory|ID:{self.id}|Slug:{self.slug}'



class Product(BaseModel):
    def __init__(self,
        awin_product_id,
        name,
        description,
        price,
        image_url,
        is_active,
        awin_deep_link,
        merchant_id,
        loader_link,
        category="default", ):
        self.awin_product_id= awin_product_id
        self.name= name
        self.description= description
        self.price= price
        self.image_url= image_url
        self.is_active = is_active
        self.awin_deep_link= awin_deep_link
        self.merchant_id= merchant_id
        self.loader_link = loader_link
        # self.category= category



    name = models.CharField(max_length=1000)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name='products'
    )
    merchant = models.ForeignKey(
        ProductMerchant, on_delete=models.PROTECT, related_name='products'
    )
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    best_deal = models.BooleanField(default=False)
    loader_link = models.ForeignKey(
        AwinProductLink, blank=True, null=True, on_delete=models.PROTECT
    )
    awin_deep_link = models.CharField(max_length=1000, null=True, blank=True)
    awin_product_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Product|ID:{self.id}|Name:{self.name}'
