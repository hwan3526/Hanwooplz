let answerContainer = document.querySelectorAll('.answer-container')

if (answerContainer) {
    answerContainer.forEach(container => {
        let answerId = container.getAttribute('data-answer-id');
        let showComments = container.querySelector('#unpack-comments');
        let commentContainer = container.querySelector('.comment-container');
        let commentText = commentContainer.querySelector('#comment-input');
        let submitButton = commentContainer.querySelector('#comment-submit-button');
        let csrfToken = commentContainer.querySelector('input[name=csrfmiddlewaretoken]').value;
        let isHidden = true;

        // 댓글 펼치기
        showComments.addEventListener('click', function (event) {
            event.preventDefault();

            if (isHidden) {
                commentContainer.style.display = 'block';
                isHidden = false;
            } else {
                commentContainer.style.display = 'none';
                isHidden = true;
            }
        })

        // 댓글 불러오기
        function fetchComment() {
            fetch(`/api/post/${answerId}/comments/`)
                .then(function (response) {
                    return response.json();
                })
                .then(function (comments) {
                    let commentList = commentContainer.querySelector(`.comment-list`);
                    commentList.innerHTML = '';
                    comments.forEach(function (comment) {
                        let commentBox = document.createElement('div');
                        commentBox.classList.add('comment-box');

                        // 댓글 작성자
                        let commentAuthor = document.createElement('div');
                        commentAuthor.classList.add('comment-author');
                        commentAuthor.textContent = comment.author;

                        // 댓글 내용
                        let commentContent = document.createElement('div');
                        commentContent.classList.add('comment-content');
                        commentContent.textContent = comment.content;

                        // 댓글 작성 시각
                        let commentTimestamp = document.createElement('div');
                        commentTimestamp.classList.add('comment-createdat');

                        let date = new Date(comment.created_at);
                        let formattedDate = date.toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
                        commentTimestamp.textContent = formattedDate;

                        // 댓글 좋아요 + 삭제
                        let commentBottomWrapper = document.createElement('div');
                        commentBottomWrapper.classList.add('comment-bottom-wrapper');

                        // 댓글 좋아요
                        let commentLike = document.createElement('a');
                        commentLike.classList.add('comment-like');
                        commentLike.setAttribute('id', comment.id);
                        commentLike.textContent = '👍 ' + comment.like.length;
                        commentLike.addEventListener('click', function () {
                            likeComment(comment.id);
                        });

                        commentBottomWrapper.appendChild(commentLike);
                        commentBox.appendChild(commentAuthor);
                        commentBox.appendChild(commentTimestamp);
                        commentBox.appendChild(commentContent);
                        commentBox.appendChild(commentBottomWrapper);
                        commentList.appendChild(commentBox);

                        // 댓글 삭제
                        if (currentUser === comment.author) {
                            let commentDelete = document.createElement('a');
                            commentDelete.classList.add('comment-delete');
                            commentDelete.textContent = '삭제';
                            commentDelete.addEventListener('click', function () {
                                let deleteConfirmed = confirm('댓글을 삭제하시겠습니까?');
                                if (deleteConfirmed) {
                                    deleteComment(comment.id);
                                }
                            })
                            commentBottomWrapper.appendChild(commentDelete);
                        }
                    });
                })
                .catch(function (error) {
                    alert('댓글을 가져오는 데 실패했습니다.');
                });
        }

        // 댓글 등록
        submitButton.addEventListener('click', function () {
            let commentData = {
                content: commentText.value
            };

            fetch(`/api/post/${answerId}/comments/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(commentData),
            })
                .then(function (response) {
                    if (response.status === 201) {
                        commentText.value = '';
                        fetchComment();
                    } else {
                        alert('댓글 작성에 실패했습니다.');
                    }
                });
        });

        // 댓글 추천
        function likeComment(commentId) {
            if (currentUser != 'AnonymousUser') {
                fetch(`/api/comment/${commentId}/like/`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                })
                    .then(function (response) {
                        if (response.status === 200) {
                            return response.json();
                        } else {
                            console.error('댓글 추천 또는 취소 실패');
                            return null;
                        }
                    })
                    .then(function (data) {
                        let message = data.message;
                        let data = data.comment_data;

                        let commentLike = document.getElementById(`${commentId}`);
                        commentLike.textContent = data.like.length;

                        if (message) {
                            alert(message);
                        }
                    })
                    .catch(function (error) {
                        console.error(error);
                    })
            } else {
                alert('댓글을 추천하려면 로그인이 필요합니다.');
            }
        }

        // 댓글 삭제
        function deleteComment(commentId) {
            fetch(`/api/comments/${commentId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            })
                .then(function (response) {
                    if (response.status === 204) {
                        commentText.value = '';
                        alert('댓글이 삭제되었습니다.')
                        return fetchComment();
                    } else if (response.status === 404) {
                        alert('존재하지 않는 댓글입니다.')
                    } else {
                        alert('댓글 삭제에 실패했습니다.');
                    }
                })
                .catch(function (error) {
                    console.error(error);
                });
        }

        commentContainer.style.display = 'none';
        fetchComment();
    })
}
