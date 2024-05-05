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
    }
    else {
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
    }
    else {
        cursorSpan.classList.remove('typing');
        textArrayIndex++;
        if (textArrayIndex >= textArray.length) textArrayIndex = 0;
        setTimeout(type, typingDelay + 1100);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    if (textArray.length) setTimeout(type, newTextDelay + 250);
});

jQuery(document).ready(function () {
    jQuery.get('/portfolio', function (data) {
        jQuery('#portfolio').html(data);
        jQuery('#portfolio .navbar').remove();
        jQuery('#portfolio .chatbot-container').remove();
        jQuery('#portfolio .select-group').remove();
        jQuery('#portfolio .page').remove();
        jQuery('#portfolio .button-black').text('더보기');
        jQuery('#portfolio .button-black').css('margin-top', '15px');
        jQuery('#portfolio .button-black').attr('onclick', "window.location.href='/portfolio'");
    });

    jQuery.get('/project', function (data) {
        jQuery('#project').html(data);
        jQuery('#project .navbar').remove();
        jQuery('#project .chatbot-container').remove();
        jQuery('#project .select-group').remove();
        jQuery('#project .page').remove();
        jQuery('#project .button-black').text('더보기');
        jQuery('#project .button-black').css('margin-top', '15px');
        jQuery('#project .button-black').attr('onclick', "window.location.href='/project'");
    });

    jQuery.get('/qna', function (data) {
        jQuery('#qna').html(data);
        jQuery('#qna .navbar').remove();
        jQuery('#qna .chatbot-container').remove();
        jQuery('#qna .select-group').remove();
        jQuery('#qna .page').remove();
        jQuery('#qna .button-black').text('더보기');
        jQuery('#qna .button-black').css('margin-top', '15px');
        jQuery('#qna .button-black').attr('onclick', "window.location.href='/qna'");
    });
});
