const notificationButton = document.getElementById('notification-button');
const notificationCount = document.getElementById('notification-count');
const notificationContainer = document.getElementById('notification-container');
const notificationMessage = document.getElementById('notification-message');
let isNotificationVisible = false;
let notifications = [];

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

async function updateNotificationCount() {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch('/get_notifications', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    const data = await response.json();
    notifications = data.notifications.notifications_list;

    let unresponse_list = [];

    notifications.forEach(notification => {
        if (notification.accept_or_not === null && currentUser === notification.user) {
            unresponse_list.push(notification);
        } else if (notification.accept_or_not !== null && notification.read_or_not === false && currentUser !== notification.user) {
            unresponse_list.push(notification);
        }

    })

    if (unresponse_list.length > 0) {
        notificationCount.textContent = unresponse_list.length;
        notificationCount.style.display = 'block';
    } else {
        notificationCount.style.display = 'none';
    }

}

async function markNotificationsAsRead() {
    const unreadNotifications = notifications.filter(
        (notification) =>
            notification.accept_or_not !== null &&
            notification.read_or_not === false &&
            currentUser !== notification.user
    );
    console.log(unreadNotifications)
    if (unreadNotifications.length > 0) {
        const notificationIds = unreadNotifications.map((notification) => notification.id);
        console.log(notificationIds)
        const csrftoken = getCookie('csrftoken');
        await fetch('/mark_notifications_as_read/', {
            method: 'POST',
            body: JSON.stringify({ notificationIds }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        });

        unreadNotifications.forEach((notification) => {
            notification.read_or_not = true;
        });
    }
}

async function sendAcceptanceResult(notificationId, result) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch('/accept_reject_notification/', {
        method: 'POST',
        body: JSON.stringify({ notificationId, result }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    });
    const data = await response.json();
    if (data.success) {
        console.log('결과가 성공적으로 서버로 전송되었습니다.');
    } else {
        console.error('결과 서버로 전송 중 오류가 발생했습니다.');
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    updateNotificationCount();
});

notificationButton.addEventListener('click', async function (e) {
    e.stopPropagation();

    if (isNotificationVisible) {
        notificationContainer.style.display = 'none';
    } else {
        notificationContainer.style.display = 'block';
        notificationMessage.innerHTML = '';

        const incomingRequestContainer = document.createElement('div');
        const incomingRequestHeader = document.createElement('h3');
        incomingRequestHeader.textContent = '수신 요청';
        incomingRequestContainer.appendChild(incomingRequestHeader);

        const responseMessageContainer = document.createElement('div');
        const responseMessageHeader = document.createElement('h3');
        responseMessageHeader.textContent = '요청 응답';
        responseMessageContainer.appendChild(responseMessageHeader);

        let hasIncomingRequests = false;
        let hasResponseMessages = false;

        notifications.sort((a, b) => {
            if (a.accept_or_not === null && b.accept_or_not !== null) return -1;
            if (a.accept_or_not !== null && b.accept_or_not === null) return 1;
            return 0;
        });

        notifications.forEach(notification => {
            if (notification.accept_or_not === null && currentUser === notification.user) {

                const listItem = document.createElement('div');
                listItem.classList.add('notification-item');

                const messageText = document.createElement('p');
                const titleLink = document.createElement('a');
                titleLink.textContent = `'${notification.title}'`;
                messageText.appendChild(titleLink);
                messageText.innerHTML += ` 게시글에서 `;

                const senderLink = document.createElement('a');
                senderLink.textContent = `'${notification.sender}'`;
                messageText.appendChild(senderLink);
                messageText.innerHTML += '로부터 참가요청이 왔습니다.';

                listItem.appendChild(messageText);

                const actionButtons = document.createElement('div');
                actionButtons.classList.add('action-buttons');

                const acceptButton = document.createElement('button');
                acceptButton.textContent = '수락';
                acceptButton.addEventListener('click', async function () {
                    const result = await sendAcceptanceResult(notification.id, '수락');
                    if (result.success) {
                        notification.accept_or_not = true;
                        messageText.textContent = '요청을 수락하였습니다.';
                        acceptButton.style.display = 'none';
                        rejectButton.style.display = 'none';
                    }
                });
                actionButtons.appendChild(acceptButton);

                const rejectButton = document.createElement('button');
                rejectButton.textContent = '거절';
                rejectButton.addEventListener('click', async function () {
                    const result = await sendAcceptanceResult(notification.id, '거절');
                    if (result.success) {
                        notification.accept_or_not = false;
                        messageText.textContent = '요청을 거절하였습니다.';
                        acceptButton.style.display = 'none';
                        rejectButton.style.display = 'none';
                    }
                });
                actionButtons.appendChild(rejectButton);

                listItem.appendChild(actionButtons);

                titleLink.addEventListener('click', () => {
                    if (notification.titlelink) {
                        window.location.href = notification.titlelink;
                    }
                });

                senderlink.addEventListener('click', () => {
                    if (notification.senderlink) {
                        window.location.href = notification.senderlink;
                    }
                });

                if (!notification.read_or_not) {
                    listItem.style.backgroundColor = '#ccc';
                }

                incomingRequestContainer.appendChild(listItem);
                hasIncomingRequests = true;
            } else if (notification.accept_or_not === true && currentUser === notification.sender) {
                const listItem = document.createElement('div');
                listItem.classList.add('notification-item');

                const messageText = document.createElement('p');
                messageText.textContent = `'${notification.title}' 프로젝트의 참가요청이 수락되었습니다.`;
                listItem.appendChild(messageText);

                listItem.addEventListener('click', () => {
                    if (notification.titlelink) {
                        window.location.href = notification.titlelink;
                    }
                });

                if (!notification.read_or_not) {
                    listItem.style.backgroundColor = '#ccc';
                }

                responseMessageContainer.appendChild(listItem);
                hasResponseMessages = true;
            } else if (notification.accept_or_not === false && currentUser === notification.sender) {
                const listItem = document.createElement('div');
                listItem.classList.add('notification-item');

                const messageText = document.createElement('p');
                messageText.textContent = `'${notification.title}' 프로젝트의 참가요청이 거절되었습니다.`;
                listItem.appendChild(messageText);

                listItem.addEventListener('click', () => {
                    if (notification.titlelink) {
                        window.location.href = notification.titlelink;
                    }
                });

                if (!notification.read_or_not) {
                    listItem.style.backgroundColor = '#ccc';
                }

                responseMessageContainer.appendChild(listItem);
                hasResponseMessages = true;
            }
        });

        if (!hasIncomingRequests) {
            const emptyMessage = document.createElement('p');
            emptyMessage.textContent = '수신 요청이 없습니다.';
            incomingRequestContainer.appendChild(emptyMessage);
        }

        if (!hasResponseMessages) {
            const emptyMessage = document.createElement('p');
            emptyMessage.textContent = '요청 응답이 없습니다.';
            responseMessageContainer.appendChild(emptyMessage);
        }

        notificationMessage.appendChild(incomingRequestContainer);
        notificationMessage.appendChild(responseMessageContainer);

    }

    await markNotificationsAsRead();

    isNotificationVisible = !isNotificationVisible;
    await updateNotificationCount();
});
