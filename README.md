# 智能菜谱推荐系统

这是一个基于Streamlit开发的智能菜谱推荐系统，可以根据用户输入的食材推荐相关的菜谱。

## 功能特点

- 根据现有食材推荐菜谱
- 显示菜谱图片和详细信息
- 列出所需和缺少的食材
- 提供完整菜谱链接

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/你的用户名/recipe-recommendation-app.git
cd recipe-recommendation-app
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
- 复制 `.env.example` 文件为 `.env`
- 在 `.env` 文件中添加你的 Spoonacular API 密钥

4. 运行应用：
```bash
streamlit run app.py
```

## 部署说明

本应用可以部署到 Streamlit Cloud：

1. 将代码推送到 GitHub
2. 在 Streamlit Cloud 中连接仓库
3. 在 Streamlit Cloud 中设置环境变量 `SPOONACULAR_API_KEY`

## 注意事项

- 需要注册 [Spoonacular API](https://spoonacular.com/food-api) 获取 API 密钥
- 请勿将 API 密钥直接提交到 GitHub
