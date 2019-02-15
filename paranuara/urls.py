from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view()),
    path('companies/<int:pk>/', views.CompanyDetail.as_view()),

    path('people/', views.PersonList.as_view()),
    path('people/<int:pk>/', views.PersonDetail.as_view()),

    re_path(r'^people/(?P<comma_separated_ids>[0-9]+(,[0-9]+)+)/$', views.PersonCompare.as_view()),
]