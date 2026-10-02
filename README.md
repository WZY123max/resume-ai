 ResumeAI · AI 简历诊断工具

一个面向应届生和在校生的 AI 简历诊断工具。用户粘贴简历和目标岗位，工具输出结构化诊断报告：匹配度、问题清单、逐条建议、优化后简历、修改对比、待补充清单、学习路径建议。

 技术栈

后端：FastAPI + DeepSeek API
前端：原生 HTML / CSS / JavaScript
提示词：独立文件管理，配置与代码分离

 项目结构

resume-ai/
├── backend/
│   ├── app.py              # FastAPI 后端
│   ├── prompt.py           # 提示词构建
│   ├── config/             # 简历规则配置
│   └── reference/          # 参考案例 + 学习资源池
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── requirements.txt

 本地运行

1. 安装依赖：

   pip install -r requirements.txt

2. 在根目录建 `.env`，填入：

   DEEPSEEK_API_KEY=sk-你的Key

3. 启动后端：

   cd backend
   uvicorn app:app --reload

4. 用浏览器打开 `frontend/index.html`

 功能

岗位校准：目标岗位与经历不匹配时，给出提醒
结构化诊断：匹配度、问题清单、逐条建议
优化后简历：不编造，只改写已有事实
修改对比：逐条展示“原文→改后→原因”
学习路径：从资源池推荐学习方向

说明

本项目为个人学习作品，用于展示 AI 全栈开发流程。
