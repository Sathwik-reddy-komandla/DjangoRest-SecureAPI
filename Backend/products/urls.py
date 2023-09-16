from django.urls import path
from . import views

urlpatterns=[
    path('',views.ProductViewSet.as_view({'get':'list','post':'create'})),
    path('<int:pk>/',views.ProductViewSet.as_view({'get':'retrieve'}),name="product-detail"),
    path('edit/<int:pk>/',views.ProductViewSet.as_view({'get':'retrieve','put':'update'}),name="product-edit"),
]