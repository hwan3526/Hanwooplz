const idProfileImage = document.getElementById('id_profile_image');
const profileImage = document.getElementById('profile-image');

idProfileImage.addEventListener("change", function () {
    profileImage.src = URL.createObjectURL(this.files[0]);
});

profileImage.addEventListener("load", function () {
    URL.revokeObjectURL(profileImage.src)
});
