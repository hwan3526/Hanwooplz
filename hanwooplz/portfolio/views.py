from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from post.forms import PostForm
from portfolio.forms import PortfolioForm
from account.models import UserProfile
from post.models import Post
from portfolio.models import Portfolio

def list(request):
    post_per_page = 9

    portfolio = Portfolio.objects.order_by('-id')
    portfolio_list = []

    search = request.GET.get('search')
    search_type = request.GET.get('search-type')

    if search:
        if search_type == 'title-content':
            portfolio = portfolio.filter(
                Q(post__title__icontains=search) | Q(post__content__icontains=search)
            )
        elif search_type == 'writer':
            portfolio = portfolio.filter(
                Q(post__author__username__icontains=search)
            )

    page = int(request.GET.get('page', 1))
    paginator = Paginator(portfolio, post_per_page)
    portfolio_page = paginator.get_page(page)
    page_start = page//10*10
    page_end = min(paginator.num_pages, page//10*10+10)
    page_range = paginator.page_range[page_start:page_end]

    for portfolio in portfolio_page:
        post = Post.objects.get(id=portfolio.post_id)
        author = UserProfile.objects.get(id=post.author_id)

        portfolio_list.append({
            'portfolio_id': portfolio.id,
            'title': post.title,
            'author': author.username,
            'created_at': post.created_at,
            'tech_stack': portfolio.tech_stack.split()[0]
        })

    context = {
        'portfolio_list': portfolio_list,
        'page_range': page_range,
        'current_page': portfolio_page.number,
    }

    previous = page_range[0]-10
    next = page_range[-1]+1

    if previous in paginator.page_range:
        context['previous'] = previous
    if next in paginator.page_range:
        context['next'] = next

    return render(request, 'portfolio/list.html', context)

def read(request, portfolio_id=None):
    if portfolio_id:
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        post = get_object_or_404(Post, id=portfolio.post_id)
        author = get_object_or_404(UserProfile, id=post.author_id)
        context = {
            'portfolio_id' : portfolio_id,
            'title': post.title,
            'author': author.username,
            'created_at': post.created_at.replace(microsecond=0),
            'edited_at': post.edited_at.replace(microsecond=0),
            'start_date': portfolio.start_date,
            'end_date': portfolio.end_date,
            'members': portfolio.members,
            'tech_stack': portfolio.tech_stack.split(),
            'ext_link': portfolio.ext_link,
            'content': post.content,
            'post_id': post.id,
            'author_id': author.id,
        }
        if context['created_at']==context['edited_at']:
            context.pop('edited_at')

        return render(request, 'portfolio/read.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('/portfolio')

@login_required(login_url='/login')
def write(request):
    portfolio = Portfolio()
    post = Post()

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        portfolio_form = PortfolioForm(request.POST, request.FILES, instance=portfolio)

        if post_form.is_valid() and portfolio_form.is_valid():
            post = post_form.save(commit=False)
            portfolio = portfolio_form.save(commit=False)

            post.author_id = request.user.id
            post.category = 0
            post.save()
            portfolio.post_id = post.id
            portfolio.save()

            return redirect('/portfolio/'+str(portfolio.id))
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'members': request.POST.get('members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'portfolio/write.html', context)
    else:
        return render(request, 'portfolio/write.html')

@login_required(login_url='/login')
def edit(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    post = get_object_or_404(Post, id=portfolio.post_id)

    if request.method == 'POST':
        portfolio_form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        post_form = PostForm(request.POST, request.FILES, instance=post)

        if portfolio_form.is_valid() and post_form.is_valid():
            portfolio_form.save()
            post_form.save()

            return redirect('/portfolio/'+str(portfolio_id))
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'members': request.POST.get('members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'portfolio/write.html', context)
    else:
        if request.user.id == post.author_id:
            start_date = str(portfolio.start_date).replace('년 ','-').replace('월 ','-').replace('일','')
            end_date = str(portfolio.end_date).replace('년 ','-').replace('월 ','-').replace('일','')
            context = {
                'portfolio_id': portfolio_id,
                'title': post.title,
                'start_date': start_date,
                'end_date': end_date,
                'members': portfolio.members,
                'tech_stack': portfolio.tech_stack,
                'ext_link': portfolio.ext_link,
                'content': post.content,
                'author_id': post.author_id,
            }
            return render(request, 'portfolio/write.html', context)
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('/portfolio/'+str(portfolio_id))

@login_required(login_url='/login')
def delete(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    post = get_object_or_404(Post, id=portfolio.post_id)

    if request.user.id == post.author_id:
        post.delete()
        return redirect('/portfolio')
    else:
        return redirect('/portfolio/'+str(portfolio_id))
