from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("add-institution/", views.add_institution, name="add-institution"),
    path("view-institutions/", views.view_institutions, name="view-institutions"),
    path("edit-institution/<str:institution_name>/", views.edit_institution, name="edit-institution"),
    path('delete-institution/<str:institution_name>/', views.delete_institution, name='delete-institution'),
    path("add-instrument/", views.add_instrument, name="add-instrument"),
    path('add-dropdown-option/', views.add_dropdown_option_view, name='add-dropdown-option'),
    path("view-instruments/", views.view_instruments, name="view-instruments"),
    path("edit-instrument/<str:instrument_id>/", views.edit_instrument, name="edit-instrument"),
    path('delete-instrument/<str:instrument_id>/', views.delete_instrument, name='delete-instrument'),
    path("service-order/<int:so_number>/", views.service_order, name="service-order"),
    path("update-instrument-values/<str:instrument_id>/", views.update_instrument_values, name='update-instrument-values'),
    path('delete-instrument-service-order/<int:so_number>/<str:instrument_id>/', views.delete_instrument_service_order, name='delete-instrument-service-order'),
    path("edit-instrument-service-order/<int:so_number>/<str:instrument_id>/", views.edit_instrument_service_order, name="edit-instrument-service-order"),
    path("add-instrument-service-order/<int:so_number>/", views.add_instrument_service_order, name="add-instrument-service-order"),
    path("add-service-order-details/<int:so_number>/", views.add_service_order_details, name="add-service-order-details"),
    path("view-service-orders/", views.view_service_orders, name="view-service-orders"),
    path('download-service-order/<int:so_number>/', views.download_service_order_pdf, name='download-service-order'),
]