from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('api/chat/messages', views.get_user_messages),
    path('api/chat/send', views.send_user_message),
    path('admin-panel/', views.support_admin_panel),
    path('api/admin/chats', views.get_all_chats),
    path('api/admin/chat', views.get_chat_by_user),
    path('api/admin/send', views.send_admin_message),


    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('info/', TemplateView.as_view(template_name='info.html'), name='info'),
    path('rules/', TemplateView.as_view(template_name='rules.html'), name='rules'),
    path('support/', TemplateView.as_view(template_name='support.html'), name='support'),
    path('team/', TemplateView.as_view(template_name='team.html'), name='team'),
    path('story/', TemplateView.as_view(template_name='story.html'), name='story'),
         
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
