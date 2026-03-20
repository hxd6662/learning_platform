# 前后端 API 接口对照文档

## 接口对照表

### 1. 认证模块 (Auth)

| 前端调用 | 后端路由 | 方法 | 状态 |
|---------|---------|------|------|
| `/api/v1/auth/login` | `/api/v1/auth/login` | POST | ✅ 已对接 |
| `/api/v1/auth/register` | `/api/v1/auth/register` | POST | ✅ 已对接 |
| `/api/v1/auth/profile` | `/api/v1/auth/profile` | GET | ✅ 已对接 |

### 2. 学习模块 (Learning)

| 前端调用 | 后端路由 | 方法 | 状态 |
|---------|---------|------|------|
| `/api/v1/learning/stats/{user_id}` | `/api/v1/learning/stats/{user_id}` | GET | ✅ 已对接 |
| `/api/v1/learning/stats` | `/api/v1/learning/stats` | GET | ✅ 已对接 |
| `/api/v1/learning/goals` | `/api/v1/learning/goals` | GET | ✅ 已对接 |
| `/api/v1/learning/goals` | `/api/v1/learning/goals` | POST | ✅ 已对接 |
| `/api/v1/learning/goals/{goal_id}` | `/api/v1/learning/goals/{goal_id}` | PUT | ✅ 已对接 |
| `/api/v1/learning/goals/{goal_id}` | `/api/v1/learning/goals/{goal_id}` | DELETE | ✅ 已对接 |

### 3. 健康监测模块 (Health)

| 前端调用 | 后端路由 | 方法 | 状态 |
|---------|---------|------|------|
| `/api/v1/health/stats` | `/api/v1/health/stats` | GET | ✅ 已对接 |
| `/api/v1/health/records` | `/api/v1/health/records` | GET | ✅ 已对接 |
| `/api/v1/health/records` | `/api/v1/health/records` | POST | ✅ 已对接 |
| `/api/v1/health/report` | `/api/v1/health/report` | GET | ✅ 已对接 |
| `/api/v1/health/realtime` | `/api/v1/health/realtime` | GET | ✅ 已对接 |
| `/api/v1/health/monitor/start` | `/api/v1/health/monitor/start` | POST | ✅ 已对接 |
| `/api/v1/health/monitor/stop` | `/api/v1/health/monitor/stop` | POST | ✅ 已对接 |
| `/api/v1/health/realtime/detect` | `/api/v1/health/realtime/detect` | GET | ✅ 已对接 |
| `/api/v1/health/posture/detect` | `/api/v1/health/posture/detect` | POST | ✅ 已对接 |
| `/api/v1/health/posture/history` | `/api/v1/health/posture/history` | GET | ✅ 已对接 |
| `/api/v1/health/posture/stats` | `/api/v1/health/posture/stats` | GET | ✅ 已对接 |
| `/api/v1/health/video/start` | `/api/v1/health/video/start` | POST | ✅ 已对接 |
| `/api/v1/health/video/stop` | `/api/v1/health/video/stop` | POST | ✅ 已对接 |
| `/api/v1/health/video/frame` | `/api/v1/health/video/frame` | POST | ✅ 已对接 |
| `/api/v1/health/video/stats` | `/api/v1/health/video/stats` | GET | ✅ 已对接 |
| `/api/v1/health/video/history` | `/api/v1/health/video/history` | GET | ✅ 已对接 |

### 4. 错题本模块 (Questions)

| 前端调用 | 后端路由 | 方法 | 状态 |
|---------|---------|------|------|
| `/api/v1/questions/wrong` | `/api/v1/questions/wrong` | GET | ✅ 已对接 |
| `/api/v1/questions/wrong` | `/api/v1/questions/wrong` | POST | ✅ 已对接 |
| `/api/v1/questions/wrong/{id}` | `/api/v1/questions/wrong/{id}` | DELETE | ✅ 已对接 |

### 5. 学习资源模块 (Resources)

| 前端调用 | 后端路由 | 方法 | 状态 |
|---------|---------|------|------|
| `/api/v1/resources/` | `/api/v1/resources/` | GET | ✅ 已对接 |

### 6. AI助手模块 (Assistant)

| 前端调用 | 后端路由 | 方法 | 状态 |
|---------|---------|------|------|
| `/api/v1/assistant/chat` | `/api/v1/assistant/chat` | POST | ✅ 已对接 |

### 7. OCR识别模块 (OCR)

| 前端调用 | 后端路由 | 方法 | 状态 |
|---------|---------|------|------|
| `/api/v1/ocr/recognize` | `/api/v1/ocr/recognize` | POST | ✅ 已对接 |

---

## 前端 API 调用汇总

```javascript
// 认证相关
POST /api/v1/auth/login          - 用户登录
POST /api/v1/auth/register       - 用户注册
GET  /api/v1/auth/profile        - 获取用户信息

// 学习统计
GET  /api/v1/learning/stats/{user_id}  - 获取用户学习统计
GET  /api/v1/learning/stats             - 获取仪表盘统计

// 学习目标
GET  /api/v1/learning/goals      - 获取学习目标列表
POST /api/v1/learning/goals      - 创建学习目标
PUT  /api/v1/learning/goals/{id} - 更新学习目标
DELETE /api/v1/learning/goals/{id} - 删除学习目标

// 健康监测
GET  /api/v1/health/stats        - 获取健康统计
GET  /api/v1/health/records      - 获取健康记录
POST /api/v1/health/records      - 创建健康记录
GET  /api/v1/health/report       - 获取健康报告
GET  /api/v1/health/realtime     - 获取实时数据
POST /api/v1/health/monitor/start - 开始监测
POST /api/v1/health/monitor/stop  - 停止监测

// 坐姿检测
GET  /api/v1/health/realtime/detect - 实时坐姿检测
POST /api/v1/health/posture/detect  - 坐姿检测(Base64)
GET  /api/v1/health/posture/history - 坐姿历史
GET  /api/v1/health/posture/stats   - 坐姿统计

// 视频流坐姿检测
POST /api/v1/health/video/start   - 启动视频监测
POST /api/v1/health/video/stop    - 停止视频监测
POST /api/v1/health/video/frame   - 处理视频帧
GET  /api/v1/health/video/stats   - 获取视频监测统计
GET  /api/v1/health/video/history - 获取视频监测历史

// 错题本
GET  /api/v1/questions/wrong      - 获取错题列表
POST /api/v1/questions/wrong      - 添加错题
DELETE /api/v1/questions/wrong/{id} - 删除错题

// 学习资源
GET  /api/v1/resources/           - 获取学习资源列表

// AI助手
POST /api/v1/assistant/chat       - AI对话

// OCR识别
POST /api/v1/ocr/recognize        - OCR图片识别
```

---

## 后端路由注册 (src/app.py)

```python
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(learning.router, prefix="/api/v1/learning", tags=["学习"])
app.include_router(questions.router, prefix="/api/v1/questions", tags=["错题本"])
app.include_router(health.router, prefix="/api/v1/health", tags=["健康监测"])
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["AI助手"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["学习资源"])
app.include_router(ocr.router, prefix="/api/v1/ocr", tags=["OCR识别"])
```

---

## 数据格式对照

### 登录响应
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### 用户信息响应
```json
{
  "id": 1,
  "username": "user",
  "email": "user@example.com",
  "nickname": "用户昵称",
  "avatar": null
}
```

### 学习统计响应
```json
{
  "success": true,
  "data": {
    "stats": [...],
    "totalStudyMinutes": 120,
    "totalQuestions": 35,
    "consecutiveDays": 7,
    "accuracy": 85.5
  }
}
```

### 坐姿检测响应
```json
{
  "success": true,
  "data": {
    "status": "good",
    "score": 85.5,
    "head_angle": 5.2,
    "shoulder_balance": "良好",
    "back_curve": "正常",
    "eye_distance": 45.0,
    "details": {
      "recommendation": "坐姿良好，请继续保持"
    }
  }
}
```

---

*文档更新时间：2026-03-19*
