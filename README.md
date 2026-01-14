# 🤪 表情包检索系统 (Meme Museum)

> **人工智能课程设计** | 基于 Streamlit 与开源数据集的轻量级表情包检索系统

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B)
![Status](https://img.shields.io/badge/Status-Completed-success)

📖 项目简介

**表情包检索系统** 是一个“即搜即得”的 Web 端表情包检索系统。

针对当前用户面临的海量表情包难以管理、搜索不精准的问题，本项目放弃了传统的爬虫加本地数据库的重型架构，创新性地采用了 **“Serverless 静态索引 + CDN 加速”** 的轻量级方案。系统直接接入 GitHub 高质量开源数据集 (ChineseBQB)，通过智能解析算法和内存缓存机制，实现了毫秒级的搜索响应体验。

## ✨ 核心功能

* **⚡ 极速检索**：基于内存的线性扫描算法，支持对文件名和分类进行模糊匹配，响应速度极快。
* **🚀 CDN 加速**：利用 `jsDelivr` CDN 替代原始 GitHub 链接，解决国内网络环境下图片加载慢、裂图等问题。
* **🛡️ 鲁棒性设计**：内置智能解析引擎 (`parse_item`)，能自动处理异构数据源（兼容列表与字典嵌套格式），防止系统因数据源微调而崩溃。
* **💾 智能缓存**：引入 `@st.cache_data` 机制，索引文件仅需首次加载，后续请求直接读取内存（TTL 1小时），极大降低延迟。
* **🖼️ 沉浸体验**：简洁的瀑布流布局，支持侧边栏热门分类导航及原图下载。

## 🛠️ 技术栈

* **开发语言**：Python 3.x
* **Web 框架**：Streamlit (用于快速构建交互式前端)
* **网络请求**：Requests
* **数据处理**：Re (正则表达式)
* **数据来源**：[zhaoolee/ChineseBQB](https://github.com/zhaoolee/ChineseBQB)

## 🚀 快速启动

### 1. 克隆仓库
```bash
git clone [https://github.com/Caster0898/Yanbiaoqing-2020212847.git](https://github.com/Caster0898/Yanbiaoqing-2020212847.git)
cd Yanbiaoqing-2020212847
