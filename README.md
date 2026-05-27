# 🎭 角色扮演AI助手

基于LangChain框架开发的智能角色扮演对话系统，支持多种角色模拟，包括小学生、老师、客服、医生、好朋友、商业顾问等。

## ✨ 功能特性

- **多角色支持**: 内置6种角色，涵盖不同场景
- **记忆功能**: 支持对话历史记忆，保持上下文连贯
- **前后端分离**: 使用LangServe部署后端服务，Streamlit构建前端
- **高并发支持**: 基于FastAPI的高性能服务
- **友好界面**: 使用Streamlit构建的现代化前端
- **模块化设计**: 后端代码完全模块化，易于扩展和维护

## 🛠️ 技术栈

- **后端**: Python 3.10+, LangChain, LangServe, FastAPI
- **前端**: Streamlit
- **大模型**: DeepSeek API

## 📁 项目结构

```
jkl/
├── backend/                    # 后端服务
│   ├── llm_config.py          # LLM配置模块
│   ├── characters.py          # 角色定义模块
│   ├── prompts.py             # Prompt模板模块
│   ├── chains.py              # Chain链式调用模块
│   ├── server.py              # LangServe服务入口
│   ├── requirements.txt       # 后端依赖
│   └── .env                   # 后端环境变量
├── frontend/                   # 前端应用
│   ├── app.py                 # Streamlit前端应用
│   ├── requirements.txt       # 前端依赖
│   └── .env                   # 前端环境变量
├── start_backend.bat          # Windows后端启动脚本
├── start_frontend.bat         # Windows前端启动脚本
├── start_backend.sh           # Linux/Mac后端启动脚本
├── start_frontend.sh          # Linux/Mac前端启动脚本
├── .gitignore                 # Git忽略配置
├── requirements.txt           # 全局依赖
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 方式一：使用启动脚本（推荐）

**Windows用户：**
```bash
# 启动后端服务
start_backend.bat

# 启动前端应用
start_frontend.bat
```

**Linux/Mac用户：**
```bash
# 启动后端服务
bash start_backend.sh

# 启动前端应用
bash start_frontend.sh
```

### 方式二：手动启动

#### 1. 安装依赖

```bash
# 安装全局依赖
pip install -r requirements.txt

# 或者分别安装前后端依赖
cd backend && pip install -r requirements.txt
cd ../frontend && pip install -r requirements.txt
```

#### 2. 配置环境变量

**后端配置**：
复制 `backend/.env.example` 到 `backend/.env`，并填写您的DeepSeek API Key：
```bash
cd backend
cp .env.example .env
```

编辑 `backend/.env` 文件：
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

**前端配置**：
复制 `frontend/.env.example` 到 `frontend/.env`：
```bash
cd frontend
cp .env.example .env
```

#### 3. 启动后端服务

```bash
cd backend
python server.py
```

服务将在 `http://localhost:8000` 启动。

#### 4. 启动前端应用

```bash
cd frontend
streamlit run app.py
```

前端将在 `http://localhost:8501` 启动。

## 🔗 API端点

- `GET /api/characters` - 获取角色列表
- `GET /api/characters/{character_id}` - 获取角色详情
- `POST /chat/{character_id}/invoke` - 与角色对话
- `GET /docs` - API文档（Swagger UI）

## 🎭 内置角色

| ID | 角色 | 描述 |
|----|------|------|
| xiaoming | 小明 | 活泼可爱的小学生 |
| teacher | 张老师 | 经验丰富的中学语文老师 |
| customer_service | 客服小美 | 专业的客服人员 |
| doctor | 王医生 | 资深的全科医生 |
| friend | 好朋友 | 知心好朋友 |
| business_consultant | 李顾问 | 资深商业顾问 |

## 📝 开发说明

### LLM调用
使用 `langchain_openai.ChatOpenAI` 调用DeepSeek API，支持自定义模型参数。

### Prompt工程
采用结构化Prompt模板，包含角色姓名、描述、性格、语气和示例回复。

### Chain链式调用
使用 `LLMChain` 实现Prompt与LLM的链式组合。

### Memory记忆
使用 `ConversationBufferMemory` 保持对话历史。

### 前后端分离架构
- **后端**: 提供RESTful API，使用LangServe部署，支持高并发
- **前端**: 独立的Streamlit应用，通过HTTP请求与后端通信
- **通信**: 前端通过requests库调用后端API

## 🌐 部署指南

### 后端部署
1. 将后端代码部署到服务器
2. 配置环境变量
3. 启动服务：`python backend/server.py`

### 前端部署
1. 将前端代码部署到服务器
2. 配置API_BASE_URL指向后端服务地址
3. 启动应用：`streamlit run frontend/app.py`

### Streamlit Cloud部署
1. 将项目推送到GitHub
2. 在Streamlit Cloud创建新应用
3. 配置环境变量（API_BASE_URL）
4. 部署

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**注意**: 本项目仅用于学习和研究目的，请遵守相关法律法规和DeepSeek API使用条款。