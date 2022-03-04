from django.urls import path
from .views import (ProductList,ProductDetail,CreatCategory,CreatMerchant)

# URLConf
urlpatterns = [
    path('products/',  ProductList.as_view(), name="ProductList"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="ProductDetail"),
    path("newcategory/<int:pk>/", CreatCategory.as_view(), name="CreatCategory"),
    path("newmerchant/<int:pk>/", CreatMerchant.as_view(), name="CreatMerchant"),
]
