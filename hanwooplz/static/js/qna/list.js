const parameter = new URLSearchParams(window.location.search);
const searchType = parameter.get('search-type');
const search = parameter.get('search');
const title = document.querySelector('.main-container h2');
const page = document.querySelectorAll('.page a');

if (searchType && search) {
    if (searchType === 'title-content') {
        title.textContent = '포트폴리오: 제목+내용 검색결과';
    } else if (searchType === 'writer') {
        title.textContent = '포트폴리오: 작성자 검색결과';
    }

    page.forEach(function (pageNumber) {
        pageNumber.href += '&search-type=' + searchType + '&search=' + search;
    });
}
