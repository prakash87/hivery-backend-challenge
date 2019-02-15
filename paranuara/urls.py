from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name='companies_list'),
    path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='company_detail'),

    path('people/', views.PersonList.as_view(), name='people_list'),
    path('people/<int:pk>/', views.PersonDetail.as_view(), name='person_detail'),

    re_path(r'^people/(?P<comma_separated_ids>[0-9]+(,[0-9]+)+)/$', views.PersonCompare.as_view(),
            name='people_compare'),
]
