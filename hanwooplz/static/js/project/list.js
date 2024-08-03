const searchSelect = document.getElementById('search-select');

searchSelect.addEventListener('change', function () {
    let selectedOption = this.value;
    let currentURL = window.location.href;
    let newURL;
    if (currentURL.includes('?')) {
        let searchParams = new URLSearchParams(currentURL.split('?')[1]);
        searchParams.set('search-type', selectedOption);
        newURL = window.location.pathname + '?' + searchParams.toString();
    } else {
        newURL = window.location.pathname + '?search-type=' + selectedOption;
    }
    document.getElementById('search-form').action = newURL;
});

let searchType = new URLSearchParams(window.location.search).get('search-type');
let titleElement = document.querySelector('.post-list h2');

if (searchType === 'title-content') {
    titleElement.textContent = '프로젝트 팀원 모집: 제목+내용 검색결과';
} else if (searchType === 'writer') {
    titleElement.textContent = '프로젝트 팀원 모집: 작성자 검색결과';
}

const urlParams = new URLSearchParams(window.location.search);
const filterOption = urlParams.get('filter-option');
const tabList = document.querySelectorAll('.tab');

if (filterOption === 'recruiting') {
    document.querySelector('.tab a[href="?filter-option=recruiting"]').parentElement.classList.add('active');
} else {
    document.querySelector('.tab a[href="/project"]').parentElement.classList.add('active');
}
