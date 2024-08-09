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
    items_per_page = 10

    question = Question.objects.order_by('-id')
    question_list = []

    query = request.GET.get('search')
    search_type = request.GET.get('search-type')

    filtered_questions = question
    if query:
        if search_type == 'title-content':
            filtered_questions = question.filter(
                Q(post__title__icontains=query) | Q(post__content__icontains=query)
            )
        elif search_type == 'writer':
            filtered_questions = question.filter(
                Q(post__author__username__icontains=query)
            )
    else:
        query = ''
        search_type = ''

    page = request.GET.get('page', page_num)
    paginator = Paginator(filtered_questions, items_per_page)
    page_obj = paginator.get_page(page)

    for question in page_obj:
        post = Post.objects.get(id=question.post_id)
        author = UserProfile.objects.get(id=post.author_id)

        question_list.append({
                    'question_id': question.id,
                    'title': post.title,
                    'author': author.username,
                    'created_at': post.created_at,
                })

    context = {
        'post_list': question_list,
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
    }

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
def write_question(request, question_id=None):
    if question_id:
        question = get_object_or_404(Question, id=question_id)
        post = get_object_or_404(Post, id=question.post_id)
    else:
        question = Question()
        post = Post()
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('/qna')
        
        post_form = PostForm(request.POST, request.FILES, instance=post)
        question_form = QuestionForm(request.POST, request.FILES, instance=question)

        if post_form.is_valid() and question_form.is_valid():
            post = post_form.save(commit=False)
            question = question_form.save(commit=False)
            if not question_id:
                post.author_id = request.user.id
                post.category = 2
                post.save()
                question.post_id = post.id
                question.save()
                question_id = question.id
            else:
                post.save()
                question.save()

            return redirect('/qna/'+question_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'keyword': request.POST.get('keyword'),
                'content': request.POST.get('content'),
            }
            return render(request, 'qna/write_question.html', context)
    else:
        if question_id:
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
                return redirect('/qna/'+question_id)
        else:
            return render(request, 'qna/write_question.html')

@login_required(login_url='/login')
def write_answer(request, question_id, answer_id=None):
    if question_id:
        question = get_object_or_404(Question, id=question_id)
        post_q = get_object_or_404(Post, id=question.post_id)
        author_q = get_object_or_404(UserProfile, id=post_q.author_id)
        if answer_id:
            answer = get_object_or_404(Answer, id=answer_id)
            post_a = get_object_or_404(Post, id=answer.post_id)
        else:
            answer = Answer()
            post_a = Post()
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('/qna')
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post_a.delete()
            return redirect('/qna/'+question_id)

        request.POST._mutable = True
        request.POST['title'] = '제목없음'
        post_form = PostForm(request.POST, request.FILES, instance=post_a)

        if post_form.is_valid():
            post_a = post_form.save(commit=False)
            if not answer_id:
                post_a.author_id = request.user.id
                post_a.category = 3
                post_a.save()
                answer.post_id = post_a.id
                answer.question_id = question_id
                answer.save()
            else:
                post_a.save()
                answer.save()

            return redirect('/qna/'+question_id)
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
                'answer': request.POST.get('answer'),
            }
            return render(request, 'qna/write_answer.html', context)
    else:
        if answer_id:
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
                return redirect('/qna/'+question_id)
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
        return redirect('/qna/'+question_id)
    return redirect('/qna/'+question_id)
