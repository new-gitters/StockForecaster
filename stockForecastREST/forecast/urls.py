
from django.conf.urls import url, include
from forecast import views

urlpatterns =[
    url(r'^api/forecast/historical/(?P<symbol>[\w-]+)/(?P<choice>[\w-]+)/$',views.historical),
    url(r'^api/forecast/realtime/(?P<symbol>[\w-]+)/(?P<choice>[\w-]+)/$',views.realtime),
]

