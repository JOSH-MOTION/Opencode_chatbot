# 🚀 Railway Deployment Guide

## Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Chatbot web UI"
git branch -M main
git remote add origin https://github.com/yourusername/chatbot.git
git push -u origin main
```

## Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Flask app
6. Click "Deploy"

## Step 3: Configure Environment (if needed)
Railway will automatically:
- Install dependencies from `pyproject.toml`
- Use `Procfile` to start the app
- Assign a URL
- Set up HTTPS

## 🎯 What You Get
- **Free tier**: $5/month credit (enough for your chatbot)
- **Auto-deploys** on git push
- **Custom domain** support
- **Environment variables** for secrets
- **Logs** and monitoring

## 🔧 What I Added
- `Procfile` - Tells Railway how to run your app
- Updated `.gitignore` - Excludes sensitive files

## 🌐 After Deployment
Your app will be available at: `https://your-app-name.railway.app`

## 📱 Mobile Ready
Your web UI is fully responsive and will work perfectly on mobile devices!

## 🔥 Pro Tips
- Railway automatically restarts your app if it crashes
- You can add a custom domain for free
- Monitor usage in Railway dashboard
- Scale up if you get more traffic
