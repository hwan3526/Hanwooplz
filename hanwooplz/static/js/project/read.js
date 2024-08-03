function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function sendApplication(recipientId, postId) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch('/send-application/', {
        method: 'POST',
        body: JSON.stringify({ recipient_id: recipientId, post_id: postId }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    });
    const data = await response.json();
    if (data.success) {
        alert('참가신청이 성공적으로 요청되었습니다.');
    } else {
        alert('이미 참가요청한 게시물입니다.');
    }
}

let joinButton = document.getElementById('joinProjectButton');

if (joinButton) {
    joinButton.addEventListener('click', function () {
        let recipientId = joinButton.getAttribute('data-recipient-id');
        let postId = joinButton.getAttribute('data-post-id');
        sendApplication(recipientId, postId);
    });
}
