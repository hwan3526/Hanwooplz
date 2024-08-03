const showCommentsLink = document.getElementById('show-comment');
const commentContainer = document.getElementById('comment-wrapper');
let isHidden = true;

showCommentsLink.addEventListener('click', function (event) {
    event.preventDefault();

    if (isHidden) {
        commentContainer.style.display = 'block';
        isHidden = false;
    } else {
        commentContainer.style.display = 'none';
        isHidden = true;
    }
});
