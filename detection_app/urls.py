from django.urls import path

from detection_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('sign_up', views.sign_up, name='sign_up'),

    path('admin_home', views.admin_home, name='admin_home'),
    path('state_register', views.state_register, name='state_register'),
    path('state_view', views.state_view, name='state_view'),
    path('state_update/<int:id>/', views.state_update, name='state_update'),
    path('state_delete/<int:id>/', views.state_delete, name='state_delete'),
    path('police_view_admin', views.police_view_admin, name='police_view_admin'),
    path('criminal_records', views.criminal_records, name='criminal_records'),
    path('crimegraph', views.crimegraph, name='crimegraph'),

    path('state', views.state, name='state'),
    path('police_register', views.police_register, name='police_register'),
    path('police_view', views.police_view, name='police_view'),
    path('police_delete/<int:id>/', views.police_delete, name='police_delete'),
    path('criminal_state', views.criminal_state, name='criminal_state'),

    path('police', views.police, name='police'),
    path('profile', views.profile, name='profile'),
    path('profile_edit/<int:id>', views.profile_edit, name='profile_edit'),
    path('criminal_add', views.criminal_add, name='criminal_add'),
    path('criminal', views.criminal, name='criminal'),
    path('criminal_update/<int:id>', views.criminal_update, name='criminal_update'),
    path('criminal_delete/<int:id>', views.criminal_delete, name='criminal_delete'),
    path('missing_add', views.missing_add, name='missing_add'),
    path('missing', views.missing, name='missing'),
    path('missing_update/<int:id>/', views.missing_update, name='missing_update'),
    path('missing_delete/<int:id>/', views.missing_delete, name='missing_delete'),

    path('user_home', views.user_home, name='user_home'),
    path('detection_panel', views.detection_panel, name='detection_panel'),
]
