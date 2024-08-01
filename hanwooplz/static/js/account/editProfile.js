const idUserImg = document.getElementById('id_user_img');
const userImg = document.getElementById('user-img');

idUserImg.addEventListener("change", function () {
    userImg.src = URL.createObjectURL(this.files[0]);
});

userImg.addEventListener("load", function () {
    URL.revokeObjectURL(userImg.src)
});
