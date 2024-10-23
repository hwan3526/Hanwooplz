from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from post.forms import PostForm
from qna.forms import QuestionForm
from account.models import UserProfile
from post.models import Post
from qna.models import Question, Answer, AnswerLike

def list(request, page_num=1):
    post_per_page = 10

    question = Question.objects.order_by('-id')
    question_list = []

    search = request.GET.get('search')
    search_type = request.GET.get('search-type')

    if search:
        if search_type == 'title-content':
            question = question.filter(
                Q(post__title__icontains=search) | Q(post__content__icontains=search)
            )
        elif search_type == 'writer':
            question = question.filter(
                Q(post__author__username__icontains=search)
            )

    page = int(request.GET.get('page', 1))
    paginator = Paginator(question, post_per_page)
    question_page = paginator.get_page(page)
    page_start = page//10*10
    page_end = min(paginator.num_pages, page//10*10+10)
    page_range = paginator.page_range[page_start:page_end]

    for question in question_page:
        post = Post.objects.get(id=question.post_id)
        author = UserProfile.objects.get(id=post.author_id)

        question_list.append({
                    'question_id': question.id,
                    'title': post.title,
                    'author': author.username,
                    'created_at': post.created_at,
                })

    context = {
        'question_list': question_list,
        'page_range': page_range,
        'current': question_page.number,
    }

    previous = page_range[0]-1
    next = page_range[-1]+1

    if previous in paginator.page_range:
        context['previous'] = previous
    if next in paginator.page_range:
        context['next'] = next

    return render(request, 'qna/list.html', context)

def read(request, question_id=None):
    if question_id:
        question = get_object_or_404(Question, id=question_id)
        post_q = get_object_or_404(Post, id=question.post_id)
        author_q = get_object_or_404(UserProfile, id=post_q.author_id)

        answer = Answer.objects.filter(question_id=question_id)
        if answer:
            post_a = Post.objects.filter(id__in=answer.values_list('post_id', flat=True))
            author_a = UserProfile.objects.filter(id__in=post_a.values_list('author_id', flat=True))
            answer, post_a , author_a = answer.values(), post_a.values(), author_a.values()
            for p in post_a:
                p['answer_id'] = p['id']
                p.pop('id')
            for a in author_a:
                a.pop('id')
            answers = []
            answer_post_id_list = []
            for i in range(len(answer)):
                likes = AnswerLike.objects.filter(answer=answer[i]['id']).count()
                answers.append({**answer[i],**post_a[i],**author_a[i],'likes': likes})
                answer_post_id_list.append(answer[i]['post_id'])
            answered = True if request.user.id in post_a.values_list('author_id', flat=True) else False
        else:
            answers = []
            answered = False
            answer_post_id_list = []

        context = {
            'question_id' : question_id,
            'title': post_q.title,
            'author': author_q.username,
            'created_at': post_q.created_at,
            'keyword': question.keyword.split(),
            'content': post_q.content,
            'like': question.like.count(),
            'post_id': post_q.id,
            'author_id': author_q.id,
            'answer': answers,
            'answer_post_id_list': answer_post_id_list,
            'answered': answered,
        }
        return render(request, 'qna/read.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('/qna')

@login_required(login_url='/login')
def write_question(request):
    question = Question()
    post = Post()

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        question_form = QuestionForm(request.POST, request.FILES, instance=question)

        if post_form.is_valid() and question_form.is_valid():
            post = post_form.save(commit=False)
            question = question_form.save(commit=False)

            post.author_id = request.user.id
            post.category = 2
            post.save()
            question.post_id = post.id
            question.save()

            return redirect('/qna/'+str(question.id))
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'keyword': request.POST.get('keyword'),
                'content': request.POST.get('content'),
            }
            return render(request, 'qna/write_question.html', context)
    else:
        return render(request, 'qna/write_question.html')

@login_required(login_url='/login')
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    post = get_object_or_404(Post, id=question.post_id)

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        question_form = QuestionForm(request.POST, request.FILES, instance=question)

        if post_form.is_valid() and question_form.is_valid():
            post_form.save()
            question_form.save()

            return redirect('/qna/'+str(question_id))
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'keyword': request.POST.get('keyword'),
                'content': request.POST.get('content'),
            }
            return render(request, 'qna/write_question.html', context)
    else:
        if request.user.id == post.author_id:
            context = {
                'question_id': question_id,
                'title': post.title,
                'keyword': question.keyword,
                'content': post.content,
                'author_id': post.author_id,
            }
            return render(request, 'qna/write_question.html', context)
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('/qna/'+str(question_id))

@login_required(login_url='/login')
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    post = get_object_or_404(Post, id=question.post_id)

    if request.user.id == post.author_id:
        post.delete()
        return redirect('/qna')
    else:
        return redirect('/qna/'+str(question_id))

@login_required(login_url='/login')
def write_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    post_q = get_object_or_404(Post, id=question.post_id)
    author_q = get_object_or_404(UserProfile, id=post_q.author_id)

    answer = Answer()
    post_a = Post()

    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['title'] = 'Untitled'
        post_form = PostForm(request.POST, request.FILES, instance=post_a)

        if post_form.is_valid():
            post_a = post_form.save(commit=False)

            post_a.author_id = request.user.id
            post_a.category = 3
            post_a.save()
            answer.post_id = post_a.id
            answer.question_id = question_id
            answer.save()

            return redirect('/qna/'+str(question_id))
        else:
            messages.info(request, '답변을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'question_id': question_id,
                'title': post_q.title,
                'author': author_q.username,
                'created_at': post_q.created_at,
                'keyword': question.keyword.split(),
                'content': post_q.content,
                'author_id': author_q.id,
                'answer': request.POST.get('content'),
            }
            return render(request, 'qna/write_answer.html', context)
    else:        
        context = {
                'question_id': question_id,
                'title': post_q.title,
                'author': author_q.username,
                'created_at': post_q.created_at,
                'keyword': question.keyword.split(),
                'content': post_q.content,
                'author_id': author_q.id,
        }
        return render(request, 'qna/write_answer.html', context)

@login_required(login_url='/login')
def edit_answer(request, question_id, answer_id):
    question = get_object_or_404(Question, id=question_id)
    post_q = get_object_or_404(Post, id=question.post_id)
    author_q = get_object_or_404(UserProfile, id=post_q.author_id)

    answer = get_object_or_404(Answer, id=answer_id)
    post_a = get_object_or_404(Post, id=answer.post_id)

    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['title'] = 'Untitled'
        post_form = PostForm(request.POST, request.FILES, instance=post_a)

        if post_form.is_valid():
            post_form.save()

            return redirect('/qna/'+str(question_id))
        else:
            messages.info(request, '답변을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'question_id': question_id,
                'title': post_q.title,
                'author': author_q.username,
                'created_at': post_q.created_at,
                'keyword': question.keyword.split(),
                'content': post_q.content,
                'author_id': author_q.id,
                'answer': request.POST.get('content'),
            }
            return render(request, 'qna/write_answer.html', context)
    else:
        if request.user.id == post_a.author_id:
            context = {
                'question_id': question_id,
                'title': post_q.title,
                'author': author_q.username,
                'created_at': post_q.created_at,
                'keyword': question.keyword.split(),
                'content': post_q.content,
                'author_id': author_q.id,
                'answer_id': answer_id,
                'answer': post_a.content,
            }
            return render(request, 'qna/write_answer.html', context)
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('/qna/'+str(question_id))

@login_required(login_url='/login')
def delete_answer(request, question_id, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    post = get_object_or_404(Post, id=answer.post_id)

    if request.user.id == post.author_id:
        post.delete()
        return redirect('/qna/'+str(question_id))
    else:
        return redirect('/qna/'+str(question_id))

@login_required(login_url='/login')
def like(request, question_id, answer_id=None):
    if request.user.is_authenticated:
        if not answer_id:
            post = get_object_or_404(Question, id=question_id)
        else:
            post = get_object_or_404(Answer, id=answer_id)
        user = get_object_or_404(UserProfile, id=request.user.id)

        if user in post.like.all():
            post.like.remove(user)
        else:
            post.like.add(user)

        post.save()
        return redirect('/qna/'+str(question_id))
    return redirect('/qna/'+str(question_id))
