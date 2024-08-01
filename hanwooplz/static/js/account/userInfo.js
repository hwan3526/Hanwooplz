const portfolioTab = document.getElementById('portfolio-tab');
const projectTab = document.getElementById('project-tab');
const qnaTab = document.getElementById('qna-tab');

const portfolioPosts = document.getElementById('portfolio-posts');
const projectPosts = document.getElementById('project-posts');
const qnaPosts = document.getElementById('qna-posts');

portfolioTab.addEventListener('click', function () {
    portfolioTab.style.backgroundColor = '#dddddd';
    projectTab.style.backgroundColor = 'white';
    qnaTab.style.backgroundColor = 'white';

    portfolioPosts.style.display = 'grid';
    projectPosts.style.display = 'none';
    qnaPosts.style.display = 'none';
});

projectTab.addEventListener('click', function () {
    portfolioTab.style.backgroundColor = 'white';
    projectTab.style.backgroundColor = '#dddddd';
    qnaTab.style.backgroundColor = 'white';

    portfolioPosts.style.display = 'none';
    projectPosts.style.display = 'grid';
    qnaPosts.style.display = 'none';
});

qnaTab.addEventListener('click', function () {
    portfolioTab.style.backgroundColor = 'white';
    projectTab.style.backgroundColor = 'white';
    qnaTab.style.backgroundColor = '#dddddd';

    portfolioPosts.style.display = 'none';
    projectPosts.style.display = 'none';
    qnaPosts.style.display = 'grid';
});
