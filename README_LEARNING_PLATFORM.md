# 基于AI可移动设备的青少年智能学习平台

一个基于FastAPI + MySQL的青少年智能学习平台，结合AI技术提供个性化学习辅助。

## 项目概述

本项目是一个针对青少年的智能学习平台，通过AI可移动设备（双摄像头学习装置）提供：

- 题目拍照识别与解析
- 错题本管理
- 学习行为分析
- 坐姿/疲劳监测
- AI智能助手
- 个性化学习推荐

## 技术架构

### 后端技术栈

- **框架**: FastAPI (Python)
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0
- **AI/ML**:
  - OpenCV (视觉处理)
  - OCR (文字识别，如百度/阿里OCR)
  - 大模型API (DeepSeek、文心一言等)
- **实时通信**: WebSocket

### 前端技术栈

- **移动应用**: React Native (Expo)
- **Web端**: Vue.js + Element UI (预留扩展)

## 目录结构

```
projects/
├── src/                          # Python/FastAPI 后端
│   ├── main.py                   # FastAPI 应用入口
│   ├── api/                      # API 路由
│   │   ├── __init__.py
│   │   ├── auth.py               # 认证相关接口
│   │   ├── learning.py           # 学习数据接口
│   │   ├── questions.py          # 错题本接口
│   │   ├── health.py             # 健康监测接口
│   │   ├── assistant.py          # AI助手接口
│   │   ├── resources.py          # 学习资源接口
│   │   └── ocr.py                # OCR识别接口
│   ├── models/                   # 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── learning.py
│   │   ├── question.py
│   │   └── health.py
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── ocr_service.py
│   │   └── health_service.py
│   ├── storage/
│   │   └── database/
│   │       ├── db.py             # 数据库连接
│   │       └── shared/
│   │           └── model.py      # 基础模型
│   └── utils/                    # 工具函数
├── client/                       # React Native 移动应用
│   ├── app/                      # Expo Router 路由
│   ├── screens/                  # 页面组件
│   │   ├── home/                 # 首页
│   │   ├── photo-learning/       # 拍照学习
│   │   ├── wrong-questions/      # 错题本
│   │   ├── health-monitor/       # 健康监测
│   │   ├── assistant/            # AI助手
│   │   ├── learning-goals/       # 学习目标
│   │   ├── learning-resources/   # 学习资源
│   │   └── profile/              # 个人中心
│   └── components/               # 可复用组件
├── server/                       # (可选) Express.js 备用后端
├── docs/                         # 文档
├── .env.example                  # 环境变量示例
├── requirements.txt              # Python依赖
└── README.md
```

## 核心功能模块

### 1. 核心功能模块

#### 拍照学习 (Photo Learning)

- 通过摄像头拍摄题目
- OCR识别题目内容
- AI解析解题思路
- 关联知识点

#### 错题本 (Wrong Questions)

- 自动收集错题
- 错题分类整理
- 知识点标签
- 错题重做与复习

#### 学习统计 (Learning Stats)

- 学习时长统计
- 题目完成情况
- 连续学习天数
- 学习数据分析

#### 健康监测 (Health Monitor)

- 实时坐姿检测
- 疲劳状态识别
- 休息提醒
- 健康报告生成

#### AI助手 (AI Assistant)

- 语音/文字对话
- 题目讲解
- 知识点答疑
- 学习建议

#### 学习资源 (Learning Resources)

- 题库管理
- 知识点库
- 视频课程
- 学习计划推荐

### 2. 硬件支持

#### 双摄像头设计

- **上摄像头 (2.8mm广角)**: 拍摄桌面/试卷，捕捉学习内容
- **下摄像头**: 拍摄学生面部，监测学习状态

#### 物理结构

- L形隐藏式设计
- 紧凑尺寸 (约13cm×3cm×90cm)
- 适合桌面场景

## 快速开始

### 环境要求

- Python 3.10+
- MySQL 8.0+
- Node.js 18+ (用于前端开发)
- pnpm (推荐包管理器)

### 1. 数据库配置

创建MySQL数据库：

```sql
CREATE DATABASE learning_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'learning_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON learning_platform.* TO 'learning_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. 后端安装

```bash
# 克隆项目
cd projects

# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库连接等信息
```

### 3. 配置环境变量

编辑 `.env` 文件：

```env
# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=learning_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=learning_platform

# JWT密钥
SECRET_KEY=your-secret-key-change-this-in-production

# AI服务配置
OCR_PROVIDER=baidu  # baidu, aliyun
OCR_API_KEY=your-ocr-api-key
OCR_SECRET_KEY=your-ocr-secret-key

LLM_PROVIDER=deepseek  # deepseek, wenxin
LLM_API_KEY=your-llm-api-key

# 服务器配置
HOST=0.0.0.0
PORT=8000
```

### 4. 启动后端服务

```bash
cd src
python main.py
```

或使用uvicorn：

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API文档将在 <http://localhost:8000/docs> 可用。

### 5. 启动前端应用

```bash
# 安装依赖
pnpm install

# 启动开发服务器
cd client
pnpm expo start
```

## API接口概览

### 认证模块

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/profile` - 获取用户信息

### 学习统计

- `GET /api/v1/learning-stats/:userId` - 获取学习统计
- `POST /api/v1/learning-stats` - 记录学习数据

### 错题本

- `GET /api/v1/wrong-questions` - 获取错题列表
- `POST /api/v1/wrong-questions` - 添加错题
- `PUT /api/v1/wrong-questions/:id` - 更新错题
- `DELETE /api/v1/wrong-questions/:id` - 删除错题

### 拍照学习

- `POST /api/v1/ocr/recognize` - OCR识别题目
- `POST /api/v1/photo-learning/analyze` - AI分析题目

### 健康监测

- `POST /api/v1/health-monitor/record` - 记录健康数据
- `GET /api/v1/health-monitor/report` - 获取健康报告

### AI助手

- `POST /api/v1/assistant/chat` - 与AI对话
- `GET /api/v1/assistant/history` - 获取对话历史

## 数据库设计

### 核心数据表

#### 用户表 (users)

- id, username, email, password\_hash, created\_at, updated\_at

#### 学习统计表 (learning\_stats)

- id, user\_id, study\_date, study\_minutes, questions\_attempted, questions\_correct, created\_at

#### 错题表 (wrong\_questions)

- id, user\_id, question\_text, question\_image, correct\_answer, user\_answer, knowledge\_point, difficulty, created\_at, reviewed\_at

#### 健康监测表 (health\_records)

- id, user\_id, record\_time, posture\_score, fatigue\_level, eye\_strain, notes, created\_at

#### 学习资源表 (learning\_resources)

- id, title, description, type, content\_url, knowledge\_points, difficulty, created\_at

#### AI对话表 (ai\_conversations)

- id, user\_id, message, response, created\_at

## 开发指南

### 添加新的API接口

1. 在 `src/api/` 下创建新的路由文件
2. 在 `src/main.py` 中注册路由
3. 在 `src/models/` 中定义数据模型（如需要）
4. 在 `src/services/` 中实现业务逻辑

### 数据库迁移

使用Alembic进行数据库迁移：

```bash
# 初始化迁移（首次）
alembic init alembic

# 创建迁移脚本
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head
```

## 移动端功能说明

### 首页 (Home)

- 展示学习统计（学习时长、完成题目、连续天数）
- 快捷功能入口
- 今日推荐

### 拍照学习 (Photo Learning)

- 调用摄像头拍照
- 预览和裁剪图片
- 发送到后端进行OCR识别和AI解析
- 显示解析结果

### 错题本 (Wrong Questions)

- 错题列表展示
- 错题详情查看
- 错题重做
- 错题分类筛选

### 坐姿监测 (Health Monitor)

- 实时预览摄像头画面
- 显示坐姿/疲劳状态
- 历史记录查看

### AI助手 (Assistant)

- 聊天界面
- 语音输入
- 对话历史

### 学习目标 (Learning Goals)

- 目标列表
- 创建/编辑目标
- 目标进度追踪

### 学习资源 (Learning Resources)

- 资源浏览
- 资源搜索
- 资源收藏

### 个人中心 (Profile)

- 用户信息展示
- 设置修改
- 数据统计

## 扩展到Web应用

本项目架构已为Web端扩展做好准备：

### Web端技术栈建议

- **框架**: Vue 3 + Vite
- **UI组件库**: Element Plus / Ant Design Vue
- **状态管理**: Pinia
- **路由**: Vue Router

### 共享代码

- API接口设计保持一致
- 业务逻辑可复用
- 数据库结构共用

详见 `docs/WEB_PLATFORM_GUIDE.md`

## 配置说明

### AI服务配置

#### OCR配置

支持百度OCR和阿里OCR：

```python
# 百度OCR
OCR_PROVIDER=baidu
BAIDU_OCR_API_KEY=your-key
BAIDU_OCR_SECRET_KEY=your-secret

# 阿里OCR
OCR_PROVIDER=aliyun
ALIYUN_OCR_ACCESS_KEY_ID=your-id
ALIYUN_OCR_ACCESS_KEY_SECRET=your-secret
```

#### 大模型配置

支持DeepSeek和文心一言：

```python
# DeepSeek
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-key

# 文心一言
LLM_PROVIDER=wenxin
WENXIN_API_KEY=your-key
WENXIN_SECRET_KEY=your-secret
```

## 常见问题

### 数据库连接失败

- 检查MySQL服务是否启动
- 确认.env中的数据库配置正确
- 检查用户权限

### 前端无法连接后端

- 确认后端服务已启动
- 检查 `EXPO_PUBLIC_BACKEND_BASE_URL` 配置
- 确认防火墙设置

### OCR识别不准确

- 确保图片清晰
- 调整拍摄角度和光线
- 考虑使用更高精度的OCR服务

## 团队成员

- **黄旭东** - 组长，后端开发
- 萧远声 - 后端开发
- 刘鑫彤 - 前端开发\&UI设计
- **何文皓**- 视觉与推荐算法

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请联系项目维护者。

***

**注意**: 这是一个项目方案初稿，后续会根据实际开发情况不断完善。
