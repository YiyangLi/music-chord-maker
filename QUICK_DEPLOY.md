# 快速部署指南

## ✅ 已完成

1. ✅ 代码已推送到 GitHub: https://github.com/YiyangLi/music-chord-maker
2. ✅ Dockerfile 已创建
3. ✅ 部署脚本已准备就绪

## 🚀 部署步骤

### 1. 设置 API Token

你需要获取你的 `AI_BUILDER_TOKEN`。可以通过以下方式：

**方法 A: 通过 MCP 获取**
- 在 Cursor 中使用 AI-builders-coach MCP 的 `get_auth_token` 工具

**方法 B: 从环境变量获取**
- 如果你之前设置过，检查环境变量

**方法 C: 联系讲师**
- 如果以上方法都不行，联系你的讲师获取 token

### 2. 创建 .env 文件

在 `music-chord-maker` 目录下创建 `.env` 文件：

```bash
cd /Users/YiyangLi/Desktop/AI/music-chord-maker
echo "AI_BUILDER_TOKEN=你的实际token" > .env
```

### 3. 运行部署

```bash
source venv/bin/activate
python deploy.py
```

### 4. 检查部署状态

部署需要 5-10 分钟。你可以随时检查状态：

```bash
python deploy.py status
```

### 5. 访问你的应用

部署完成后，你的应用将在以下地址可用：

**https://music-chord-maker.ai-builders.space**

## 📋 部署信息

- **GitHub 仓库**: https://github.com/YiyangLi/music-chord-maker
- **服务名称**: music-chord-maker  
- **分支**: main
- **部署平台**: ai-builders.space

## 🔍 故障排除

如果部署失败：
1. 检查 token 是否正确设置
2. 确认 GitHub 仓库是公开的
3. 检查 Dockerfile 是否正确
4. 查看部署状态获取详细错误信息

## 📞 需要帮助？

如果遇到问题，联系讲师并提供：
- 服务名称: music-chord-maker
- GitHub 仓库: https://github.com/YiyangLi/music-chord-maker
- 错误信息或部署状态

