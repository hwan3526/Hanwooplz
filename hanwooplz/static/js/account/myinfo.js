$(document).ready(function () {
    $('.category-button').click(function (event) {
        event.preventDefault();
        var category = $(this).data('category');
        var form = $('<form action="" method="get"></form>');
        form.append(`<input type="hidden" name="category" value="${category}">`);
        form.appendTo('body').submit();
    });
});
