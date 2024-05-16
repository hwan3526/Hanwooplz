const chatLog = document.querySelector('#chat-log');
const chatList = document.querySelector('#chat-list-box');

function generateMessageId() {
    return uuid.v4();
}

function redirectToChat(chatRoomId, receiverId) {
    const chatBoxes = document.querySelectorAll('.chat-box');
    chatBoxes.forEach(chatBox => {
        chatBox.classList.remove('selected-chat');
    });

    const selectedChat = document.querySelector(`[data-chat-room-id="${chatRoomId}"]`);
    if (selectedChat) {
        selectedChat.classList.add('selected-chat');
    }

    window.location.href = `/chat/${chatRoomId}/${receiverId}`;
}

function isScrolledToBottom() {
    const scrollThreshold = 54;
    return chatLog.scrollHeight - chatLog.scrollTop <= chatLog.clientHeight + scrollThreshold;
}

const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${room_number}/`);

document.addEventListener('DOMContentLoaded', function () {
    const messageInputDom = document.querySelector('#chat-message-input');
    const chatMessageSubmitBtn = document.querySelector('#chat-message-submit');

    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();

        const amOrPm = hours >= 12 ? 'PM' : 'AM';
        const formattedHours = hours % 12 || 12;
        const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;

        const currentTime = `오늘 ${amOrPm} ${formattedHours}:${formattedMinutes}`;

        return currentTime;
    }

    const currentTime = getCurrentTime();

    function scrollToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // 안 읽은 메시지 스크롤 관리 함수
    function handleUnreadMessages() {
        const unreadMessages = document.querySelectorAll('.unread');

        if (unreadMessages.length > 0) {
            // 안 읽은 메시지가 있을 때
            if (unreadMessages.length <= 3) {
                // 안 읽은 메시지가 3개 이하일 때
                scrollToBottom();
            } else {
                // 안 읽은 메시지가 3개보다 많을 때
                // 가장 오래된 안 읽은 메시지가 화면의 최상단에 오도록 스크롤
                unreadMessages[0].scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } else {
            // 모든 메시지가 읽혔을 때
            scrollToBottom();
        }
    }

    ws.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.type === 'chat_message') {

            const messageContainer = document.createElement('div');

            const currentUser = data.username;
            const messageId = data.message_id;

            if (currentUser === username) {
                messageContainer.className = 'message-box from-me';
                messageContainer.innerHTML = `
            <p class="s-text unread-message"></p>
            <p class="s-text">${data.created_at}</p>
            <div class="message-text">${data.message}</div>
          `;
            } else {
                messageContainer.className = 'message-box from-you';
                messageContainer.innerHTML = `
            <div class="message-text">${data.message}</div>
            <p class="s-text">${data.created_at}</p>
          `;

                const messageText = data.message.length > 10 ? data.message.slice(0, 10) + '...' : data.message;

                if (!isScrolledToBottom()) {
                    showNewMessagePopup(messageText);
                }
            }
            chatLog.appendChild(messageContainer);

            if (currentUser == username) {
                scrollToBottom();
            }

            if (isScrolledToBottom()) {
                scrollToBottom();
            }

            handleUnreadMessages();

            scrollToBottom();

        };

        if (data.type === 'chat_message_read') {
            let unreadMessages = document.querySelectorAll('.unread-message');
            unreadMessages.forEach(message => {
                message.textContent = '';
            });
        }


    }

    if (room_number > 0 || room_number == -1) {
        chatMessageSubmitBtn.addEventListener('click', function () {
            const message = messageInputDom.value;

            if (message.trim() !== '') { // 빈 메시지는 추가하지 않음

                let uuid = generateMessageId();
                if (room_number > 0) {
                    ws.send(JSON.stringify({
                        'type': 'chat_message',
                        'message': message,
                        'username': username,
                        'receiver': receiver_username,
                        'room_number': room_number,
                        'created_at': currentTime,
                        'chat_uuid': uuid
                    }));
                } else if (room_number == -1) {
                    const messageContainer = document.createElement('div');
                    messageContainer.className = 'message-box from-me';
                    messageContainer.innerHTML = `
              <p class="s-text">${currentTime}</p>
              <div class="message-text">${message}</div>
            `;
                    chatLog.appendChild(messageContainer);



                    chatLog.appendChild(second);
                    scrollToBottom();
                }

                messageInputDom.value = '';

            };
        });

        document.querySelector('#chat-message-input').addEventListener('keydown', function (e) {
            if (e.keyCode === 13) {  // enter, return
                e.preventDefault(); // 폼 제출을 막음
                document.querySelector('#chat-message-submit').click();
            }
        });
    }
});

window.addEventListener('focus', function () {
    if (isScrolledToBottom(chatLog)) {

        if (room_number > 0) {
            ws.send(JSON.stringify({
                'type': 'chat_message_read',
                'receiver': request_user_username,
                'room_number': room_number,
                'chat_uuid': generateMessageId(),
                'is_read': true
            }));
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        const currentUrl = window.location.href;
        const match = currentUrl.match(/chat\/(\d+)/);
        let chatRoomId = 0;

        if (match) {
            chatRoomId = match[1];
        }

        const selectedChat = document.querySelector(`[data-chat-room-id="${chatRoomId}"]`);
        if (selectedChat) {
            selectedChat.classList.add('selected-chat');
        }

        if (firstUnreadIndex > 0) {
            const unreadChat = chatLog.querySelectorAll('.unread')[0];
            if (unreadChat) {
                unreadChat.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        } else {
            if (chatLog) {
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        }
    });

    const chatListItems = document.querySelectorAll('.chat-box');

    chatListItems.forEach(item => {
        const textElement = item.querySelector('.chat-thumb-text');
        const maxTextLength = 15;

        if (textElement.textContent.length > maxTextLength) {
            const truncatedText = textElement.textContent.slice(0, maxTextLength) + '...';
            textElement.textContent = truncatedText;
        }
    });

});

document.addEventListener('DOMContentLoaded', function () {
    const messageInput = document.querySelector('#chat-message-input');
    const chatMessageSubmitBtn = document.querySelector('#chat-message-submit');

    messageInput.addEventListener('input', function () {
        if (messageInput.value.trim() !== '') {
            chatMessageSubmitBtn.style.backgroundColor = '#000';
            chatMessageSubmitBtn.style.color = '#fff';
        } else {
            chatMessageSubmitBtn.style.backgroundColor = '#E1E1E1';
            chatMessageSubmitBtn.style.color = '#000';
        }
    });
});

const ws2 = new WebSocket('ws://127.0.0.1:8000/ws/chat_list/');

ws2.onmessage = function (e) {
    const chatListData = JSON.parse(e.data);

    // 채팅 목록 업데이트 로직
    chatList.innerHTML = '';  // 기존 목록 초기화

    chatListData.forEach(msg => {
        const chatBox = document.createElement('div');
        chatBox.className = 'chat-box between';
        chatBox.dataset.chatRoomId = msg.chat_room_id;

        // 채팅방 목록 항목 구성
        const flexBox = document.createElement('div');
        flexBox.className = 'flex-box';
        const receiverSpan = document.createElement('span');
        receiverSpan.className = 'bold';
        receiverSpan.textContent = msg.receiver;
        const dateSpan = document.createElement('span');
        dateSpan.className = 's-text';
        dateSpan.textContent = msg.created_at;

        flexBox.appendChild(receiverSpan);
        flexBox.appendChild(dateSpan);

        chatBox.appendChild(flexBox);

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        const chatThumbText = document.createElement('p');
        chatThumbText.className = 'chat-thumb-text';
        chatThumbText.textContent = msg.message;

        messageContent.appendChild(chatThumbText);

        chatBox.appendChild(messageContent);

        if (msg.unread_message_count > 0) {
            const unreadMessageCount = document.createElement('span');
            unreadMessageCount.className = 'unread_message_count';
            unreadMessageCount.textContent = msg.unread_message_count;
            chatBox.appendChild(unreadMessageCount);
        }

        chatList.appendChild(chatBox);
    });
};
