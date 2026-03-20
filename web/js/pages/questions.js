/**
 * 错题本页面模块
 */

const questionsPage = {
    questions: [],

    async render(container) {
        container.innerHTML = `
            <div class="animate-fade-in">
                <div class="card mb-6">
                    <div class="card-header flex items-center justify-between">
                        <h3 class="text-lg font-semibold text-gray-900">错题列表</h3>
                        <button id="add-question-btn" class="btn btn-primary btn-sm">
                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                            </svg>
                            添加错题
                        </button>
                    </div>
                    <div class="card-body" id="questions-list">
                        <div class="text-center py-12 text-gray-500">
                            <div class="loading-spinner mx-auto mb-4"></div>
                            <p>加载中...</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.setupEventListeners();
        await this.loadQuestions();
    },

    setupEventListeners() {
        const addBtn = document.getElementById('add-question-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.showAddModal());
        }
    },

    async loadQuestions() {
        try {
            const response = await questionsAPI.getWrongQuestions();
            this.questions = response?.data || [];
            this.renderQuestions();
        } catch (error) {
            console.error('Failed to load questions:', error);
            this.showError();
        }
    },

    renderQuestions() {
        const container = document.getElementById('questions-list');
        if (!container) return;

        if (this.questions.length === 0) {
            container.innerHTML = `
                <div class="text-center py-12 text-gray-500">
                    <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                    <p class="text-lg font-medium text-gray-900 mb-2">暂无错题</p>
                    <p class="text-sm">点击上方按钮添加你的第一道错题</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="overflow-x-auto">
                <table class="table">
                    <thead>
                        <tr>
                            <th>科目</th>
                            <th>题目内容</th>
                            <th>正确答案</th>
                            <th>错误答案</th>
                            <th>添加时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.questions.map(q => `
                            <tr>
                                <td>
                                    <span class="badge badge-primary">${q.subject || '未分类'}</span>
                                </td>
                                <td>
                                    <div class="max-w-xs truncate" title="${q.question_content}">
                                        ${q.question_content}
                                    </div>
                                </td>
                                <td>
                                    <div class="max-w-xs truncate text-green-600" title="${q.answer || '-'}">
                                        ${q.answer || '-'}
                                    </div>
                                </td>
                                <td>
                                    <div class="max-w-xs truncate text-red-600" title="${q.wrong_answer || '-'}">
                                        ${q.wrong_answer || '-'}
                                    </div>
                                </td>
                                <td class="text-gray-500 text-sm">
                                    ${formatDate(q.created_at)}
                                </td>
                                <td>
                                    <button onclick="questionsPage.viewQuestion(${q.id})" class="btn btn-secondary btn-sm mr-2">
                                        查看
                                    </button>
                                    <button onclick="questionsPage.deleteQuestion(${q.id})" class="btn btn-danger btn-sm">
                                        删除
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    },

    showError() {
        const container = document.getElementById('questions-list');
        if (!container) return;

        container.innerHTML = `
            <div class="text-center py-12 text-gray-500">
                <svg class="w-16 h-16 mx-auto mb-4 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <p class="text-lg font-medium text-gray-900 mb-2">加载失败</p>
                <button onclick="questionsPage.loadQuestions()" class="btn btn-primary btn-sm">
                    重新加载
                </button>
            </div>
        `;
    },

    showAddModal() {
        const content = `
            <div class="p-6">
                <h3 class="text-xl font-semibold text-gray-900 mb-6">添加错题</h3>
                <form id="add-question-form" class="space-y-4">
                    <div class="form-group">
                        <label class="form-label">科目 <span class="text-red-500">*</span></label>
                        <select name="subject" class="input" required>
                            <option value="">请选择科目</option>
                            <option value="数学">数学</option>
                            <option value="语文">语文</option>
                            <option value="英语">英语</option>
                            <option value="物理">物理</option>
                            <option value="化学">化学</option>
                            <option value="生物">生物</option>
                            <option value="历史">历史</option>
                            <option value="地理">地理</option>
                            <option value="政治">政治</option>
                            <option value="其他">其他</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">题目内容 <span class="text-red-500">*</span></label>
                        <textarea name="question_content" class="input" rows="4" placeholder="请输入题目内容" required></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">正确答案</label>
                        <textarea name="answer" class="input" rows="2" placeholder="请输入正确答案"></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">错误答案</label>
                        <textarea name="wrong_answer" class="input" rows="2" placeholder="请输入你的错误答案"></textarea>
                    </div>
                    <div class="flex justify-end space-x-3 mt-6">
                        <button type="button" onclick="hideModal()" class="btn btn-secondary">取消</button>
                        <button type="submit" class="btn btn-primary">添加</button>
                    </div>
                </form>
            </div>
        `;

        showModal(content);

        document.getElementById('add-question-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = {
                subject: formData.get('subject'),
                question_content: formData.get('question_content'),
                answer: formData.get('answer') || undefined,
                wrong_answer: formData.get('wrong_answer') || undefined,
            };

            try {
                await questionsAPI.addWrongQuestion(data);
                hideModal();
                showToast('错题添加成功', 'success');
                await this.loadQuestions();
            } catch (error) {
                showToast(error.message || '添加失败', 'error');
            }
        });
    },

    viewQuestion(id) {
        const question = this.questions.find(q => q.id === id);
        if (!question) return;

        const content = `
            <div class="p-6">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-xl font-semibold text-gray-900">错题详情</h3>
                    <span class="badge badge-primary">${question.subject || '未分类'}</span>
                </div>
                
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-gray-500">题目内容</label>
                        <p class="mt-1 text-gray-900 bg-gray-50 p-3 rounded-lg">${question.question_content}</p>
                    </div>
                    
                    <div>
                        <label class="text-sm font-medium text-gray-500">正确答案</label>
                        <p class="mt-1 text-green-700 bg-green-50 p-3 rounded-lg">${question.answer || '未填写'}</p>
                    </div>
                    
                    <div>
                        <label class="text-sm font-medium text-gray-500">错误答案</label>
                        <p class="mt-1 text-red-700 bg-red-50 p-3 rounded-lg">${question.wrong_answer || '未填写'}</p>
                    </div>
                    
                    <div class="text-sm text-gray-500">
                        添加时间：${formatDate(question.created_at)}
                    </div>
                </div>
                
                <div class="flex justify-end space-x-3 mt-6">
                    <button onclick="hideModal()" class="btn btn-secondary">关闭</button>
                    <button onclick="hideModal(); questionsPage.deleteQuestion(${question.id})" class="btn btn-danger">删除</button>
                </div>
            </div>
        `;

        showModal(content);
    },

    async deleteQuestion(id) {
        if (!confirm('确定要删除这道错题吗？')) return;

        try {
            await questionsAPI.deleteWrongQuestion(id);
            showToast('错题已删除', 'success');
            await this.loadQuestions();
        } catch (error) {
            showToast(error.message || '删除失败', 'error');
        }
    },
};

window.questionsPage = questionsPage;
