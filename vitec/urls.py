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
    path("add-service-order/<int:so_number>/", views.add_service_order, name="add-service-order"),
    path("update-instrument-values/<str:instrument_id>/", views.update_instrument_values, name='update-instrument-values'),
    # path("view-service-orders/", views.view_service_orders, name="view-institutions"),
    # path("edit-service-order/<int:so_number>/", views.edit_service_order, name="edit-institution"),
    # path('delete-service-order/<int:so_number>/', views.delete_service_order, name='delete-institution'),
]