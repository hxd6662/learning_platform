/**
 * 坐姿检测页面模块
 */

const healthPage = {
    isMonitoring: false,
    videoStream: null,
    intervalId: null,
    currentPosture: null,

    async render(container) {
        container.innerHTML = `
            <div class="animate-fade-in">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    <div class="stat-card">
                        <div class="stat-icon bg-blue-100 text-blue-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="detection-count">0</div>
                        <div class="stat-label">今日检测次数</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-red-100 text-red-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="bad-posture-count">0</div>
                        <div class="stat-label">坐姿不良次数</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon bg-green-100 text-green-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="stat-value" id="good-posture-rate">0%</div>
                        <div class="stat-label">良好坐姿率</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2">
                        <div class="card">
                            <div class="card-header flex items-center justify-between">
                                <h3 class="text-lg font-semibold text-gray-900">实时监测</h3>
                                <div id="monitor-status" class="status-indicator good">
                                    未启动
                                </div>
                            </div>
                            <div class="card-body">
                                <div class="video-container mb-4">
                                    <video id="video-preview" autoplay playsinline class="w-full rounded-lg"></video>
                                    <canvas id="video-canvas" style="display: none;"></canvas>
                                    <div id="video-overlay" class="video-overlay">
                                        <svg class="w-16 h-16 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                                        </svg>
                                        <p class="text-gray-300">摄像头未启动</p>
                                    </div>
                                </div>

                                <div class="flex items-center justify-center space-x-4">
                                    <button id="start-monitor-btn" class="btn btn-primary btn-lg">
                                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                        </svg>
                                        开始检测
                                    </button>
                                    <button id="stop-monitor-btn" class="btn btn-danger btn-lg hidden">
                                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"></path>
                                        </svg>
                                        停止检测
                                    </button>
                                </div>

                                <div class="mt-4 p-4 bg-blue-50 rounded-lg">
                                    <div class="flex items-start">
                                        <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                        </svg>
                                        <p class="text-sm text-blue-700">检测过程中请保持头部在画面内，系统会自动检测坐姿和疲劳状态并给出提醒。</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-6">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="text-lg font-semibold text-gray-900">实时状态</h3>
                            </div>
                            <div class="card-body">
                                <div class="space-y-4">
                                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                        <span class="text-gray-600">坐姿状态</span>
                                        <span id="posture-status" class="status-indicator good">良好</span>
                                    </div>
                                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                        <span class="text-gray-600">疲劳状态</span>
                                        <span class="status-indicator good">正常</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="card">
                            <div class="card-header">
                                <h3 class="text-lg font-semibold text-gray-900">检测数据</h3>
                            </div>
                            <div class="card-body" id="posture-data">
                                <div class="text-center py-8 text-gray-500">
                                    <p>暂无检测数据</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.setupEventListeners();
        await this.loadStats();
    },

    setupEventListeners() {
        const startBtn = document.getElementById('start-monitor-btn');
        const stopBtn = document.getElementById('stop-monitor-btn');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startMonitoring());
        }
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopMonitoring());
        }
    },

    async loadStats() {
        try {
            const response = await healthAPI.getVideoStats();
            const stats = response?.data?.statistics || {};

            const detectionCount = document.getElementById('detection-count');
            const badPostureCount = document.getElementById('bad-posture-count');
            const goodPostureRate = document.getElementById('good-posture-rate');

            if (detectionCount) {
                detectionCount.textContent = stats.detection_count || 0;
            }
            if (badPostureCount) {
                badPostureCount.textContent = stats.bad_posture_count || 0;
            }
            if (goodPostureRate) {
                goodPostureRate.textContent = (stats.good_posture_rate || 0) + '%';
            }
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    },

    async startMonitoring() {
        try {
            await healthAPI.startVideoMonitor();

            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' },
                audio: false,
            });

            this.videoStream = stream;
            const video = document.getElementById('video-preview');
            if (video) {
                video.srcObject = stream;
            }

            this.isMonitoring = true;
            this.updateUI();

            this.intervalId = setInterval(() => this.captureFrame(), 2000);

            showToast('监测已启动', 'success');
        } catch (error) {
            console.error('Failed to start monitoring:', error);
            showToast('无法访问摄像头，请确保已授予权限', 'error');
        }
    },

    async stopMonitoring() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }

        if (this.videoStream) {
            this.videoStream.getTracks().forEach(track => track.stop());
            this.videoStream = null;
        }

        try {
            await healthAPI.stopVideoMonitor();
            await this.loadStats();
        } catch (error) {
            console.error('Failed to stop monitoring:', error);
        }

        this.isMonitoring = false;
        this.updateUI();
        showToast('监测已停止', 'info');
    },

    async captureFrame() {
        const video = document.getElementById('video-preview');
        const canvas = document.getElementById('video-canvas');

        if (!video || !canvas || !this.videoStream) return;

        try {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            if (!ctx) return;

            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.8));
            const file = new File([blob], 'frame.jpg', { type: 'image/jpeg' });

            const response = await healthAPI.processVideoFrame(file);
            
            if (response.success && response.data) {
                this.currentPosture = response.data;
                this.updatePostureData(response.data);
                await this.loadStats();
            }
        } catch (error) {
            console.error('Frame capture error:', error);
        }
    },

    updateUI() {
        const startBtn = document.getElementById('start-monitor-btn');
        const stopBtn = document.getElementById('stop-monitor-btn');
        const overlay = document.getElementById('video-overlay');
        const status = document.getElementById('monitor-status');

        if (startBtn) {
            startBtn.classList.toggle('hidden', this.isMonitoring);
        }
        if (stopBtn) {
            stopBtn.classList.toggle('hidden', !this.isMonitoring);
        }
        if (overlay) {
            overlay.classList.toggle('hidden', this.isMonitoring);
        }
        if (status) {
            status.textContent = this.isMonitoring ? '监测中' : '未启动';
            status.className = `status-indicator ${this.isMonitoring ? 'good' : ''}`;
        }
    },

    updatePostureData(data) {
        const postureStatus = document.getElementById('posture-status');
        const postureData = document.getElementById('posture-data');

        if (postureStatus) {
            const statusMap = {
                good: { text: '良好', class: 'good' },
                warning: { text: '需注意', class: 'warning' },
                danger: { text: '需纠正', class: 'danger' },
            };
            const status = statusMap[data.status] || statusMap.good;
            postureStatus.textContent = status.text;
            postureStatus.className = `status-indicator ${status.class}`;
        }

        if (postureData) {
            postureData.innerHTML = `
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600">头部角度</span>
                        <span class="font-medium text-gray-900">${data.head_angle || 0}°</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600">肩部平衡</span>
                        <span class="font-medium text-gray-900">${data.shoulder_balance || '-'}</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600">背部弯曲</span>
                        <span class="font-medium text-gray-900">${data.back_curve || '-'}</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600">眼睛距离</span>
                        <span class="font-medium text-gray-900">${data.eye_distance || 0} cm</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600">综合评分</span>
                        <span class="font-medium text-gray-900">${data.score || 0}分</span>
                    </div>
                </div>
            `;
        }
    },
};

window.healthPage = healthPage;
