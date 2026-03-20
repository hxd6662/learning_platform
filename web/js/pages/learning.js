/**
 * 学习统计页面模块
 */

const learningPage = {
    async render(container) {
        container.innerHTML = `
            <div class="animate-fade-in">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div class="stat-card">
                        <div class="stat-icon bg-blue-100 text-blue-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="total-study-time">0</div>
                        <div class="stat-label">总学习时长（分钟）</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-green-100 text-green-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="total-questions">0</div>
                        <div class="stat-label">完成题目</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-purple-100 text-purple-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="consecutive-days">0</div>
                        <div class="stat-label">连续学习天数</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-orange-100 text-orange-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="accuracy-rate">0%</div>
                        <div class="stat-label">正确率</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    <div class="card">
                        <div class="card-header flex items-center justify-between">
                            <h3 class="text-lg font-semibold text-gray-900">学习目标</h3>
                            <button id="add-goal-btn" class="btn btn-primary btn-sm">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                                </svg>
                                添加目标
                            </button>
                        </div>
                        <div class="card-body" id="goals-list">
                            <div class="text-center py-8 text-gray-500">
                                <p>加载中...</p>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header">
                            <h3 class="text-lg font-semibold text-gray-900">学习记录</h3>
                        </div>
                        <div class="card-body" id="stats-list">
                            <div class="text-center py-8 text-gray-500">
                                <p>加载中...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.setupEventListeners();
        await this.loadData();
    },

    setupEventListeners() {
        const addGoalBtn = document.getElementById('add-goal-btn');
        if (addGoalBtn) {
            addGoalBtn.addEventListener('click', () => this.showAddGoalModal());
        }
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
        const totalStudyTime = document.getElementById('total-study-time');
        const totalQuestions = document.getElementById('total-questions');
        const consecutiveDays = document.getElementById('consecutive-days');
        const accuracyRate = document.getElementById('accuracy-rate');

        if (totalStudyTime) {
            totalStudyTime.textContent = stats?.data?.totalStudyMinutes || 0;
        }
        if (totalQuestions) {
            totalQuestions.textContent = stats?.data?.totalQuestions || 0;
        }
        if (consecutiveDays) {
            consecutiveDays.textContent = stats?.data?.consecutiveDays || 0;
        }
        if (accuracyRate) {
            accuracyRate.textContent = (stats?.data?.accuracy || 0) + '%';
        }
    },

    updateGoals(response) {
        const container = document.getElementById('goals-list');
        if (!container) return;

        const goals = response?.data || [];

        if (goals.length === 0) {
            container.innerHTML = `
                <div class="text-center py-8 text-gray-500">
                    <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                    <p>暂无学习目标</p>
                    <button onclick="learningPage.showAddGoalModal()" class="mt-3 text-primary-600 hover:text-primary-700 font-medium">
                        添加第一个目标
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = goals.map(goal => `
            <div class="flex items-center justify-between p-4 rounded-lg hover:bg-gray-50 transition-colors">
                <div class="flex-1">
                    <div class="flex items-center mb-2">
                        <span class="font-medium text-gray-900 ${goal.is_completed ? 'line-through text-gray-400' : ''}">${goal.title}</span>
                        ${goal.is_completed ? '<span class="ml-2 badge badge-success">已完成</span>' : ''}
                    </div>
                    ${goal.description ? `<p class="text-sm text-gray-500 mb-2">${goal.description}</p>` : ''}
                    <div class="flex items-center space-x-4 text-sm text-gray-500">
                        <span>进度: ${goal.progress || 0}%</span>
                        ${goal.target_date ? `<span>目标日期: ${goal.target_date}</span>` : ''}
                    </div>
                    <div class="progress mt-2">
                        <div class="progress-bar" style="width: ${goal.progress || 0}%"></div>
                    </div>
                </div>
                <div class="flex items-center space-x-2 ml-4">
                    <button onclick="learningPage.updateGoalProgress(${goal.id}, ${(goal.progress || 0) + 10})" class="btn btn-secondary btn-sm" ${goal.is_completed ? 'disabled' : ''}>
                        +10%
                    </button>
                    <button onclick="learningPage.deleteGoal(${goal.id})" class="btn btn-danger btn-sm">
                        删除
                    </button>
                </div>
            </div>
        `).join('');
    },

    showAddGoalModal() {
        const content = `
            <div class="p-6">
                <h3 class="text-xl font-semibold text-gray-900 mb-6">添加学习目标</h3>
                <form id="add-goal-form" class="space-y-4">
                    <div class="form-group">
                        <label class="form-label">目标标题 <span class="text-red-500">*</span></label>
                        <input type="text" name="title" class="input" placeholder="例如：完成数学第一章" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">目标描述</label>
                        <textarea name="description" class="input" rows="3" placeholder="详细描述你的学习目标"></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">目标日期</label>
                        <input type="date" name="target_date" class="input">
                    </div>
                    <div class="flex justify-end space-x-3 mt-6">
                        <button type="button" onclick="hideModal()" class="btn btn-secondary">取消</button>
                        <button type="submit" class="btn btn-primary">添加</button>
                    </div>
                </form>
            </div>
        `;

        showModal(content);

        document.getElementById('add-goal-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = {
                title: formData.get('title'),
                description: formData.get('description') || undefined,
                target_date: formData.get('target_date') || undefined,
            };

            try {
                await learningAPI.createGoal(data);
                hideModal();
                showToast('目标添加成功', 'success');
                await this.loadData();
            } catch (error) {
                showToast(error.message || '添加失败', 'error');
            }
        });
    },

    async updateGoalProgress(goalId, progress) {
        try {
            await learningAPI.updateGoal(goalId, { 
                progress: Math.min(progress, 100),
                is_completed: progress >= 100 
            });
            showToast('进度更新成功', 'success');
            await this.loadData();
        } catch (error) {
            showToast(error.message || '更新失败', 'error');
        }
    },

    async deleteGoal(goalId) {
        if (!confirm('确定要删除这个目标吗？')) return;

        try {
            await learningAPI.deleteGoal(goalId);
            showToast('目标已删除', 'success');
            await this.loadData();
        } catch (error) {
            showToast(error.message || '删除失败', 'error');
        }
    },
};

window.learningPage = learningPage;
