const typedTextSpan = document.querySelector('.typed-text');
const cursorSpan = document.querySelector('.cursor');

const textArray = ['Hard', 'Fun', 'Career', 'Life'];
const typingDelay = 200;
const erasingDelay = 100;
const newTextDelay = 2000;
let textArrayIndex = 0;
let charIndex = 0;

function type() {
    if (charIndex < textArray[textArrayIndex].length) {
        if (!cursorSpan.classList.contains('typing')) cursorSpan.classList.add('typing');
        typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, typingDelay);
    } else {
        cursorSpan.classList.remove('typing');
        setTimeout(erase, newTextDelay);
    }
}

function erase() {
    if (charIndex > 0) {
        if (!cursorSpan.classList.contains('typing')) cursorSpan.classList.add('typing');
        typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erase, erasingDelay);
    } else {
        cursorSpan.classList.remove('typing');
        textArrayIndex++;
        if (textArrayIndex >= textArray.length) textArrayIndex = 0;
        setTimeout(type, typingDelay + 1100);
    }
}

if (textArray.length) {
    setTimeout(type, newTextDelay + 250);
}

$.get('/portfolio', function (data) {
    $('#portfolio').html(data);
    let content = $('#portfolio .post-list').clone();
    $('#portfolio').html(content);
    $('#portfolio .select-group').remove();
    $('#portfolio .page').remove();
    $('#portfolio .button-black').text('더보기');
    $('#portfolio .button-black').css('margin-top', '15px');
    $('#portfolio .button-black').attr('onclick', "window.location.href='/portfolio'");
});

$.get('/project', function (data) {
    $('#project').html(data);
    let content = $('#project .post-list').clone();
    $('#project').html(content);
    $('#project .select-group').remove();
    $('#project .tab-container').remove();
    $('#project .page').remove();
    $('#project .button-black').text('더보기');
    $('#project .button-black').css('margin-top', '15px');
    $('#project .button-black').attr('onclick', "window.location.href='/project'");
});

$.get('/qna', function (data) {
    $('#qna').html(data);
    let content = $('#qna .post-list').clone();
    $('#qna').html(content);
    $('#qna .select-group').remove();
    $('#qna .page').remove();
    $('#qna .button-black').text('더보기');
    $('#qna .button-black').css('margin-top', '15px');
    $('#qna .button-black').attr('onclick', "window.location.href='/qna'");
});
