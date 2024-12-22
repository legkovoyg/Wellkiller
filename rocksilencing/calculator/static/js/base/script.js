document.addEventListener("DOMContentLoaded", function() {
    // Добавьте этот код в самое начало функции
    if (document.querySelector('.chat-widget')) {
        const chatWidget = document.querySelector('.chat-widget');
        chatWidget.style.zIndex = '9999';
    }
    // Сайдбар функциональность
    const body = document.querySelector("body");
    const sidebar = body.querySelector(".sidebar");
    const toggle = body.querySelector(".toggle");
    
    // Чат функциональность
    const chatButton = document.getElementById('chatButton');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');
    const closeChatButton = document.getElementById('closeChatButton');
    const chatDialog = document.getElementById('chatDialog');

    // Инициализация и обработчики сайдбара
    if (toggle) {
        toggle.addEventListener("click", () => {
            sidebar.classList.toggle("close");
        });
    }

    // Открытие/закрытие чата
    if (chatButton && chatDialog) {
        chatButton.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            chatDialog.classList.add('open');
            if (messageInput) messageInput.focus();
        });
    }

    // Закрытие чата
    if (closeChatButton && chatDialog) {
        closeChatButton.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            chatDialog.classList.remove('open');
        });
    }

    // Функционал чата
    if (messageInput && sendButton && chatMessages) {
        // Функция для получения CSRF токена
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // Функция для добавления сообщения в чат
        function addMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', type);
            messageDiv.textContent = text;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Функция отправки сообщения
        async function sendMessage(e) {
            if (e) e.preventDefault();
            
            const message = messageInput.value.trim();
            if (!message) return;

            // Добавляем сообщение пользователя в чат
            addMessage(message, 'user');
            
            // Очищаем поле ввода
            messageInput.value = '';
            messageInput.style.height = 'auto';
            
            try {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const response = await fetch('api/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    credentials: 'include',
                    body: JSON.stringify({ message })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Received response:', data);
                
                if (data.status === 'success') {
                    addMessage(data.response, 'assistant');
                } else {
                    throw new Error(data.message || 'Unknown error occurred');
                }
            } catch (error) {
                console.error('Error:', error);
                addMessage('Произошла ошибка при отправке сообщения', 'assistant');
            }
        }

        // Обработчики событий для отправки сообщений
        sendButton.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            sendMessage();
        });
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                e.stopPropagation();
                sendMessage();
            }
        });

        // Автоматическая высота текстового поля
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        });
    }

    // Мобильная версия
    function mobile() {
        let newToggle = document.querySelector('.toggle-sidebar-img');
        const mainHeaderRight = document.querySelector('.main-Header__rightContent');
        const logInButton = document.querySelector('.rightContent-fourth');
        const closeSidebar = document.querySelector('.close-sidebar');

        if (document.documentElement.clientWidth <= 500) {
            if (logInButton) logInButton.style.display = 'none';
            if (!newToggle && mainHeaderRight) {
                newToggle = document.createElement('img');
                newToggle.classList.add('toggle-sidebar-img');
                mainHeaderRight.append(newToggle);
                newToggle.src = '/static/images/base/Frame-15003.svg';
                newToggle.addEventListener("click", () => {
                    sidebar.classList.remove("close");
                });
                if (closeSidebar) {
                    closeSidebar.addEventListener('click', () => {
                        sidebar.classList.add("close");
                    });
                }
            }
        } else {
            if (newToggle) newToggle.remove();
            if (logInButton) logInButton.style.display = 'flex';
        }
    }

    // Инициализация мобильной версии
    window.addEventListener('resize', mobile);
    window.addEventListener('load', mobile);
});