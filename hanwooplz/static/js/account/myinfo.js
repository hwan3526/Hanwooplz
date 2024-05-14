$(document).ready(function () {
    $('.category-button').click(function (event) {
        event.preventDefault();
        let category = $(this).data('category');
        let form = $('<form action="" method="get"></form>');
        form.append(`<input type="hidden" name="category" value="${category}">`);
        form.appendTo('body').submit();
    });
});
