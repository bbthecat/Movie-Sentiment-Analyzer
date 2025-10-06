# 🪰 Deploy to Fly.io

Fly.io offers global deployment with excellent performance!

## ✨ Why Fly.io?

- **🌍 Global Edge** - Deploy worldwide
- **💰 3 Free VMs** - Generous free tier
- **⚡ Fast Performance** - Edge computing
- **🔄 Auto Scaling** - Scale based on demand
- **🛠️ Docker Support** - Full container support

## 🚀 Quick Deploy

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login
```bash
fly auth login
```

### Step 3: Deploy
```bash
# From your project directory
fly launch

# Follow the prompts:
# - App name: movie-sentiment-analyzer
# - Region: sin (Singapore) or choose closest
# - Deploy now: Yes
```

### Step 4: Set Environment Variables
```bash
fly secrets set OMDB_API_KEY=your_omdb_api_key
fly secrets set TMDB_API_KEY=your_tmdb_api_key
fly secrets set HF_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
fly secrets set DATA_DIR=backend/data
```

### Step 5: Deploy Again
```bash
fly deploy
```

## 🔧 Configuration

### `fly.toml`
```toml
app = "movie-sentiment-analyzer"
primary_region = "sin"

[build]

[env]
  PORT = "8000"
  PYTHONPATH = "."

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  interval = "10s"
  timeout = "2s"
  grace_period = "5s"
  method = "GET"
  path = "/api/health"

[processes]
  app = "uvicorn app:app --host 0.0.0.0 --port 8000"
```

## 🎯 Features

- **Global deployment** - Deploy to multiple regions
- **Auto-scaling** - Scale based on traffic
- **Health checks** - Automatic health monitoring
- **SSL certificates** - Automatic HTTPS
- **Persistent volumes** - For data storage

## 💰 Pricing

- **Free Tier**: 3 shared VMs, 3GB storage
- **Paid**: $1.94/month per VM

## 🆚 Fly.io vs Others

| Feature | Fly.io | Railway | Vercel |
|---------|--------|---------|--------|
| **Global Edge** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Free Tier** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Docker Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🚨 Troubleshooting

### Common Issues

1. **Deploy Fails**
   - Check fly.toml configuration
   - Ensure Dockerfile exists

2. **App Won't Start**
   - Check start command in fly.toml
   - Verify environment variables

3. **Health Check Fails**
   - Ensure /api/health endpoint works
   - Check internal port configuration

### Useful Commands

```bash
# View logs
fly logs

# Check app status
fly status

# Scale app
fly scale count 2

# Deploy to specific region
fly deploy --region sin
```

## 🎉 Success!

Your Movie Sentiment Analyzer is now live on Fly.io!

- **🌐 URL**: `https://movie-sentiment-analyzer.fly.dev`
- **📊 Dashboard**: Available in Fly.io console
- **🔄 Auto Deploy**: Use `fly deploy` to update
- **📈 Monitoring**: Real-time logs and metrics

---

**Happy Flying! 🪰**
