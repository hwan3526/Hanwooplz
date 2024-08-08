const idProfileImage = document.getElementById('id_profile_image');
const profileImage = document.getElementById('profile-image');
const profileImageClearId = document.getElementById('profile_image-clear_id');
const profileImageClear = document.getElementById('profile-image-clear');

idProfileImage.addEventListener('change', function () {
    URL.revokeObjectURL(profileImage.src);
    profileImage.src = URL.createObjectURL(this.files[0]);

    profileImageClearId.checked = false;
});

profileImageClear.addEventListener('click', function () {
    URL.revokeObjectURL(profileImage.src);
    profileImage.src = '/static/img/basicuser.png';

    profileImageClearId.checked = true;
    idProfileImage.value = '';
});

const profileImageUpload = document.getElementById('profile-image-upload');

profileImageUpload.addEventListener('click', function () {
    document.getElementById('id_profile_image').click();
});
