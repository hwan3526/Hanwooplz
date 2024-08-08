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

def list(request, page_num=1):
    items_per_page = 9

    portfolio = Portfolio.objects.order_by('-id')
    portfolio_list = []

    query = request.GET.get('search')
    search_type = request.GET.get('search-type')

    filtered_portfolios = portfolio
    if query:
        if search_type == 'title-content':
            filtered_portfolios = portfolio.filter(
                Q(post__title__icontains=query) | Q(post__content__icontains=query)
            )
        elif search_type == 'writer':
            filtered_portfolios = portfolio.filter(
                Q(post__author__username__icontains=query)
            )
    else:
        query = ''
        search_type = ''

    page = request.GET.get('page', page_num)
    paginator = Paginator(filtered_portfolios, items_per_page)
    page_obj = paginator.get_page(page)

    for portfolio in page_obj:
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
        'post_list': portfolio_list,
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
    }

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
            'created_at': post.created_at,
            'start_date': portfolio.start_date,
            'end_date': portfolio.end_date,
            'members': portfolio.members,
            'tech_stack': portfolio.tech_stack.split(),
            'ext_link': portfolio.ext_link,
            'content': post.content,
            'post_id': post.id,
            'author_id': author.id,
        }
        return render(request, 'portfolio/read.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('/portfolio')

@login_required(login_url='login')
def write(request, portfolio_id=None):
    if portfolio_id:
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        post = get_object_or_404(Post, id=portfolio.post_id)
    else:
        portfolio = Portfolio()
        post = Post()
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('/portfolio')
        
        post_form = PostForm(request.POST, request.FILES, instance=post)
        portfolio_form = PortfolioForm(request.POST, request.FILES, instance=portfolio)

        if post_form.is_valid() and portfolio_form.is_valid():
            post = post_form.save(commit=False)
            portfolio = portfolio_form.save(commit=False)
            if not portfolio_id:
                post.author_id = request.user.id
                post.save()
                portfolio.post_id = post.id
                portfolio.save()
                portfolio_id = portfolio.id
            else:
                post.save()
                portfolio.save()

            return redirect('/portfolio/'+portfolio_id)
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
        if portfolio_id:
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
                return redirect('/portfolio/'+portfolio_id)
        else:
            return render(request, 'portfolio/write.html')
