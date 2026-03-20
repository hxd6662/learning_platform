/**
 * AI助手页面模块
 */

const assistantPage = {
    messages: [],

    async render(container) {
        container.innerHTML = `
            <div class="animate-fade-in h-full flex flex-col">
                <div class="card flex-1 flex flex-col">
                    <div class="card-header flex items-center justify-between">
                        <h3 class="text-lg font-semibold text-gray-900">AI学习助手</h3>
                        <button id="clear-chat-btn" class="btn btn-secondary btn-sm">
                            清空对话
                        </button>
                    </div>
                    
                    <div id="chat-messages" class="flex-1 overflow-y-auto p-4 space-y-4" style="max-height: 500px;">
                        <div class="chat-message assistant">
                            <div class="avatar mr-3">AI</div>
                            <div class="chat-bubble">
                                你好！我是AI学习助手，可以帮你解答学习中的问题。请问有什么可以帮助你的吗？
                            </div>
                        </div>
                    </div>
                    
                    <div class="card-footer">
                        <form id="chat-form" class="flex items-center space-x-3">
                            <input type="text" id="chat-input" class="input flex-1" placeholder="输入你的问题..." autocomplete="off">
                            <button type="submit" class="btn btn-primary">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                                </svg>
                            </button>
                        </form>
                    </div>
                </div>

                <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="card p-4 cursor-pointer hover:shadow-lg transition-shadow" onclick="assistantPage.quickAsk('帮我解释一下勾股定理')">
                        <div class="flex items-center space-x-3">
                            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="font-medium text-gray-900">数学问题</p>
                                <p class="text-sm text-gray-500">勾股定理讲解</p>
                            </div>
                        </div>
                    </div>

                    <div class="card p-4 cursor-pointer hover:shadow-lg transition-shadow" onclick="assistantPage.quickAsk('如何提高英语阅读能力？')">
                        <div class="flex items-center space-x-3">
                            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="font-medium text-gray-900">英语学习</p>
                                <p class="text-sm text-gray-500">阅读能力提升</p>
                            </div>
                        </div>
                    </div>

                    <div class="card p-4 cursor-pointer hover:shadow-lg transition-shadow" onclick="assistantPage.quickAsk('给我推荐一些高效的学习方法')">
                        <div class="flex items-center space-x-3">
                            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="font-medium text-gray-900">学习方法</p>
                                <p class="text-sm text-gray-500">高效学习技巧</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.setupEventListeners();
    },

    setupEventListeners() {
        const form = document.getElementById('chat-form');
        const clearBtn = document.getElementById('clear-chat-btn');

        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const input = document.getElementById('chat-input');
                const message = input.value.trim();
                if (message) {
                    this.sendMessage(message);
                    input.value = '';
                }
            });
        }

        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clearChat();
            });
        }
    },

    async sendMessage(message) {
        this.addMessage('user', message);

        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'chat-message assistant';
            loadingDiv.id = 'loading-message';
            loadingDiv.innerHTML = `
                <div class="avatar mr-3">AI</div>
                <div class="chat-bubble">
                    <div class="flex items-center space-x-2">
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
                    </div>
                </div>
            `;
            messagesContainer.appendChild(loadingDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        try {
            const response = await assistantAPI.chat(message);
            const aiMessage = response?.data?.message || '抱歉，我暂时无法回答这个问题。';
            
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }

            this.addMessage('assistant', aiMessage);
        } catch (error) {
            console.error('Chat error:', error);
            
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }

            this.addMessage('assistant', '抱歉，发生了错误，请稍后再试。');
        }
    },

    addMessage(role, content) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role}`;
        
        if (role === 'user') {
            messageDiv.innerHTML = `
                <div class="chat-bubble">${this.escapeHtml(content)}</div>
                <div class="avatar ml-3">${this.getUserInitial()}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="avatar mr-3">AI</div>
                <div class="chat-bubble">${this.escapeHtml(content)}</div>
            `;
        }

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        this.messages.push({ role, content });
    },

    quickAsk(question) {
        const input = document.getElementById('chat-input');
        if (input) {
            input.value = question;
            input.focus();
        }
    },

    clearChat() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        this.messages = [];
        messagesContainer.innerHTML = `
            <div class="chat-message assistant">
                <div class="avatar mr-3">AI</div>
                <div class="chat-bubble">
                    对话已清空。请问有什么可以帮助你的吗？
                </div>
            </div>
        `;
    },

    getUserInitial() {
        const user = authService.getUser();
        return user?.username?.charAt(0).toUpperCase() || 'U';
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
};

window.assistantPage = assistantPage;
