from django.urls import path
from . import views


urlpatterns = [
    path('convert_matrix', views.MatrixController.as_view(), name='convert_matrix'),


]