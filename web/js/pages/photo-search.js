/**
 * 拍照搜题页面模块
 */

const photoSearchPage = {
    isProcessing: false,
    result: null,

    async render(container) {
        container.innerHTML = `
            <div class="animate-fade-in max-w-3xl mx-auto">
                <div class="card mb-6">
                    <div class="card-header">
                        <h3 class="text-lg font-semibold text-gray-900">拍照搜题</h3>
                    </div>
                    <div class="card-body">
                        <div class="text-center py-8">
                            <div id="upload-area" class="border-2 border-dashed border-gray-300 rounded-xl p-8 hover:border-primary-500 hover:bg-primary-50 transition-colors cursor-pointer">
                                <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0118.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                </svg>
                                <p class="text-lg font-medium text-gray-700 mb-2">点击或拖拽上传图片</p>
                                <p class="text-sm text-gray-500">支持 JPG、PNG 格式，最大 10MB</p>
                            </div>
                            <input type="file" id="file-input" accept="image/*" class="hidden">
                            
                            <div class="mt-6 flex items-center justify-center space-x-4">
                                <span class="text-gray-500">或者</span>
                                <button id="camera-btn" class="btn btn-primary">
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0118.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    </svg>
                                    拍照
                                </button>
                            </div>
                        </div>

                        <div id="preview-section" class="hidden">
                            <div class="mb-4">
                                <img id="preview-image" class="max-w-full max-h-96 mx-auto rounded-lg shadow-md" alt="预览图片">
                            </div>
                            
                            <div class="mb-4">
                                <label class="form-label">科目（可选）</label>
                                <select id="subject-select" class="input">
                                    <option value="">请选择科目</option>
                                    <option value="语文">语文</option>
                                    <option value="数学">数学</option>
                                    <option value="英语">英语</option>
                                    <option value="物理">物理</option>
                                    <option value="化学">化学</option>
                                    <option value="生物">生物</option>
                                    <option value="历史">历史</option>
                                    <option value="地理">地理</option>
                                    <option value="政治">政治</option>
                                </select>
                            </div>

                            <div class="flex space-x-4">
                                <button id="reset-btn" class="btn btn-secondary flex-1">
                                    重新上传
                                </button>
                                <button id="search-btn" class="btn btn-primary flex-1">
                                    <span class="btn-icon">🔍</span>
                                    开始搜题
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="result-section" class="hidden">
                    <div class="card">
                        <div class="card-header flex items-center justify-between">
                            <h3 class="text-lg font-semibold text-gray-900">搜题结果</h3>
                            <button id="new-search-btn" class="btn btn-primary btn-sm">
                                新搜索
                            </button>
                        </div>
                        <div class="card-body">
                            <div class="mb-6">
                                <h4 class="font-medium text-gray-900 mb-3">📝 识别结果</h4>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <p id="ocr-text" class="text-gray-700 whitespace-pre-wrap"></p>
                                </div>
                            </div>

                            <div class="divider"></div>

                            <div>
                                <h4 class="font-medium text-gray-900 mb-3">💡 AI解析</h4>
                                <div id="ai-analysis" class="bg-blue-50 rounded-lg p-4">
                                    <p class="text-gray-700 whitespace-pre-wrap"></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="loading-section" class="hidden">
                    <div class="card">
                        <div class="card-body text-center py-12">
                            <div class="loading-spinner mx-auto mb-4"></div>
                            <p class="text-lg font-medium text-gray-700">正在分析中...</p>
                            <p class="text-sm text-gray-500 mt-2">OCR识别 + AI分析，请稍候</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.setupEventListeners();
    },

    setupEventListeners() {
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        const cameraBtn = document.getElementById('camera-btn');
        const resetBtn = document.getElementById('reset-btn');
        const searchBtn = document.getElementById('search-btn');
        const newSearchBtn = document.getElementById('new-search-btn');

        if (uploadArea && fileInput) {
            uploadArea.addEventListener('click', () => fileInput.click());
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('border-primary-500', 'bg-primary-50');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('border-primary-500', 'bg-primary-50');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-primary-500', 'bg-primary-50');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileSelect(files[0]);
                }
            });
            
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFileSelect(e.target.files[0]);
                }
            });
        }

        if (cameraBtn) {
            cameraBtn.addEventListener('click', () => this.showCameraModal());
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetUpload());
        }

        if (searchBtn) {
            searchBtn.addEventListener('click', () => this.performSearch());
        }

        if (newSearchBtn) {
            newSearchBtn.addEventListener('click', () => this.resetUpload());
        }
    },

    handleFileSelect(file) {
        if (!file.type.startsWith('image/')) {
            showToast('请选择图片文件', 'error');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            showToast('图片大小不能超过10MB', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const previewImage = document.getElementById('preview-image');
            const uploadArea = document.getElementById('upload-area');
            const previewSection = document.getElementById('preview-section');

            if (previewImage) {
                previewImage.src = e.target.result;
            }
            if (uploadArea) {
                uploadArea.closest('.text-center').classList.add('hidden');
            }
            if (previewSection) {
                previewSection.classList.remove('hidden');
            }

            this.currentFile = file;
        };
        reader.readAsDataURL(file);
    },

    showCameraModal() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            showToast('您的浏览器不支持摄像头功能', 'error');
            return;
        }

        const content = `
            <div class="p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-xl font-semibold text-gray-900">拍照</h3>
                    <button onclick="hideModal()" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="video-container mb-4">
                    <video id="camera-preview" autoplay playsinline class="w-full rounded-lg"></video>
                    <canvas id="camera-canvas" style="display: none;"></canvas>
                </div>
                <div class="flex justify-center space-x-4">
                    <button onclick="photoSearchPage.capturePhoto()" class="btn btn-primary btn-lg">
                        <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <circle cx="12" cy="12" r="10" stroke-width="2"></circle>
                            <circle cx="12" cy="12" r="3" fill="currentColor"></circle>
                        </svg>
                        拍照
                    </button>
                </div>
            </div>
        `;

        showModal(content, {
            onClose: () => this.stopCamera()
        });

        this.startCamera();
    },

    async startCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });
            const preview = document.getElementById('camera-preview');
            if (preview) {
                preview.srcObject = stream;
            }
            this.cameraStream = stream;
        } catch (error) {
            console.error('Camera error:', error);
            showToast('无法访问摄像头', 'error');
            hideModal();
        }
    },

    stopCamera() {
        if (this.cameraStream) {
            this.cameraStream.getTracks().forEach(track => track.stop());
            this.cameraStream = null;
        }
    },

    capturePhoto() {
        const preview = document.getElementById('camera-preview');
        const canvas = document.getElementById('camera-canvas');

        if (!preview || !canvas) return;

        canvas.width = preview.videoWidth;
        canvas.height = preview.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(preview, 0, 0);

        canvas.toBlob((blob) => {
            const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
            this.handleFileSelect(file);
            hideModal();
            this.stopCamera();
        }, 'image/jpeg', 0.8);
    },

    resetUpload() {
        const uploadAreaContainer = document.querySelector('#upload-area').closest('.text-center');
        const previewSection = document.getElementById('preview-section');
        const resultSection = document.getElementById('result-section');
        const fileInput = document.getElementById('file-input');
        const subjectSelect = document.getElementById('subject-select');

        if (uploadAreaContainer) {
            uploadAreaContainer.classList.remove('hidden');
        }
        if (previewSection) {
            previewSection.classList.add('hidden');
        }
        if (resultSection) {
            resultSection.classList.add('hidden');
        }
        if (fileInput) {
            fileInput.value = '';
        }
        if (subjectSelect) {
            subjectSelect.value = '';
        }

        this.currentFile = null;
        this.result = null;
    },

    async performSearch() {
        if (!this.currentFile) {
            showToast('请先选择图片', 'error');
            return;
        }

        if (this.isProcessing) {
            return;
        }

        this.isProcessing = true;

        const previewSection = document.getElementById('preview-section');
        const loadingSection = document.getElementById('loading-section');
        const resultSection = document.getElementById('result-section');
        const subjectSelect = document.getElementById('subject-select');

        if (previewSection) {
            previewSection.classList.add('hidden');
        }
        if (loadingSection) {
            loadingSection.classList.remove('hidden');
        }
        if (resultSection) {
            resultSection.classList.add('hidden');
        }

        try {
            const subject = subjectSelect ? subjectSelect.value : null;
            const response = await ocrAPI.photoSearch(this.currentFile, subject);

            if (response.success && response.data) {
                this.result = response.data;
                this.showResult();
            } else {
                throw new Error(response.error || '搜题失败');
            }
        } catch (error) {
            console.error('Photo search error:', error);
            showToast(error.message || '搜题失败，请重试', 'error');
            this.resetUpload();
        } finally {
            this.isProcessing = false;
            if (loadingSection) {
                loadingSection.classList.add('hidden');
            }
        }
    },

    showResult() {
        const resultSection = document.getElementById('result-section');
        const ocrText = document.getElementById('ocr-text');
        const aiAnalysis = document.getElementById('ai-analysis');

        if (resultSection) {
            resultSection.classList.remove('hidden');
        }
        if (ocrText && this.result.ocr_text) {
            ocrText.textContent = this.result.ocr_text;
        }
        if (aiAnalysis && this.result.ai_analysis) {
            aiAnalysis.innerHTML = this.result.ai_analysis.replace(/\n/g, '<br>');
        }
    },
};

window.photoSearchPage = photoSearchPage;
