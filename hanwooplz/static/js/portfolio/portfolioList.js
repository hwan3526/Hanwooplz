const searchSelect = document.getElementById('search-select');

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
    document.getElementById('search-form').action = newURL;
});

let searchType = new URLSearchParams(window.location.search).get('search_type');
let titleElement = document.querySelector('.post-list h2');

if (searchType === 'title_content') {
    titleElement.textContent = '포트폴리오: 제목+내용 검색결과';
} else if (searchType === 'writer') {
    titleElement.textContent = '포트폴리오: 작성자 검색결과';
}
