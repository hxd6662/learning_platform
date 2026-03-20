/**
 * API 服务模块
 * 处理所有与后端的HTTP通信
 */

const API_BASE_URL = 'http://localhost:8001';

class APIService {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.token = localStorage.getItem('authToken');
    }

    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('authToken', token);
        } else {
            localStorage.removeItem('authToken');
        }
    }

    getToken() {
        return this.token || localStorage.getItem('authToken');
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }

    async uploadFile(endpoint, file) {
        const formData = new FormData();
        formData.append('file', file);

        const headers = {};
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers,
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Upload Error: ${response.status}`);
        }

        return await response.json();
    }

    async postFormData(endpoint, formData) {
        const headers = {};
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers,
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error: ${response.status}`);
        }

        return await response.json();
    }
}

const api = new APIService();

const authAPI = {
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await api.postFormData('/api/v1/auth/login', formData);
        if (response.access_token) {
            api.setToken(response.access_token);
        }
        return response;
    },

    async register(data) {
        return api.post('/api/v1/auth/register', data);
    },

    async getProfile() {
        return api.get('/api/v1/auth/profile');
    },
};

const learningAPI = {
    async getStats() {
        return api.get('/api/v1/learning/stats');
    },

    async getUserStats(userId) {
        return api.get(`/api/v1/learning/stats/${userId}`);
    },

    async createStat(data) {
        return api.post('/api/v1/learning/stats', data);
    },

    async getGoals() {
        return api.get('/api/v1/learning/goals');
    },

    async createGoal(data) {
        return api.post('/api/v1/learning/goals', data);
    },

    async updateGoal(goalId, data) {
        return api.put(`/api/v1/learning/goals/${goalId}`, data);
    },

    async deleteGoal(goalId) {
        return api.delete(`/api/v1/learning/goals/${goalId}`);
    },
};

const healthAPI = {
    async getStats() {
        return api.get('/api/v1/health/stats');
    },

    async getRecords(params = {}) {
        const query = new URLSearchParams(params).toString();
        return api.get(`/api/v1/health/records?${query}`);
    },

    async createRecord(data) {
        return api.post('/api/v1/health/records', data);
    },

    async getReport(days = 7) {
        return api.get(`/api/v1/health/report?days=${days}`);
    },

    async startMonitor() {
        return api.post('/api/v1/health/monitor/start', {});
    },

    async stopMonitor() {
        return api.post('/api/v1/health/monitor/stop', {});
    },

    async getRealtime() {
        return api.get('/api/v1/health/realtime');
    },

    async getRealtimeDetect() {
        return api.get('/api/v1/health/realtime/detect');
    },

    async detectPosture(images) {
        return api.post('/api/v1/health/posture/detect', { images, image_type: 'base64' });
    },

    async getPostureHistory(limit = 20) {
        return api.get(`/api/v1/health/posture/history?limit=${limit}`);
    },

    async getPostureStats(days = 7) {
        return api.get(`/api/v1/health/posture/stats?days=${days}`);
    },

    async startVideoMonitor() {
        return api.post('/api/v1/health/video/start', {});
    },

    async stopVideoMonitor() {
        return api.post('/api/v1/health/video/stop', {});
    },

    async processVideoFrame(file) {
        return api.uploadFile('/api/v1/health/video/frame', file);
    },

    async getVideoStats() {
        return api.get('/api/v1/health/video/stats');
    },

    async getVideoHistory(limit = 50) {
        return api.get(`/api/v1/health/video/history?limit=${limit}`);
    },
};

const questionsAPI = {
    async getWrongQuestions() {
        return api.get('/api/v1/questions/wrong');
    },

    async addWrongQuestion(data) {
        return api.post('/api/v1/questions/wrong', data);
    },

    async deleteWrongQuestion(id) {
        return api.delete(`/api/v1/questions/wrong/${id}`);
    },
};

const resourcesAPI = {
    async getResources() {
        return api.get('/api/v1/resources/');
    },
};

const assistantAPI = {
    async chat(message) {
        return api.post('/api/v1/assistant/chat', { message });
    },
};

const ocrAPI = {
    async recognize(file) {
        return api.uploadFile('/api/v1/ocr/recognize', file);
    },
    async photoSearch(file, subject) {
        const formData = new FormData();
        formData.append('file', file);
        if (subject) {
            formData.append('subject', subject);
        }
        return api.postFormData('/api/v1/ocr/photo-search', formData);
    },
};

window.api = api;
window.authAPI = authAPI;
window.learningAPI = learningAPI;
window.healthAPI = healthAPI;
window.questionsAPI = questionsAPI;
window.resourcesAPI = resourcesAPI;
window.assistantAPI = assistantAPI;
window.ocrAPI = ocrAPI;
