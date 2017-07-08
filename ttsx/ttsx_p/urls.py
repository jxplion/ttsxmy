from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^list(\d+)*_*([abc]*)_*(\d*)/$', views.list),
    url(r'^detail(\d*)/$', views.detail),
]