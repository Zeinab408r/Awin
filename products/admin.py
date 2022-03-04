from django.contrib import admin
import json
from products.models import (Product,
                             ProductCategory,
                             ProductMerchant)


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductMerchant)