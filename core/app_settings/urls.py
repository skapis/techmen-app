from django.urls import path
from . import views

urlpatterns = [
    path('', views.app_settings, name='settings'),
    path('work-list/add', views.add_work_list_item, name='work_list_add'),
    path('work-item-desc/add', views.add_work_item_desc, name='work_item_desc_add'),
    path('work-list-item/edit/<str:item_id>', views.edit_work_list_item, name='worklist_edit'),
    path('work-item-desc/edit/<str:item_id>', views.edit_work_item_desc, name='itemdesc_edit'),
    path('change/work-list-item/<str:item_id>', views.change_validity_work_list_item, name='worklist_change'),
    path('change/work-item-desc/<str:item_desc_id>', views.change_validity_work_item_desc, name='itemdesc_change'),
    path('create/enumerations', views.create_enums, name='enums_create')
]
