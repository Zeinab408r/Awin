from django.urls import path
from .views import (ProductList,ProductDetail,CreatCategory,CreatMerchant)

# URLConf
urlpatterns = [
    path('',  ProductList.as_view(), name="ProductList"),
    path("<int:pk>/", ProductDetail.as_view(), name="ProductDetail"),
    path("category/<int:pk>/", CreatCategory.as_view(), name="CreatCategory"),
    path("merchant/<int:pk>/", CreatMerchant.as_view(), name="CreatMerchant"),
]
