import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.db.models import Q

from account.models import UserProfile
from post.models import Post
from project.models import PostProject, ProjectMembers
from notification.models import Notifications

@login_required
@ensure_csrf_cookie
def send_application(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        post_id = data.get('post_id')
        author_id = data.get('recipient_id')
        sender_id = request.user.id  # 요청을 보낸 사용자의 ID

        try:
            post = Post.objects.get(pk=post_id)
            recipient = UserProfile.objects.get(pk=author_id)
            sender = UserProfile.objects.get(pk=sender_id)

            # 중복 레코드 방지를 위해 먼저 확인
            if not Notifications.objects.filter(user=recipient, sender=sender, post=post).exists():
                # 중복 레코드가 없을 때만 알림 메시지 생성
                notification = Notifications(user=recipient, sender=sender, post=post, accept_or_not=None)
                notification.save()
                success = True
            else:
                success = False  # 이미 존재하는 레코드라면 중복 처리
        except (Post.DoesNotExist, UserProfile.DoesNotExist) as e:
            # 필요한 객체를 찾을 수 없는 경우
            success = False
    else:
        success = False

    return JsonResponse({'success': success})

def mark_notifications_as_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_ids = data.get('notificationIds', [])
            print(notification_ids)

            for notification_id in notification_ids:
                try:
                    notification = Notifications.objects.get(id=notification_id)

                    # 현재 사용자가 해당 알림을 소유하고 있는지 확인
                    if request.user == notification.sender:
                        notification.read_or_not = True  # 알림을 '읽음'으로 표시
                        notification.save()  # 데이터베이스에 변경사항 저장
                    else:
                        return JsonResponse({'success': False, 'error': '권한이 없습니다.'})
                except Notifications.DoesNotExist:
                    return JsonResponse({'success': False, 'error': f'알림을 찾을 수 없습니다: {notification_id}'})
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': '잘못된 JSON 데이터입니다.'})
    else:
        return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(Q(user=request.user) | Q(sender=request.user)).order_by('-created_at')

        notifications_list = []
        for notification in notifications:
            postinfo = Post.objects.get(id=notification.post.id)
            projectinfo = PostProject.objects.get(post_id=postinfo.id)
            senderinfo = UserProfile.objects.get(id=notification.sender.id)
            created_at_formatted = notification.created_at.strftime('%Y-%m-%d %H:%M')
            notifications_list.append({
                'id': notification.id,
                'user': notification.user.username,
                'title': postinfo.title,
                'sender': senderinfo.username,
                'created_at': created_at_formatted,
                'accept_or_not': notification.accept_or_not,
                'read_or_not': notification.read_or_not,
                'titlelink': f'/project/{projectinfo.id}',
                'senderlink': f'/myinfo/{senderinfo.id}',
            })

        context = {'notifications_list': notifications_list}
        return JsonResponse({'notifications': context})
    else:
        return JsonResponse({'notifications': []})

def accept_reject_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_id = data.get('notificationId')
            result = data.get('result')
            
            if notification_id is not None and result is not None:
                try:
                    notification = Notifications.objects.get(id=notification_id)

                    if result == '수락':
                        notification.accept_or_not = True
                        notification.save()
                        
                        # 추가적인 작업을 수행 (예: ProjectMembers에 멤버 추가)
                        sender = notification.sender.id
                        projectinfo = PostProject.objects.get(post_id=notification.post.id)
                        projectid = projectinfo.id
                        ProjectMembers.objects.create(members_id=sender, project_id=projectid)
                        members = ProjectMembers.objects.filter(project_id=projectid).count()
                        if members >= projectinfo.target_members:
                            projectinfo.status = 2
                            projectinfo.save()

                    elif result == '거절':
                        notification.accept_or_not = False
                        notification.save()

                    response_data = {'success': True}
                    return JsonResponse(response_data)

                except Notifications.DoesNotExist:
                    response_data = {'success': False, 'error': '알림을 찾을 수 없습니다.'}
                    return JsonResponse(response_data)

            else:
                response_data = {'success': False, 'error': '잘못된 데이터 요청입니다.'}
                return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data)

    else:
        response_data = {'success': False, 'error': 'POST 요청이 필요합니다.'}
        return JsonResponse(response_data)
