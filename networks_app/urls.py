from django.urls import path
from .views import (UpdateProduct)

# URLConf
urlpatterns = [
    path('update/',UpdateProduct , name="update"),
    
]
