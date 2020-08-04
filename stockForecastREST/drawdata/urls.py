from django.conf.urls import url, include
from drawdata import views

urlpatterns =[
    url(r'^api/drawdata/historical/(?P<symbol>[\w-]+)/(?P<start>[\w-]+)/$',views.historical),
    url(r'^api/drawdata/realtime/(?P<symbol>[\w-]+)/$',views.realtime),
]

