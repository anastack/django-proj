from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SupportMessage
from .serializers import SupportMessageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.contrib.admin.views.decorators import staff_member_required


@api_view(['GET'])
def get_user_messages(request):
    if not request.session.session_key:
        request.session.create() 
    user_id = request.session.session_key
    messages = SupportMessage.objects.filter(user_id=user_id).order_by('timestamp')
    serializer = SupportMessageSerializer(messages, many=True, context={'request': request})
    return Response({'success': True, 'messages': serializer.data})


@api_view(['POST'])
def send_user_message(request):
    if not request.session.session_key:
        request.session.create()

    user_id = request.session.session_key
    message = request.data.get('message', '').strip()
    image = request.FILES.get('image') 

    if not message:
        return Response({'success': False, 'error': 'Сообщение не может быть пустым'}, status=400)

    msg = SupportMessage.objects.create(user_id=user_id, sender='user', message=message, image=image)
    return Response({'success': True, 'message': 'Отправлено'})



@staff_member_required
def support_admin_panel(request):
    return render(request, 'admin.html')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_chats(request):
    user_ids = SupportMessage.objects.values_list('user_id', flat=True).distinct()
    data = []

    for uid in user_ids:
        last_msg = SupportMessage.objects.filter(user_id=uid).order_by('-timestamp').first()
        count = SupportMessage.objects.filter(user_id=uid).count()
        last_user_msg = SupportMessage.objects.filter(user_id=uid, sender='user').order_by('-timestamp').first()
        last_admin_msg = SupportMessage.objects.filter(user_id=uid, sender='admin').order_by('-timestamp').first()

        has_unread = False
        if last_user_msg and (
            not last_admin_msg or last_user_msg.timestamp > last_admin_msg.timestamp
        ):
            has_unread = True


        data.append({
            'userId': uid,
            'lastMessage': {
                'message': last_msg.message if last_msg else '',
                'timestamp': last_msg.timestamp.isoformat() if last_msg else ''
            },
            'messageCount': count,
            'hasUnreadFromUser': has_unread
        })

    return Response({'success': True, 'chats': data})





@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_chat_by_user(request):
    uid = request.GET.get('user_id')
    if not uid:
        return Response({'success': False, 'error': 'user_id обязателен'}, status=400)

    messages = SupportMessage.objects.filter(user_id=uid).order_by('timestamp')
    serializer = SupportMessageSerializer(messages, many=True,  context={'request': request})
    return Response({'success': True, 'messages': serializer.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def send_admin_message(request):
    uid = request.data.get('user_id')
    message = request.data.get('message', '').strip()
    if not uid or not message:
        return Response({'success': False, 'error': 'user_id и message обязательны'}, status=400)

    SupportMessage.objects.create(user_id=uid, sender='admin', message=message)
    return Response({'success': True})