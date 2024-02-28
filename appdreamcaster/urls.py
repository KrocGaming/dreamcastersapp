from django.urls import path
from . import views
from .views import *
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"), name="redirect-admin"),

    #login
    path('', views.loginpage, name="loginpage"),
    path('logout', views.logoutuser, name="logout"),

    #dashboard
    path('dashboard', views.dashboardpage, name="dashboardpage"),

    #all List
    path('all-list', views.alllist, name="alllist"),
    path('create_customerenq/', CustomerEnqCreate.as_view(), name='create_customerenq'),
    path('update_customerenq/<int:pk>/', CustomerEnqUpdate.as_view(), name='update_customerenq'),
    path('view_customerenq/<int:pk>/', views.CustomerEnqView, name='view_customerenq'),
    path('changeprocessing_customerenq/<int:pk>/', views.CustomerEnqStatPro, name='changeprocessing_customerenq'),

    #processing list
    path('processing-list', views.processinglist, name="processing-list"),
    path('view_customerenqprocess/<int:pk>/', views.view_customerenqprocess, name='view_customerenqprocess'),
    path('changefollowup_customerenq/<int:pk>/', views.changefollowup_customerenq, name='changefollowup_customerenq'),


    #follow-up list
    path('followup-list', views.followuplist, name="followup-list"),
    path('view_customerenqfollow/<int:pk>/', views.view_customerenqfollow, name='view_customerenqfollow'),
    path('changeconfirmed_customerenq/<int:pk>/', views.changeconfirmed_customerenq, name='changeconfirmed_customerenq'),
    path('changerejected_customerenq/<int:pk>/', views.changerejected_customerenq, name='changerejected_customerenq'),

    #confirmed list
    path('confirmed-list', views.confirmedlist, name="confirmed-list"),
    path('view_customerenqconfirm/<int:pk>/', views.view_customerenqconfirm, name='view_customerenqconfirm'),
    path('changetravelled_customerenq/<int:pk>/', views.changetravelled_customerenq, name='changetravelled_customerenq'),

    #rejected list
    path('rejected-list', views.rejectedlist, name="rejected-list"),
    
    #traveled list
    path('traveled-list', views.traveledlist, name="traveled-list"),
    
    #customerdetails list
    path('customerdetails-list', views.customerdetailslist, name="customerdetails-list"),
    path('adddirect/<int:pk>/', ProductCreate.as_view(), name='adddirect'),
    path('update/<int:pk>/', ProductUpdate.as_view(), name='update_product'),
    path('delete-image/<int:pk>/', views.delete_image, name='delete_image'),
    path('delete-variant/<int:pk>/', views.delete_variant, name='delete_variant'),
    path('deleteproduct/<int:id>/', views.deleteproduct, name='delete_product'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
