from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

from post.forms import PostForm
from project.forms import ProjectForm
from account.models import UserProfile
from post.models import Post
from project.models import Project, ProjectMembers

def list(request, page_num=1):
    items_per_page = 9

    project = Project.objects.order_by('-id')
    project_list = []

    query = request.GET.get('search')
    search_type = request.GET.get('search-type')

    filtered_projects = project
    if query:
        if search_type == 'title-content':
            filtered_projects = project.filter(
                Q(post__title__icontains=query) | Q(post__content__icontains=query)
            )
        elif search_type == 'writer':
            filtered_projects = project.filter(
                Q(post__author__username__icontains=query)
            )
    else:
        query = ''
        search_type = ''

    filter_option = request.GET.get('filter-option')
    if filter_option == 'recruiting':
        filtered_projects = filtered_projects.filter(status=1)
    
    page = request.GET.get('page', page_num)
    paginator = Paginator(filtered_projects, items_per_page)
    page_obj = paginator.get_page(page)

    for project in page_obj:
        post = Post.objects.get(id=project.post_id)
        author = UserProfile.objects.get(id=post.author_id)
        status = project.status

        project_list.append({
                    'project_id': project.id,
                    'title': post.title,
                    'author': author.username,
                    'created_at': post.created_at,
                    'tech_stack': project.tech_stack.split()[0],
                    'status': status,
                })

    context = {
        'post_list': project_list,
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
    }

    return render(request, 'project/list.html', context)

def read(request, project_id=None):
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        post = get_object_or_404(Post, id=project.post_id)
        author = get_object_or_404(UserProfile, id=post.author_id)
        members = ProjectMembers.objects.filter(project=project_id).count()
        context = {
            'project_id' : project_id,
            'title': post.title,
            'author': author.username,
            'created_at': post.created_at,
            'start_date': project.start_date,
            'end_date': project.end_date,
            'members': members,
            'target_members': project.target_members,
            'tech_stack': project.tech_stack.split(),
            'ext_link': project.ext_link,
            'content': post.content,
            'status': project.status,
            'post_id': post.id,
            'author_id': author.id,
        }
        return render(request, 'project/read.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('/project')

@login_required(login_url='login')
def write(request, project_id=None):
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        post = get_object_or_404(Post, id=project.post_id)
    else:
        project = Project()
        post = Post()
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('/project')
        
        post_form = PostForm(request.POST, request.FILES, instance=post)
        project_form = ProjectForm(request.POST, request.FILES, instance=project)

        if post_form.is_valid() and project_form.is_valid():
            post = post_form.save(commit=False)
            project = project_form.save(commit=False)
            if not project_id:
                post.author_id = request.user.id
                post.save()
                project.post_id = post.id
                project.save()
                project_id = project.id
                user = get_object_or_404(UserProfile, id=request.user.id)
                project = get_object_or_404(Project, id=project_id)
                ProjectMembers.objects.create(project=project, members=user)
            else:
                post.save()
                project.save()

            return redirect('/project/'+project_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'target_members': request.POST.get('members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'project/write.html', context)
    else:
        if project_id:
            if request.user.id == post.author_id:
                start_date = str(project.start_date).replace('년 ','-').replace('월 ','-').replace('일','')
                end_date = str(project.end_date).replace('년 ','-').replace('월 ','-').replace('일','')
                context = {
                    'project_id': project_id,
                    'title': post.title,
                    'start_date': start_date,
                    'end_date': end_date,
                    'target_members': project.target_members,
                    'tech_stack': project.tech_stack,
                    'ext_link': project.ext_link,
                    'content': post.content,
                    'author_id': post.author_id,
                }
                return render(request, 'project/write.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('/project/'+project_id)
        else:
            return render(request, 'project/write.html')

def update_status(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        status = request.POST.get('status')
        project = get_object_or_404(Project, id=project_id)
        project.status = status
        project.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
