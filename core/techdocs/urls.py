from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('record/add', views.add_record, name='add_record'),
    path('record/<str:record_id>/delete', views.delete_record, name='delete_record'),
    path('record/<str:record_id>/edit', views.edit_record, name='edit_record'),
    path('record/<str:record_id>', views.record_detail, name='record'),
    path('record/<str:record_id>/confirm', views.confirm_record, name='confirm_record'),
    path('record/<str:record_id>/export', views.export_record, name='export_record'),
    path('lines', views.production_lines, name='lines'),
    path('line/<str:line_id>/edit', views.edit_line, name='edit_line'),
    path('line/<str:line_id>/change', views.change_line, name='change_line'),
    path('lines/check', views.check_line_name, name='line_duplicate_check'),
    path('line/<str:line_id>', views.line_detail, name='line'),
]