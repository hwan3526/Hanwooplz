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

def list(request):
    post_per_page = 9

    project = Project.objects.order_by('-id')
    project_list = []

    search = request.GET.get('search')
    search_type = request.GET.get('search-type')

    if search:
        if search_type == 'title-content':
            project = project.filter(
                Q(post__title__icontains=search) | Q(post__content__icontains=search)
            )
        elif search_type == 'writer':
            project = project.filter(
                Q(post__author__username__icontains=search)
            )

    filter_option = request.GET.get('filter-option')
    if filter_option == 'process':
        project = project.filter(status=1)
    elif filter_option == 'stop':
        project = project.filter(status=0)
    elif filter_option == 'done':
        project = project.filter(status=2)
    
    page = int(request.GET.get('page', 1))
    paginator = Paginator(project, post_per_page)
    project_page = paginator.get_page(page)
    page_start = page//10*10
    page_end = min(paginator.num_pages, page//10*10+10)
    page_range = paginator.page_range[page_start:page_end]

    for project in project_page:
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
        'project_list': project_list,
        'page_range': page_range,
        'current': project_page.number,
    }

    previous = page_range[0]-1
    next = page_range[-1]+1

    if previous in paginator.page_range:
        context['previous'] = previous
    if next in paginator.page_range:
        context['next'] = next

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

@login_required(login_url='/login')
def write(request):
    project = Project()
    post = Post()

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        project_form = ProjectForm(request.POST, request.FILES, instance=project)

        if post_form.is_valid() and project_form.is_valid():
            post = post_form.save(commit=False)
            project = project_form.save(commit=False)

            post.author_id = request.user.id
            post.category = 1
            post.save()
            project.post_id = post.id
            project.save()

            return redirect('/project/'+str(project.id))
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'target_members': request.POST.get('target_members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'project/write.html', context)
    else:
        return render(request, 'project/write.html')

@login_required(login_url='/login')
def edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    post = get_object_or_404(Post, id=project.post_id)

    if request.user.id != post.author_id:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('/project/'+str(project_id))

    if request.method == 'POST':        
        project_form = ProjectForm(request.POST, request.FILES, instance=project)
        post_form = PostForm(request.POST, request.FILES, instance=post)

        if project_form.is_valid() and post_form.is_valid():
            project_form.save()
            post_form.save()

            return redirect('/project/'+str(project_id))
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'target_members': request.POST.get('target_members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'project/write.html', context)
    else:
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

@login_required(login_url='/login')
def delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    post = get_object_or_404(Post, id=project.post_id)

    if request.user.id != post.author_id:
        return redirect('/project/'+str(project_id))

    post.delete()
    return redirect('/project')

def update_status(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        status = request.POST.get('status')
        project = get_object_or_404(Project, id=project_id)
        project.status = status
        project.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
