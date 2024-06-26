from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from post.forms import PostForm
from qna.forms import PostQuestionForm
from account.models import UserProfile
from post.models import Post
from qna.models import PostQuestion, PostAnswer, AnswerLike

def qna_list(request, page_num=1):
    items_per_page = 10  # 페이지 당 항목 수

    post_question = PostQuestion.objects.order_by('-id')
    question_lists = []

    query = request.GET.get('search')
    search_type = request.GET.get('search_type')  # 검색 옵션을 가져옵니다

    # 검색
    filtered_questions = post_question
    if query:
        if search_type == 'title_content':
            filtered_questions = post_question.filter(
                Q(post__title__icontains=query) | Q(post__content__icontains=query)
            )
        elif search_type == 'writer':
            filtered_questions = post_question.filter(
                Q(post__author__username__icontains=query)
            )
    else:
        query = ''
        search_type = ''

    # 페이지네이션
    page = request.GET.get('page', page_num)
    paginator = Paginator(filtered_questions, items_per_page)
    page_obj = paginator.get_page(page)

    for question in page_obj:
        post = Post.objects.get(id=question.post_id)
        author = UserProfile.objects.get(id=post.author_id)

        question_lists.append({
                    'title': post.title,
                    'created_at': post.created_at,
                    'author_id': post.author_id,
                    'post_question': question.id,
                    'author': author.username,
                })

    context = {
        'post_lists': question_lists,
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
    }

    return render(request, 'qna/qna_list.html', context)

def qna_read(request, post_question_id=None):
    if post_question_id:
        post_question = get_object_or_404(PostQuestion, id=post_question_id)
        post = get_object_or_404(Post, id=post_question.post_id)
        author = get_object_or_404(UserProfile, id=post.author_id)

        post_answer = PostAnswer.objects.filter(question_id=post_question_id)
        if post_answer:
            post_ = Post.objects.filter(id__in=post_answer.values_list('post_id', flat=True))
            author_ = UserProfile.objects.filter(id__in=post_.values_list('author_id', flat=True))
            post_answer, post_ , author_ = post_answer.values(), post_.values(), author_.values()
            for p_ in post_:
                p_['answer_id'] = p_['id']
                p_.pop('id')
            for a_ in author_:
                a_.pop('id')
            answers = []
            answer_post_id_list = []
            for i in range(len(post_answer)):
                likes = AnswerLike.objects.filter(answer=post_answer[i]['id']).count()
                answers.append({**post_answer[i],**post_[i],**author_[i],'likes': likes})
                answer_post_id_list.append(post_answer[i]['post_id'])
            answered = True if request.user.id in post_.values_list('author_id', flat=True) else False
        else:
            answers = []
            answered = False
            answer_post_id_list = []

        context = {
            'title': post.title,
            'content': post.content,
            'author': author.username,
            'author_id': author.id,
            'created_at': post.created_at,
            'like': post_question.like.count(),
            'keywords': post_question.keyword,
            'post_question_id' : post_question_id,
            'post_id': post.id,
            'answers': answers,
            'answer_post_id_list': answer_post_id_list,
            'answered': answered,
        }
        return render(request, 'qna/qna_read.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('qna:qna_list')

@login_required(login_url='login')
def qna_write_question(request, post_question_id=None):
    if post_question_id:
        post_question = get_object_or_404(PostQuestion, id=post_question_id)
        post = get_object_or_404(Post, id=post_question.post_id)
    else:
        post_question = PostQuestion()
        post = Post()
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('qna:qna_list')
        
        request.POST._mutable = True
        request.POST['keyword'] = request.POST.get('keyword').split()
        post_form = PostForm(request.POST, request.FILES, instance=post)
        post_question_form = PostQuestionForm(request.POST, request.FILES, instance=post_question)

        if post_form.is_valid() and post_question_form.is_valid():
            post = post_form.save(commit=False)
            post_question = post_question_form.save(commit=False)
            if not post_question_id:
                post.author_id = request.user.id
                post.save()
                post_question.post_id = post.id
                post_question.save()
                post_question_id = post_question.id
            else:
                post.save()
                post_question.save()

            return redirect('qna:qna_read', post_question_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'keyword': request.POST.get('keyword'),
            }
            return render(request, 'qna/write_question.html', context)
    else:
        if post_question_id:
            if request.user.id == post.author_id:
                context = {
                    'post_question_id': post_question_id,
                    'title': post.title,
                    'content': post.content,
                    'keyword': ' '.join(post_question.keyword),
                    'post_author_id': post.author_id,
                }
                return render(request, 'qna/write_question.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('qna:qna_read', post_question_id)
        else:
            return render(request, 'qna/write_question.html')

@login_required(login_url='login')
def qna_write_answer(request, post_question_id, post_answer_id=None):
    if post_question_id:
        post_question = get_object_or_404(PostQuestion, id=post_question_id)
        post_ = get_object_or_404(Post, id=post_question.post_id)
        author_ = get_object_or_404(UserProfile, id=post_.author_id)
        if post_answer_id:
            post_answer = get_object_or_404(PostAnswer, id=post_answer_id)
            post = get_object_or_404(Post, id=post_answer.post_id)
        else:
            post_answer = PostAnswer()
            post = Post()
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('qna:qna_list')
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('qna:qna_read', post_question_id)
        if 'temp-save-button' in request.POST:
            messages.info(request, '임시저장은 현재 지원되지 않는 기능입니다.')
            context={
                'title_question': post_.title,
                'keywords_question': post_question.keyword,
                'content_question': post_.content,
                'author_question': author_.username,
                'author_id_question': author_.id,
                'created_at_question': post_.created_at,
                'post_question_id': post_question_id,
                'content': request.POST.get('content'),
            }
            return render(request, 'qna/write_answer.html', context)
        
        request.POST._mutable = True
        request.POST['title'] = '제목없음'
        post_form = PostForm(request.POST, request.FILES, instance=post)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            if not post_answer_id:
                post.author_id = request.user.id
                post.save()
                post_answer.post_id = post.id
                post_answer.question_id = post_question_id
                post_answer.save()
            else:
                post.save()
                post_answer.save()

            return redirect('qna:qna_read', post_question_id)
        else:
            messages.info(request, '답변을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title_question': post_.title,
                'keywords_question': post_question.keyword,
                'content_question': post_.content,
                'author_question': author_.username,
                'author_id_question': author_.id,
                'created_at_question': post_.created_at,
                'post_question_id': post_question_id,
                'content': request.POST.get('content'),
            }
            return render(request, 'qna/write_answer.html', context)
    else:
        if post_answer_id:
            if request.user.id == post.author_id:
                context = {
                    'title_question': post_.title,
                    'keywords_question': post_question.keyword,
                    'content_question': post_.content,
                    'author_question': author_.username,
                    'author_id_question': author_.id,
                    'created_at_question': post_.created_at,
                    'post_question_id': post_question_id,
                    'post_answer_id': post_answer_id,
                    'content': post.content,
                    'post_author_id': post.author_id,
                }
                return render(request, 'qna/write_answer.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('qna:qna_read', post_question_id)
        else:
            context = {
                    'title_question': post_.title,
                    'keywords_question': post_question.keyword,
                    'content_question': post_.content,
                    'author_question': author_.username,
                    'author_id_question': author_.id,
                    'created_at_question': post_.created_at,
                    'post_question_id': post_question_id,
            }
            return render(request, 'qna/write_answer.html', context)

@login_required
def like(request, post_question_id, answer_id=None):
    if request.user.is_authenticated:
        if not answer_id:
            post = get_object_or_404(PostQuestion, pk=post_question_id)
        else:
            post = get_object_or_404(PostAnswer, pk=answer_id)
        user = get_object_or_404(UserProfile, pk=request.user.id)

        if user in post.like.all():
            post.like.remove(user)
            message = '추천이 취소됐습니다.'
        else:
            post.like.add(user)
            message = ''

        post.save()
        return redirect('qna:qna_read', post_question_id)
    return redirect('qna:qna_read', post_question_id)
