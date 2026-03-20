/**
 * 学习资源页面模块
 */

const resourcesPage = {
    resources: [],

    async render(container) {
        container.innerHTML = `
            <div class="animate-fade-in">
                <div class="mb-6">
                    <div class="relative">
                        <input type="text" id="search-input" class="input pl-10" placeholder="搜索学习资源...">
                        <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </div>
                </div>

                <div class="tabs mb-6">
                    <button class="tab active" data-type="all">全部</button>
                    <button class="tab" data-type="video">视频</button>
                    <button class="tab" data-type="article">文章</button>
                    <button class="tab" data-type="exercise">练习</button>
                </div>

                <div id="resources-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div class="col-span-full text-center py-12">
                        <div class="loading-spinner mx-auto mb-4"></div>
                        <p class="text-gray-500">加载中...</p>
                    </div>
                </div>
            </div>
        `;

        this.setupEventListeners();
        await this.loadResources();
    },

    setupEventListeners() {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', debounce((e) => {
                this.filterResources(e.target.value);
            }, 300));
        }

        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');
                this.filterByType(e.target.dataset.type);
            });
        });
    },

    async loadResources() {
        try {
            const response = await resourcesAPI.getResources();
            this.resources = response?.data || [];
            this.renderResources(this.resources);
        } catch (error) {
            console.error('Failed to load resources:', error);
            this.showError();
        }
    },

    renderResources(resources) {
        const container = document.getElementById('resources-grid');
        if (!container) return;

        if (resources.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                    </svg>
                    <p class="text-lg font-medium text-gray-900 mb-2">暂无学习资源</p>
                    <p class="text-sm text-gray-500">请稍后再来查看</p>
                </div>
            `;
            return;
        }

        container.innerHTML = resources.map(resource => {
            const typeIcons = {
                video: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>`,
                article: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>`,
                exercise: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                </svg>`,
            };

            const typeColors = {
                video: 'bg-red-100 text-red-600',
                article: 'bg-blue-100 text-blue-600',
                exercise: 'bg-green-100 text-green-600',
            };

            const difficultyColors = {
                easy: 'badge-success',
                medium: 'badge-warning',
                hard: 'badge-danger',
            };

            const difficultyLabels = {
                easy: '简单',
                medium: '中等',
                hard: '困难',
            };

            return `
                <div class="card hover:shadow-lg transition-shadow cursor-pointer" onclick="resourcesPage.viewResource(${resource.id})">
                    <div class="card-body">
                        <div class="flex items-start justify-between mb-3">
                            <div class="w-10 h-10 ${typeColors[resource.resource_type] || 'bg-gray-100 text-gray-600'} rounded-lg flex items-center justify-center">
                                ${typeIcons[resource.resource_type] || typeIcons.article}
                            </div>
                            ${resource.difficulty ? `<span class="badge ${difficultyColors[resource.difficulty] || 'badge-gray'}">${difficultyLabels[resource.difficulty] || resource.difficulty}</span>` : ''}
                        </div>
                        <h4 class="font-semibold text-gray-900 mb-2">${resource.title}</h4>
                        <p class="text-sm text-gray-500 mb-3 line-clamp-2">${resource.description || '暂无描述'}</p>
                        ${resource.subject ? `<span class="badge badge-gray">${resource.subject}</span>` : ''}
                    </div>
                </div>
            `;
        }).join('');
    },

    showError() {
        const container = document.getElementById('resources-grid');
        if (!container) return;

        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <svg class="w-16 h-16 mx-auto mb-4 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <p class="text-lg font-medium text-gray-900 mb-2">加载失败</p>
                <button onclick="resourcesPage.loadResources()" class="btn btn-primary btn-sm">
                    重新加载
                </button>
            </div>
        `;
    },

    filterResources(keyword) {
        if (!keyword) {
            this.renderResources(this.resources);
            return;
        }

        const filtered = this.resources.filter(r => 
            r.title?.toLowerCase().includes(keyword.toLowerCase()) ||
            r.description?.toLowerCase().includes(keyword.toLowerCase()) ||
            r.subject?.toLowerCase().includes(keyword.toLowerCase())
        );
        this.renderResources(filtered);
    },

    filterByType(type) {
        if (type === 'all') {
            this.renderResources(this.resources);
            return;
        }

        const filtered = this.resources.filter(r => r.resource_type === type);
        this.renderResources(filtered);
    },

    viewResource(id) {
        const resource = this.resources.find(r => r.id === id);
        if (!resource) return;

        const typeLabels = {
            video: '视频课程',
            article: '文章',
            exercise: '练习题',
        };

        const content = `
            <div class="p-6">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <span class="badge badge-primary mb-2">${typeLabels[resource.resource_type] || '资源'}</span>
                        <h3 class="text-xl font-semibold text-gray-900">${resource.title}</h3>
                    </div>
                    <button onclick="hideModal()" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-gray-500">描述</label>
                        <p class="mt-1 text-gray-900">${resource.description || '暂无描述'}</p>
                    </div>
                    
                    ${resource.subject ? `
                    <div>
                        <label class="text-sm font-medium text-gray-500">科目</label>
                        <p class="mt-1 text-gray-900">${resource.subject}</p>
                    </div>
                    ` : ''}
                    
                    ${resource.difficulty ? `
                    <div>
                        <label class="text-sm font-medium text-gray-500">难度</label>
                        <p class="mt-1 text-gray-900">${resource.difficulty}</p>
                    </div>
                    ` : ''}
                </div>
                
                <div class="flex justify-end space-x-3 mt-6">
                    <button onclick="hideModal()" class="btn btn-secondary">关闭</button>
                    <button class="btn btn-primary">开始学习</button>
                </div>
            </div>
        `;

        showModal(content);
    },
};

window.resourcesPage = resourcesPage;
