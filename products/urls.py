from django.urls import path
from products.views import *

urlpatterns = [
    path('', dash_board, name='dash_board'),
    
    #---Authentication
    path('register/', register_view, name='register'),
    path('log-in/', login_view, name='log_in'),
    path('log-out/', logout_view, name='log_out'),
    
    #---CRUD
    path('read/', read_view, name='read_view'),
    path('create/', create_view, name='create_view'),
    path('update/<str:tiger>', update_view, name='update_view'),
    path('delete/<str:tiger>', delete_view, name='delete_view'),
]
