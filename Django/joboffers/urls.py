from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('job-list',views.joblist, name='joblist'),
    path('job/<int:offer_id>',views.detail,name="detail")
]