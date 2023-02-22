from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^login/$', 'Ecom.my_store.views.user_login', name='user_login'),
    url(r'^logout/$', 'Ecom.my_store.views.user_logout', name='user_logout'),
    
    url(r'^$', 'Ecom.my_store.views.store', name='store'),
    url(r'^create_user/$', 'Ecom.my_store.views.create_user', name='create_user'),
    
    url(r'^cart/', 'Ecom.my_store.views.cart', name='cart'),
    url(r'checkout/', 'Ecom.my_store.views.checkout', name='checkout'),
    url(r'^update_item/', 'Ecom.my_store.views.updateItem', name='update_item'),
    
    url(r'^process_order/', 'Ecom.my_store.views.processOrder', name='process_order'),
    url(r'^current_orders/', 'Ecom.my_store.views.current_orders', name='current_orders'),
    url(r'^order/(?P<transaction_id>[0-9].+\.[0-9]{1,2})/$', 'Ecom.my_store.views.ship_detail', name='ship_detail'),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
    
)