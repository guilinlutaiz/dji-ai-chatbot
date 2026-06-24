# 🚁 大疆无人机销售（售后）服务AI聊天机器人

> 大数据机器学习课程项目 - 全栈开发的智能客服系统

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red.svg)](https://fastapi.tiangolo.com/)
[![Qwen](https://img.shields.io/badge/通义千问-qwen--turbo-orange.svg)](https://dashscope.aliyun.com/)

---

## ✨ 项目简介

本项目是一款面向大疆无人机的销售与售后服务AI聊天机器人，采用**"本地知识库+大语言模型"的双层智能架构**，实现7×24小时无人值守智能客服功能。系统能够准确回答产品咨询、价格查询、售后政策、飞行法规等专业问题，同时具备无关问题过滤能力，保证客服角色定位准确。

---

## 🎯 核心功能

| 功能模块 | 功能描述 |
|----------|----------|
| 🤖 **智能问答** | 接入通义千问大模型，自然语言交互 |
| 📚 **本地知识库** | 产品参数、售后政策、飞行法规，准确可靠 |
| 💬 **多轮对话** | 支持会话管理，上下文理解 |
| 🔍 **知识库管理** | 支持知识的增删改查 |
| 🎨 **Web前端** | 无人机商城界面 + 悬浮聊天窗口 |
| 🔒 **边界控制** | 无关问题自动识别，保持客服定位 |
| 📱 **APP支持** | 移动端应用（开发中） |
| ☁️ **云部署** | 支持公有云部署，提供公网访问 |

---

## 🛠️ 技术栈

### 后端技术
- **Web框架**：FastAPI + Uvicorn ASGI
- **ORM框架**：SQLAlchemy
- **数据库**：SQLite（开发环境）/ MySQL（生产环境）
- **AI大模型**：通义千问 qwen-turbo（阿里云百炼）
- **配置管理**：python-dotenv

### 前端技术
- **页面结构**：HTML5
- **样式设计**：CSS3
- **交互逻辑**：原生JavaScript
- **HTTP请求**：Axios

### 工程化
- **版本控制**：Git + GitHub
- **部署方式**：支持Docker、阿里云ECS
- **开源协议**：MIT License

---

## 🚀 快速启动

### 环境要求
- Python 3.8+
- 通义千问API Key（阿里云百炼）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/guilinlutaiz/dji-ai-chatbot.git
cd dji-ai-chatbot
安装依赖
bash
运行
pip install -r requirements.txt
配置环境变量
创建 .env 文件，填入配置：
env
# 大模型配置
OPENAI_API_KEY=你的通义千问API Key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-turbo

# 数据库配置
DATABASE_URL=sqlite:///./dji_bot.db

# 服务配置
HOST=0.0.0.0
PORT=8000
启动后端服务
bash
运行
python main.py
服务运行地址：http://localhost:8000
打开前端
双击 index.html 即可打开无人机商城页面，点击右下角客服按钮开始对话。
📦 项目结构
plaintext
dji-ai-chatbot/
├── main.py              # FastAPI后端主程序
├── database.py          # 数据库配置与ORM模型
├── knowledge.py         # 大疆产品知识库
├── bot.py               # 命令行聊天机器人
├── index.html           # 前端商城页面
├── style.css            # 前端样式文件
├── main.js              # 前端交互逻辑
├── axios.min.js         # HTTP请求库
├── requirements.txt     # Python依赖清单
├── .env.example         # 环境变量示例
├── images/              # 产品图片资源
├── video/               # 宣传视频资源
├── LICENSE              # 开源协议
└── README.md            # 项目说明文档
🔌 API 接口文档
核心接口
1. 聊天对话接口
http
POST /api/chat
Content-Type: application/json

{
    "message": "新手推荐哪款无人机？",
    "session_id": "user_session_001"
}
响应：
json
{
    "reply": "强烈推荐Mini 5 Pro！\n✅ 249g免实名登记\n...",
    "session_id": "user_session_001"
}
2. 健康检查
http
GET /health
3. 知识库管理
http
POST /api/knowledge/add    # 添加知识
GET  /api/knowledge/list   # 获取知识列表
接口文档
启动服务后访问：http://localhost:8000/docs （自动生成的 Swagger 文档）
📚 知识库覆盖
产品库（7 款主流机型）
表格
机型	定位	价格	亮点
DJI Mini 5 Pro	2026 入门旗舰	5288 元	249g 免登记、全向避障 Pro
DJI Mini 4 Pro	经典爆款	4788 元	全向避障、45 分钟续航
DJI Mini 4K	入门首选	3288 元	249g、4K 视频
DJI Air 3S	2026 中端旗舰	7688 元	双主摄、夜景增强
DJI Air 3	创作者首选	6988 元	双主摄、20km 图传
DJI Mavic 4	2026 专业旗舰	12888 元	哈苏 2 代、8K 视频
DJI Mavic 3 Classic	专业画质	9288 元	哈苏相机、5.1K 视频
常见问题 FAQ
✅ 实名登记与飞行法规
✅ 保修政策与售后流程
✅ 电池使用与续航优化
✅ 安全飞行与避障指南
✅ DJI Care 随心换介绍
✅ 图传断连应急处理
👥 团队成员与分工
表格
成员	角色	负责板块
邢宏波	产品与测试负责人	市场调研、项目定位、报告统筹、功能测试、Web 前端开发
王刚	AI 核心开发	知识库构建、大模型对接、提示词工程、对话接口实现、GitHub 仓库维护
秦晓杰	全栈开发与架构	系统架构设计、数据库开发、后端 API、APP 开发、云服务器部署
详细分工说明
邢宏波 - 产品与报告统筹汇报 + 测试 + Web 前端开发
负责板块：
市场调研、项目定位、用户画像、核心功能梳理
项目报告整体统筹、格式排版、最终定稿
功能 / 性能 / 安全测试
Web 聊天前端页面开发
主要任务：
分析无人机销售售后客服痛点、对标大疆 AI 客服优缺点，确定项目差异化定位
全项目测试工作，编写测试用例、整理测试结果
独立开发 Web 端聊天交互前端页面，页面调试优化
报告撰写：项目背景、市场分析、总结、系统测试与部署
对应阶段：
阶段一：市场调研与项目定位
撰写 "项目背景与市场分析" 章节
明确机器人核心功能，定义目标用户画像
阶段五：集成、测试与部署
撰写 "系统测试与部署" 章节，说明测试用例、部署环境及访问方式
交付物：
市场分析摘要、完整 Word 项目报告、项目文档规范管理、项目 PPT、测试用例与结果、成品可交互 Web 前端页面
王刚 - AI 核心（模型 + 知识库 + 提示词）
负责板块：
销售 / 售后知识库构建（Q&A）
大模型 API 对接
对话接口实现
提示词工程设计与优化
主要任务：
围绕无人机行业搭建销售 / 售后知识库（Q&A 对、产品手册、飞行政策、保修条例等）
精准对接大型语言模型 API（通义千问）
设计并优化系统提示词，保证回答专业精准，设置未知问题引导话术
完成基础的对话接口，处理用户输入并返回 AI 生成的回答
负责创建 GitHub 仓库、收集全员代码上传、维护开源地址
对应阶段：
阶段三：AI 功能核心实现
撰写 "AI 模型集成与优化" 章节，详细说明提示词设计思路和调优过程
交付物：
知识库文档、可调用 AI 对话服务、提示词设计说明
秦晓杰 - 后端 + 数据库 + 架构 + APP 开发 + 部署
负责板块：
系统架构设计、模块设计
数据库 ER 图、数据库搭建
后端 API 开发（会话、历史、知识库 CRUD）
APP 开发
前后端 + AI 联调
云服务器部署、提供公网 URL
主要任务：
设计系统架构，完成技术栈选型，绘制架构图、数据库 ER 图
后端开发：用户会话管理、知识库 CRUD 接口、AI 模型调用代理、对话历史存储等 API
数据库实现：根据 ER 图建库，完成数据持久化
独立完成 APP 全功能开发
后端、AI 服务、Web 前端三方对接联调
项目整体部署至公有云，输出公网访问地址
对应阶段：
阶段二：技术选型与系统设计
撰写 "系统架构设计" 章节，包含技术架构图
完成核心功能模块设计，设计数据库 ER 图
阶段四：全栈开发与实现
撰写 "系统实现" 章节，描述关键技术实现细节、问题与解决方案
交付物：
架构图、ER 图、后端接口服务、数据库实现、成品 APP、线上可访问 URL
📊 评分标准
表格
评分项	权重	说明
项目报告	10%	结构完整性、逻辑清晰度、技术深度、文档规范性
AI 聊天机器人 Web 应用	40%	功能完整性与实用性（20%）、技术实现复杂度与代码质量（10%）、用户界面与交互体验（10%）
项目管理与团队协作	10%	更新日志、文档提交情况、答辩表现综合评定
🚀 部署方案
本地开发环境
操作系统：Windows/macOS/Linux
Python 版本：3.8+
数据库：SQLite
生产环境推荐
服务器：阿里云 ECS 2 核 4G
操作系统：Ubuntu 22.04 LTS
反向代理：Nginx
进程守护：Supervisor
数据库：MySQL 8.0
域名：绑定正式域名，配置 HTTPS 证书
📈 后续优化方向
知识库升级：接入向量数据库，实现语义检索而非关键词匹配
对话记忆：支持多轮对话上下文理解
流式输出：实现打字机效果，提升用户体验
管理后台：开发可视化知识库管理后台
多轮对话：支持上下文关联的深度对话
APP 完善：完成移动端 APP 全功能开发
📄 开源协议
本项目采用 MIT License 开源协议，欢迎自由使用、修改和分发。
🙏 致谢
感谢阿里云百炼提供的通义千问大模型服务
感谢 FastAPI、SQLAlchemy 等优秀开源项目
感谢大疆创新提供的产品参考资料
<div align="center"> <p>Made with ❤️ by 大疆AI聊天机器人团队</p> <p>大数据机器学习课程项目 | 2026</p> </div> ```
