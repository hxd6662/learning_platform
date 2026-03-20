/**
 * 主应用模块
 * 应用初始化和页面路由管理
 */

class App {
    constructor() {
        this.currentPage = 'home';
        this.pages = {};
        this.init();
    }

    async init() {
        await this.loadPages();
        this.setupEventListeners();
        await this.checkAuth();
        this.hideLoading();
    }

    async loadPages() {
        this.pages = {
            home: window.homePage,
            learning: window.learningPage,
            health: window.healthPage,
            'photo-search': window.photoSearchPage,
            questions: window.questionsPage,
            assistant: window.assistantPage,
            resources: window.resourcesPage,
            profile: window.profilePage,
        };
    }

    setupEventListeners() {
        document.querySelectorAll('.nav-item[data-page]').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const page = item.dataset.page;
                this.navigateTo(page);
            });
        });

        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const sidebar = document.getElementById('sidebar');
        
        if (mobileMenuBtn && sidebar) {
            mobileMenuBtn.addEventListener('click', () => {
                sidebar.classList.toggle('-translate-x-full');
            });

            document.addEventListener('click', (e) => {
                if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                    sidebar.classList.add('-translate-x-full');
                }
            });
        }

        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                this.logout();
            });
        }
    }

    async checkAuth() {
        const isLoggedIn = await authService.checkAuth();
        if (isLoggedIn) {
            showMainApp();
        } else {
            renderLoginPage();
        }
    }

    navigateTo(pageName) {
        if (!this.pages[pageName]) {
            console.error(`Page "${pageName}" not found`);
            return;
        }

        this.currentPage = pageName;
        this.updateNavigation(pageName);
        this.updatePageTitle(pageName);
        
        const pageContent = document.getElementById('page-content');
        if (pageContent) {
            pageContent.innerHTML = '<div class="flex items-center justify-center py-12"><div class="loading-spinner"></div></div>';
            
            setTimeout(() => {
                this.pages[pageName].render(pageContent);
            }, 100);
        }

        const sidebar = document.getElementById('sidebar');
        if (sidebar && window.innerWidth < 1024) {
            sidebar.classList.add('-translate-x-full');
        }
    }

    updateNavigation(activePage) {
        document.querySelectorAll('.nav-item[data-page]').forEach(item => {
            if (item.dataset.page === activePage) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    updatePageTitle(pageName) {
        const titles = {
            home: '首页',
            learning: '学习统计',
            health: '坐姿检测',
            'photo-search': '拍照搜题',
            questions: '错题本',
            assistant: 'AI助手',
            resources: '学习资源',
            profile: '个人中心',
        };

        const pageTitle = document.getElementById('page-title');
        if (pageTitle) {
            pageTitle.textContent = titles[pageName] || '首页';
        }
    }

    logout() {
        authService.logout();
        renderLoginPage();
        showToast('已退出登录', 'success');
    }

    hideLoading() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 300);
        }
    }
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toast || !toastMessage || !toastIcon) return;

    const icons = {
        success: `<svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>`,
        error: `<svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>`,
        warning: `<svg class="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>`,
        info: `<svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>`,
    };

    toastIcon.innerHTML = icons[type] || icons.info;
    toastMessage.textContent = message;

    toast.classList.remove('translate-y-full', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');

    setTimeout(() => {
        toast.classList.add('translate-y-full', 'opacity-0');
        toast.classList.remove('translate-y-0', 'opacity-100');
    }, 3000);
}

function showModal(content, options = {}) {
    const modalContainer = document.getElementById('modal-container');
    const modalContent = document.getElementById('modal-content');
    const modalBackdrop = document.getElementById('modal-backdrop');

    if (!modalContainer || !modalContent) return;

    modalContent.innerHTML = content;
    modalContainer.classList.remove('hidden');

    if (modalBackdrop) {
        modalBackdrop.onclick = () => hideModal();
    }

    if (options.onClose) {
        const closeBtn = modalContent.querySelector('[data-modal-close]');
        if (closeBtn) {
            closeBtn.onclick = () => {
                hideModal();
                options.onClose();
            };
        }
    }
}

function hideModal() {
    const modalContainer = document.getElementById('modal-container');
    if (modalContainer) {
        modalContainer.classList.add('hidden');
    }
}

function formatTime(minutes) {
    if (!minutes || minutes === 0) return '0分钟';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
        return `${hours}小时${mins > 0 ? mins + '分钟' : ''}`;
    }
    return `${mins}分钟`;
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
    window.showToast = showToast;
    window.showModal = showModal;
    window.hideModal = hideModal;
    window.formatTime = formatTime;
    window.formatDate = formatDate;
    window.debounce = debounce;
});
