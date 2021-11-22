
from django.contrib import admin
from django.urls import path
from driver_state import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('changestate',views.setState,name='setState'),
    path('getdriverlist',views.getDriverList,name='getDriverList')

]
