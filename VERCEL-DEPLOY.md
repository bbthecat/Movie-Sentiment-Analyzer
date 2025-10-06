# 🚀 Deploy to Vercel

This guide will help you deploy the Movie Sentiment Analyzer to Vercel as a serverless function.

## ✨ Why Vercel?

- **⚡ Fast Deployments** - Deploy in seconds
- **🌍 Global CDN** - Fast worldwide access
- **💰 Free Tier** - Generous free limits
- **🔄 Auto Deploy** - Automatic deployments from GitHub
- **📊 Analytics** - Built-in performance monitoring

## 📋 Prerequisites

1. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository** - Your code pushed to GitHub
3. **API Keys** - OMDb and TMDb API keys

## 🔑 Get API Keys

### OMDb API Key
1. Go to [OMDb API](http://www.omdbapi.com/apikey.aspx)
2. Sign up for a free API key
3. Copy your API key

### TMDb API Key
1. Go to [TMDb API](https://www.themoviedb.org/settings/api)
2. Create an account and request an API key
3. Copy your API key

## 🚀 Deploy to Vercel

### Option 1: Using Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Import project to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

3. **Configure the project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave empty)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements-vercel.txt`

4. **Set Environment Variables**
   - In project settings, go to "Environment Variables"
   - Add the following:
     ```
     OMDB_API_KEY=your_omdb_api_key_here
     TMDB_API_KEY=your_tmdb_api_key_here
     HF_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
     DATA_DIR=backend/data
     ```

5. **Deploy**
   - Click "Deploy"
   - Wait for the deployment to complete
   - Your app will be available at `https://your-app.vercel.app`

### Option 2: Using Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**
   ```bash
   cd Movie-Sentiment-Analyzer
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add OMDB_API_KEY
   vercel env add TMDB_API_KEY
   vercel env add HF_MODEL_NAME
   vercel env add DATA_DIR
   ```

5. **Redeploy with environment variables**
   ```bash
   vercel --prod
   ```

## ⚙️ Vercel Configuration

The project includes a `vercel.json` file with optimized settings:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  },
  "functions": {
    "app.py": {
      "maxDuration": 30
    }
  }
}
```

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OMDB_API_KEY` | OMDb API key for movie data | Yes | - |
| `TMDB_API_KEY` | TMDb API key for reviews | Yes | - |
| `HF_MODEL_NAME` | Hugging Face model name | No | `distilbert-base-uncased-finetuned-sst-2-english` |
| `DATA_DIR` | Data directory path | No | `backend/data` |

## 📊 Vercel Free Tier Limits

- **Function Execution Time**: 10 seconds (Hobby), 60 seconds (Pro)
- **Bandwidth**: 100GB per month
- **Function Invocations**: 100GB-hours per month
- **Cold Starts**: Functions may have cold start delays

## 🧪 Test Your Deployment

1. **Visit your deployed URL**
   ```
   https://your-app.vercel.app
   ```

2. **Check the health endpoint**
   ```
   https://your-app.vercel.app/api/health
   ```

3. **Test the API documentation**
   ```
   https://your-app.vercel.app/docs
   ```

## 🎯 API Endpoints

Once deployed, your API will be available at:

- **🏠 Homepage**: `GET /` - Beautiful web interface
- **❤️ Health Check**: `GET /api/health`
- **📖 API Documentation**: `GET /docs`
- **🔍 Movie Search**: `GET /api/movies/search?query={query}`
- **🎬 Movie Details**: `GET /api/movies/{imdb_id}`
- **📝 Upload Reviews**: `POST /api/reviews/{imdb_id}/upload`
- **🎲 Generate Mock Data**: `POST /api/reviews/{imdb_id}/generate`
- **🌐 Import from TMDb**: `POST /api/reviews/{imdb_id}/import/tmdb`
- **🧠 Analyze Sentiment**: `POST /api/analyze/{imdb_id}`
- **📊 Get Summary**: `GET /api/summary/{imdb_id}`
- **📈 Get Analysis**: `GET /api/analysis/{imdb_id}`
- **📄 Export CSV**: `GET /api/export/{imdb_id}.csv`
- **🔤 Single Text Analysis**: `POST /api/analyze-text`

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that `requirements-vercel.txt` exists
   - Ensure Python version is compatible (3.9+)
   - Verify all dependencies are listed

2. **Function Timeout**
   - Vercel has execution time limits
   - Consider optimizing model loading
   - Use smaller models for faster processing

3. **Import Errors**
   - Ensure all dependencies are in `requirements-vercel.txt`
   - Check that `PYTHONPATH` is set correctly

4. **API Keys Not Working**
   - Ensure environment variables are set in Vercel dashboard
   - Verify API keys are valid and active

5. **Cold Start Issues**
   - First request may be slow due to model loading
   - Consider using smaller models
   - Implement model caching if possible

### Performance Optimization

1. **Model Loading**
   - Models are loaded on each cold start
   - Consider using smaller/faster models
   - Implement model caching strategies

2. **Memory Usage**
   - Monitor memory usage in Vercel dashboard
   - Optimize data processing
   - Use streaming for large datasets

3. **Response Time**
   - Use Vercel Analytics to monitor performance
   - Optimize heavy computations
   - Consider async processing for long tasks

## 🔄 Local Development

To test locally with Vercel:

```bash
# Install Vercel CLI
npm i -g vercel

# Install dependencies
pip install -r requirements-vercel.txt

# Run local development server
vercel dev
```

## 📈 Production Considerations

For production use, consider:

1. **Upgrading to Pro plan** for better performance and limits
2. **Using Vercel Postgres** for persistent data storage
3. **Adding monitoring** with Vercel Analytics
4. **Implementing rate limiting**
5. **Adding authentication** if needed
6. **Optimizing model size** for faster cold starts

## 🎉 Success!

Your Movie Sentiment Analyzer is now deployed on Vercel! 

- **🌐 Live URL**: `https://your-app.vercel.app`
- **📊 Analytics**: Available in Vercel dashboard
- **🔄 Auto Deploy**: Updates automatically on git push
- **⚡ Fast Performance**: Global CDN delivery

## 📞 Support

For issues with this deployment guide:

- **📖 Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **🚀 FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **🔧 Mangum Docs**: [mangum.io](https://mangum.io/)
- **🐛 GitHub Issues**: Report issues in the repository

---

**Happy Deploying! 🚀**
