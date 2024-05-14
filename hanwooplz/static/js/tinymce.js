tinymce.init({
    selector: 'textarea#content',
    plugins: 'advcode advlist advtable autosave charmap codesample editimage emoticons help image link lists nonbreaking pagebreak searchreplace table visualblocks visualchars preview',
    menubar: 'edit view insert format table',
    toolbar1: 'checklist bullist numlist | link image | removeformat | preview | help',
    toolbar2: 'fontselect fontsizeselect | bold italic underline forecolor backcolor | align lineheight | indent outdent',
    resize: false,
    toolbar_sticky: true,
    image_dimensions: false,
    image_description: false,
    automatic_uploads: false,
    file_picker_types: 'image',

    file_picker_callback: function (cb, value, meta) {
        let input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        input.onchange = function () {
            let file = this.files[0];
            let reader = new FileReader();
            reader.onload = function () {
                let id = 'blobid' + (new Date()).getTime();
                let blobCache = tinymce.activeEditor.editorUpload.blobCache;
                let base64 = reader.result.split(',')[1];
                let blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    },
});

let question_container = document.querySelector('.question-container');
if (question_container != null) {
    question_container.style.width = '30%';
    question_container.style.margin = '0px 20px 0px 0px';
}
