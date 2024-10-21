const profilePostTab = document.querySelectorAll('.profile-post-tab');
const profilePostGrid = document.querySelectorAll('.profile-post-grid');

for (let i = 0; i < 4; i++) {
    profilePostTab[i].addEventListener('click', function () {
        for (let j = 0; j < 4; j++) {
            if (j == i) {
                profilePostTab[j].classList.add('active');
                profilePostGrid[j].classList.add('active');
            } else {
                profilePostTab[j].classList.remove('active');
                profilePostGrid[j].classList.remove('active');
            }
        }
    });
}

const profilePost = document.querySelector('.profile-post');

let heights = []
for (let i = 0; i < 4; i++) {
    profilePostTab[i].click();
    heights.push(profilePostGrid[i].offsetHeight);
}

profilePost.style.height = 81 + Math.max(...heights) + 'px';
profilePostTab[0].click();
