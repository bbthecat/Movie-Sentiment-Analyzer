# 🚂 Deploy to Railway

Railway is one of the easiest platforms to deploy your Movie Sentiment Analyzer!

## ✨ Why Railway?

- **💰 $5 Free Credit** - Every month
- **⚡ Super Fast Deploy** - Deploy in seconds
- **🔄 Auto Deploy** - From GitHub
- **🛠️ Zero Config** - Works out of the box
- **📊 Built-in Monitoring** - Real-time logs

## 🚀 Quick Deploy

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will auto-detect and deploy!

### Step 3: Set Environment Variables
In Railway dashboard:
- Go to your project
- Click "Variables" tab
- Add these variables:
  ```
  OMDB_API_KEY=your_omdb_api_key
  TMDB_API_KEY=your_tmdb_api_key
  HF_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
  DATA_DIR=backend/data
  ```

### Step 4: Get Your URL
- Railway will give you a URL like: `https://your-app.railway.app`
- Your app is live! 🎉

## 🔧 Configuration Files

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `Procfile`
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

### `runtime.txt`
```
python-3.11.0
```

## 🎯 Features

- **Auto-detection** - Railway detects Python automatically
- **Dependency management** - Installs from requirements.txt
- **Health checks** - Monitors /api/health endpoint
- **Auto-restart** - Restarts on failure
- **Real-time logs** - See what's happening

## 💰 Pricing

- **Free Tier**: $5 credit per month
- **Hobby**: $5/month for more resources
- **Pro**: $20/month for production

## 🆚 Railway vs Others

| Feature | Railway | Vercel | Render |
|---------|---------|--------|--------|
| **Ease** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speed** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Free Tier** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Python Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check requirements.txt exists
   - Ensure Python version is compatible

2. **App Won't Start**
   - Check start command in railway.json
   - Verify PORT environment variable

3. **Import Errors**
   - Ensure all dependencies in requirements.txt
   - Check file structure

### Getting Help

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Community**: [discord.gg/railway](https://discord.gg/railway)
- **Support**: Available in dashboard

## 🎉 Success!

Your Movie Sentiment Analyzer is now live on Railway!

- **🌐 URL**: `https://your-app.railway.app`
- **📊 Dashboard**: Available in Railway
- **🔄 Auto Deploy**: Updates on git push
- **📈 Monitoring**: Real-time logs and metrics

---

**Happy Deploying! 🚂**
