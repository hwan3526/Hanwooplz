const searchSelect = document.getElementById('search-select');
const searchForm = document.getElementById('search-form');

searchSelect.addEventListener('change', function () {
    let selectedOption = this.value;
    let currentURL = window.location.href;
    let newURL;

    if (currentURL.includes('?')) {
        let searchParams = new URLSearchParams(currentURL.split('?')[1]);
        searchParams.set('search_type', selectedOption);
        newURL = window.location.pathname + '?' + searchParams.toString();
    } else {
        newURL = window.location.pathname + '?search_type=' + selectedOption;
    }
    searchForm.action = newURL;
});

let searchType = new URLSearchParams(window.location.search).get('search_type');
let titleElement = document.querySelector('.posts-list h2');

if (searchType === 'title_content') {
    titleElement.textContent = '질의응답: 제목+내용 검색결과';
} else if (searchType === 'writer') {
    titleElement.textContent = '질의응답: 작성자 검색결과';
}
