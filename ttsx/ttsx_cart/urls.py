from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.cart),
    url(r'^addcart/$', views.addcart),
    url(r'^count/$', views.countt),
    url(r'^reorder/$', views.reorder),
    url(r'^dorder/$', views.dorder),
    url(r'^del/$', views.del1),
]