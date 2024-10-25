const commentShow = document.querySelectorAll('.comment-show');
const comment = document.querySelectorAll('.comment');

for (let i = 0; i < commentShow.length; i++) {
    commentShow[i].addEventListener('click', function () {
        if (comment[i].classList.contains('inactive')) {
            comment[i].classList.remove('inactive');
        } else {
            comment[i].classList.add('inactive');
        }
    });
    commentShow[i].click();
}

const likeToggle = document.querySelectorAll('.like-toggle');

likeToggle[0].addEventListener('click', function () {
    let questionId = likeToggle[0].getAttribute('question-id');
    fetch(`/qna/like-question/${questionId}`)
        .then(response => { return response.text(); })
        .then(data => { likeToggle[0].innerText = '추천 ' + data + ' 회'; });
});

for (let i = 1; i < likeToggle.length; i++) {
    likeToggle[i].addEventListener('click', function () {
        let answerId = likeToggle[i].getAttribute('answer-id');
        fetch(`/qna/like-answer/${answerId}`)
            .then(response => { return response.text(); })
            .then(data => { likeToggle[i].innerText = '추천 ' + data + ' 회'; });
    });
}
