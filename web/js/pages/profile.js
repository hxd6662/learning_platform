/**
 * 个人中心页面模块
 */

const profilePage = {
    async render(container) {
        const user = authService.getUser();
        
        container.innerHTML = `
            <div class="animate-fade-in max-w-4xl mx-auto">
                <div class="card mb-6">
                    <div class="card-body">
                        <div class="flex items-center space-x-6">
                            <div class="avatar avatar-lg bg-gradient-to-br from-primary-400 to-primary-600">
                                ${user?.username?.charAt(0).toUpperCase() || 'U'}
                            </div>
                            <div class="flex-1">
                                <h2 class="text-2xl font-bold text-gray-900">${user?.username || '用户'}</h2>
                                <p class="text-gray-500">${user?.email || '未设置邮箱'}</p>
                                <p class="text-sm text-gray-400 mt-1">
                                    注册时间：${user?.created_at ? formatDate(user.created_at) : '未知'}
                                </p>
                            </div>
                            <button id="edit-profile-btn" class="btn btn-primary">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                                </svg>
                                编辑资料
                            </button>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="text-lg font-semibold text-gray-900">学习统计</h3>
                        </div>
                        <div class="card-body">
                            <div class="space-y-4">
                                <div class="flex items-center justify-between">
                                    <span class="text-gray-600">总学习时长</span>
                                    <span class="font-semibold text-gray-900" id="profile-total-time">0 分钟</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-gray-600">完成题目</span>
                                    <span class="font-semibold text-gray-900" id="profile-total-questions">0 道</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-gray-600">连续学习</span>
                                    <span class="font-semibold text-gray-900" id="profile-streak">0 天</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-gray-600">错题数量</span>
                                    <span class="font-semibold text-gray-900" id="profile-wrong">0 道</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header">
                            <h3 class="text-lg font-semibold text-gray-900">健康统计</h3>
                        </div>
                        <div class="card-body">
                            <div class="space-y-4">
                                <div class="flex items-center justify-between">
                                    <span class="text-gray-600">今日检测次数</span>
                                    <span class="font-semibold text-gray-900" id="profile-detection">0 次</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-gray-600">坐姿不良次数</span>
                                    <span class="font-semibold text-gray-900" id="profile-bad-posture">0 次</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-gray-600">良好坐姿率</span>
                                    <span class="font-semibold text-gray-900" id="profile-good-rate">0%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="text-lg font-semibold text-gray-900">账号设置</h3>
                    </div>
                    <div class="card-body">
                        <div class="space-y-4">
                            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                <div>
                                    <p class="font-medium text-gray-900">修改密码</p>
                                    <p class="text-sm text-gray-500">定期修改密码可以提高账号安全性</p>
                                </div>
                                <button class="btn btn-secondary" onclick="profilePage.showChangePasswordModal()">
                                    修改
                                </button>
                            </div>

                            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                <div>
                                    <p class="font-medium text-gray-900">通知设置</p>
                                    <p class="text-sm text-gray-500">管理系统的通知和提醒</p>
                                </div>
                                <button class="btn btn-secondary">
                                    设置
                                </button>
                            </div>

                            <div class="flex items-center justify-between p-4 bg-red-50 rounded-lg">
                                <div>
                                    <p class="font-medium text-red-900">退出登录</p>
                                    <p class="text-sm text-red-600">退出当前账号</p>
                                </div>
                                <button class="btn btn-danger" onclick="window.app.logout()">
                                    退出
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        await this.loadStats();
    },

    async loadStats() {
        try {
            const learningStats = await learningAPI.getStats();
            const healthStats = await healthAPI.getVideoStats();

            const totalTime = document.getElementById('profile-total-time');
            const totalQuestions = document.getElementById('profile-total-questions');
            const streak = document.getElementById('profile-streak');
            const wrong = document.getElementById('profile-wrong');
            const detection = document.getElementById('profile-detection');
            const badPosture = document.getElementById('profile-bad-posture');
            const goodRate = document.getElementById('profile-good-rate');

            if (totalTime) {
                totalTime.textContent = (learningStats?.data?.totalStudyMinutes || 0) + ' 分钟';
            }
            if (totalQuestions) {
                totalQuestions.textContent = (learningStats?.data?.totalQuestions || 0) + ' 道';
            }
            if (streak) {
                streak.textContent = (learningStats?.data?.consecutiveDays || 0) + ' 天';
            }
            if (wrong) {
                wrong.textContent = (learningStats?.wrong_questions || 0) + ' 道';
            }

            const healthData = healthStats?.data?.statistics || {};
            if (detection) {
                detection.textContent = (healthData.detection_count || 0) + ' 次';
            }
            if (badPosture) {
                badPosture.textContent = (healthData.bad_posture_count || 0) + ' 次';
            }
            if (goodRate) {
                goodRate.textContent = (healthData.good_posture_rate || 0) + '%';
            }
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    },

    showChangePasswordModal() {
        const content = `
            <div class="p-6">
                <h3 class="text-xl font-semibold text-gray-900 mb-6">修改密码</h3>
                <form id="change-password-form" class="space-y-4">
                    <div class="form-group">
                        <label class="form-label">当前密码</label>
                        <input type="password" name="current_password" class="input" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">新密码</label>
                        <input type="password" name="new_password" class="input" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">确认新密码</label>
                        <input type="password" name="confirm_password" class="input" required>
                    </div>
                    <div class="flex justify-end space-x-3 mt-6">
                        <button type="button" onclick="hideModal()" class="btn btn-secondary">取消</button>
                        <button type="submit" class="btn btn-primary">确认修改</button>
                    </div>
                </form>
            </div>
        `;

        showModal(content);

        document.getElementById('change-password-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const newPassword = formData.get('new_password');
            const confirmPassword = formData.get('confirm_password');

            if (newPassword !== confirmPassword) {
                showToast('两次输入的密码不一致', 'error');
                return;
            }

            showToast('密码修改功能暂未实现', 'warning');
            hideModal();
        });
    },
};

window.profilePage = profilePage;
