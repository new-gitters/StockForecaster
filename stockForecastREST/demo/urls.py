"""
These are our routes:

/api/demo/historicaldata: GET, POST, DELETE
/api/demo/realtimedata: GET, PUT, DELETE

"""
from django.conf.urls import url 
from demo import views 
 
urlpatterns = [ 
    url(r'^api/demo/historicaldata$', views.historicaldata_list),
    url(r'^api/demo/realtimedata$', views.realtimedata_list)
]