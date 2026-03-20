/**
 * 首页模块
 */

const homePage = {
    async render(container) {
        container.innerHTML = `
            <div class="animate-fade-in">
                <div class="mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">欢迎回来！</h2>
                    <p class="text-gray-600">今天是学习的好日子，让我们开始吧！</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div class="stat-card">
                        <div class="stat-icon bg-blue-100 text-blue-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="stat-study-time">0</div>
                        <div class="stat-label">今日学习时长</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-green-100 text-green-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="stat-questions">0</div>
                        <div class="stat-label">完成题目</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-purple-100 text-purple-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="stat-streak">0</div>
                        <div class="stat-label">连续学习天数</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-orange-100 text-orange-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="stat-wrong">0</div>
                        <div class="stat-label">错题数量</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                    <div class="lg:col-span-2">
                        <div class="card">
                            <div class="card-header flex items-center justify-between">
                                <h3 class="text-lg font-semibold text-gray-900">快捷功能</h3>
                            </div>
                            <div class="card-body">
                                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <button onclick="window.app.navigateTo('health')" class="p-4 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 hover:from-blue-100 hover:to-blue-200 transition-all group">
                                        <div class="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                                            </svg>
                                        </div>
                                        <p class="font-medium text-gray-900">坐姿检测</p>
                                        <p class="text-sm text-gray-500">实时监测</p>
                                    </button>

                                    <button onclick="window.app.navigateTo('questions')" class="p-4 rounded-xl bg-gradient-to-br from-green-50 to-green-100 hover:from-green-100 hover:to-green-200 transition-all group">
                                        <div class="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                                            </svg>
                                        </div>
                                        <p class="font-medium text-gray-900">错题本</p>
                                        <p class="text-sm text-gray-500">错题管理</p>
                                    </button>

                                    <button onclick="window.app.navigateTo('assistant')" class="p-4 rounded-xl bg-gradient-to-br from-purple-50 to-purple-100 hover:from-purple-100 hover:to-purple-200 transition-all group">
                                        <div class="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                                            </svg>
                                        </div>
                                        <p class="font-medium text-gray-900">AI助手</p>
                                        <p class="text-sm text-gray-500">智能答疑</p>
                                    </button>

                                    <button onclick="window.app.navigateTo('resources')" class="p-4 rounded-xl bg-gradient-to-br from-orange-50 to-orange-100 hover:from-orange-100 hover:to-orange-200 transition-all group">
                                        <div class="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                                            </svg>
                                        </div>
                                        <p class="font-medium text-gray-900">学习资源</p>
                                        <p class="text-sm text-gray-500">资源浏览</p>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header">
                            <h3 class="text-lg font-semibold text-gray-900">学习目标</h3>
                        </div>
                        <div class="card-body" id="goals-container">
                            <div class="text-center py-8 text-gray-500">
                                <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                                </svg>
                                <p>暂无学习目标</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header flex items-center justify-between">
                        <h3 class="text-lg font-semibold text-gray-900">最近学习记录</h3>
                        <button onclick="window.app.navigateTo('learning')" class="text-sm text-primary-600 hover:text-primary-700 font-medium">
                            查看全部
                        </button>
                    </div>
                    <div class="card-body" id="recent-records">
                        <div class="text-center py-8 text-gray-500">
                            <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                            </svg>
                            <p>暂无学习记录</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        await this.loadData();
    },

    async loadData() {
        try {
            const stats = await learningAPI.getStats();
            this.updateStats(stats);
        } catch (error) {
            console.error('Failed to load stats:', error);
        }

        try {
            const goalsResponse = await learningAPI.getGoals();
            this.updateGoals(goalsResponse);
        } catch (error) {
            console.error('Failed to load goals:', error);
        }
    },

    updateStats(stats) {
        const studyTimeEl = document.getElementById('stat-study-time');
        const questionsEl = document.getElementById('stat-questions');
        const streakEl = document.getElementById('stat-streak');
        const wrongEl = document.getElementById('stat-wrong');

        if (studyTimeEl) {
            studyTimeEl.textContent = stats?.study_time || 0;
        }
        if (questionsEl) {
            questionsEl.textContent = stats?.completed_questions || 0;
        }
        if (streakEl) {
            streakEl.textContent = stats?.streak_days || 0;
        }
        if (wrongEl) {
            wrongEl.textContent = stats?.wrong_questions || 0;
        }
    },

    updateGoals(response) {
        const container = document.getElementById('goals-container');
        if (!container) return;

        const goals = response?.data || [];

        if (goals.length === 0) {
            container.innerHTML = `
                <div class="text-center py-8 text-gray-500">
                    <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                    <p>暂无学习目标</p>
                </div>
            `;
            return;
        }

        container.innerHTML = goals.slice(0, 3).map(goal => `
            <div class="mb-4 last:mb-0">
                <div class="flex items-center justify-between mb-2">
                    <span class="font-medium text-gray-900 ${goal.is_completed ? 'line-through text-gray-400' : ''}">${goal.title}</span>
                    <span class="text-sm text-gray-500">${goal.progress || 0}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: ${goal.progress || 0}%"></div>
                </div>
            </div>
        `).join('');
    },
};

window.homePage = homePage;
