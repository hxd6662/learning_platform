/**
 * 认证模块
 * 处理用户登录、注册和会话管理
 */

class AuthService {
    constructor() {
        this.user = null;
        this.isAuthenticated = false;
    }

    async checkAuth() {
        const token = localStorage.getItem('authToken');
        if (!token) {
            return false;
        }

        try {
            const user = await authAPI.getProfile();
            this.user = user;
            this.isAuthenticated = true;
            return true;
        } catch (error) {
            console.error('Auth check failed:', error);
            this.logout();
            return false;
        }
    }

    async login(username, password) {
        try {
            const response = await authAPI.login(username, password);
            this.user = await authAPI.getProfile();
            this.isAuthenticated = true;
            return { success: true, user: this.user };
        } catch (error) {
            console.error('Login failed:', error);
            return { success: false, error: error.message };
        }
    }

    async register(username, email, password) {
        try {
            const response = await authAPI.register({
                username,
                email: email || undefined,
                password,
            });
            return { success: true };
        } catch (error) {
            console.error('Register failed:', error);
            return { success: false, error: error.message };
        }
    }

    logout() {
        localStorage.removeItem('authToken');
        this.user = null;
        this.isAuthenticated = false;
        api.setToken(null);
    }

    getUser() {
        return this.user;
    }

    isLoggedIn() {
        return this.isAuthenticated;
    }
}

const authService = new AuthService();

function renderLoginPage() {
    const authContainer = document.getElementById('auth-container');
    authContainer.innerHTML = `
        <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4">
            <div class="max-w-md w-full animate-fade-in">
                <div class="bg-white rounded-2xl shadow-xl p-8">
                    <div class="text-center mb-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                            </svg>
                        </div>
                        <h1 class="text-2xl font-bold text-gray-900">欢迎回来</h1>
                        <p class="text-gray-500 mt-2">登录您的智能学习平台账号</p>
                    </div>

                    <form id="login-form" class="space-y-5">
                        <div class="form-group">
                            <label class="form-label">用户名</label>
                            <input type="text" name="username" class="input" placeholder="请输入用户名" required>
                        </div>

                        <div class="form-group">
                            <label class="form-label">密码</label>
                            <input type="password" name="password" class="input" placeholder="请输入密码" required>
                        </div>

                        <button type="submit" class="btn btn-primary btn-lg w-full">
                            登录
                        </button>
                    </form>

                    <div class="mt-6 text-center">
                        <p class="text-gray-600">
                            还没有账号？
                            <button id="go-to-register" class="text-primary-600 hover:text-primary-700 font-medium">
                                立即注册
                            </button>
                        </p>
                    </div>
                </div>

                <div class="mt-8 text-center text-sm text-gray-500">
                    <p>© 2026 智能学习平台. All rights reserved.</p>
                </div>
            </div>
        </div>
    `;

    authContainer.classList.remove('hidden');
    document.getElementById('main-container').classList.add('hidden');

    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const username = formData.get('username');
        const password = formData.get('password');

        const btn = e.target.querySelector('button[type="submit"]');
        btn.disabled = true;
        btn.textContent = '登录中...';

        const result = await authService.login(username, password);
        
        if (result.success) {
            showToast('登录成功', 'success');
            setTimeout(() => {
                showMainApp();
            }, 500);
        } else {
            showToast(result.error || '登录失败', 'error');
            btn.disabled = false;
            btn.textContent = '登录';
        }
    });

    document.getElementById('go-to-register').addEventListener('click', () => {
        renderRegisterPage();
    });
}

function renderRegisterPage() {
    const authContainer = document.getElementById('auth-container');
    authContainer.innerHTML = `
        <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4">
            <div class="max-w-md w-full animate-fade-in">
                <div class="bg-white rounded-2xl shadow-xl p-8">
                    <div class="text-center mb-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                            </svg>
                        </div>
                        <h1 class="text-2xl font-bold text-gray-900">创建账号</h1>
                        <p class="text-gray-500 mt-2">开启您的智能学习之旅</p>
                    </div>

                    <form id="register-form" class="space-y-5">
                        <div class="form-group">
                            <label class="form-label">用户名 <span class="text-red-500">*</span></label>
                            <input type="text" name="username" class="input" placeholder="请输入用户名" required>
                        </div>

                        <div class="form-group">
                            <label class="form-label">邮箱</label>
                            <input type="email" name="email" class="input" placeholder="请输入邮箱（可选）">
                        </div>

                        <div class="form-group">
                            <label class="form-label">密码 <span class="text-red-500">*</span></label>
                            <input type="password" name="password" class="input" placeholder="请输入密码" required>
                        </div>

                        <div class="form-group">
                            <label class="form-label">确认密码 <span class="text-red-500">*</span></label>
                            <input type="password" name="confirmPassword" class="input" placeholder="请再次输入密码" required>
                        </div>

                        <button type="submit" class="btn btn-primary btn-lg w-full">
                            注册
                        </button>
                    </form>

                    <div class="mt-6 text-center">
                        <p class="text-gray-600">
                            已有账号？
                            <button id="go-to-login" class="text-primary-600 hover:text-primary-700 font-medium">
                                立即登录
                            </button>
                        </p>
                    </div>
                </div>

                <div class="mt-8 text-center text-sm text-gray-500">
                    <p>© 2026 智能学习平台. All rights reserved.</p>
                </div>
            </div>
        </div>
    `;

    authContainer.classList.remove('hidden');
    document.getElementById('main-container').classList.add('hidden');

    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const username = formData.get('username');
        const email = formData.get('email');
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');

        if (password !== confirmPassword) {
            showToast('两次输入的密码不一致', 'error');
            return;
        }

        const btn = e.target.querySelector('button[type="submit"]');
        btn.disabled = true;
        btn.textContent = '注册中...';

        const result = await authService.register(username, email, password);
        
        if (result.success) {
            showToast('注册成功，请登录', 'success');
            setTimeout(() => {
                renderLoginPage();
            }, 1000);
        } else {
            showToast(result.error || '注册失败', 'error');
            btn.disabled = false;
            btn.textContent = '注册';
        }
    });

    document.getElementById('go-to-login').addEventListener('click', () => {
        renderLoginPage();
    });
}

function showMainApp() {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('main-container').classList.remove('hidden');
    
    const user = authService.getUser();
    if (user) {
        const userInitial = user.username ? user.username.charAt(0).toUpperCase() : 'U';
        const userAvatar = document.querySelector('#user-info .avatar');
        if (userAvatar) {
            userAvatar.textContent = userInitial;
        }
        const userName = document.querySelector('#user-info span');
        if (userName) {
            userName.textContent = user.username || '用户';
        }
    }
    
    if (window.app && window.app.navigateTo) {
        window.app.navigateTo('home');
    }
}

window.authService = authService;
window.renderLoginPage = renderLoginPage;
window.renderRegisterPage = renderRegisterPage;
window.showMainApp = showMainApp;
