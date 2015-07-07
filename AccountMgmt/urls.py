from django.conf.urls import url
from . import views


urlpatterns= [
    
    url(r'^$',views.index, name = 'index'),
    url(r'^(?P<companyID>[0-9]+)/$',views.office_list_view, name = 'office list view'),
    url(r'^(?P<companyID>[0-9]+)/edit/$',views.single_company_view, name = 'single company view'),
    url(r'^(?P<companyID>[0-9]+)/(?P<officeID>[0-9]+)/$', views.account_view, name = 'account view'),
    url(r'^(?P<companyID>[0-9]+)/(?P<officeID>[0-9]+)/edit',views.single_office_view, name = 'single office view'),
    url(r'^(?P<companyID>[0-9]+)/(?P<officeID>[0-9]+)/(?P<accountID>[0-9]+)/$', views.single_account_view, name = 'single account view')
    
]

