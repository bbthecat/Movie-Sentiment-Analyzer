# Deploy to Render

This guide will help you deploy the Movie Sentiment Analyzer to Render.

## Prerequisites

1. A Render account (free tier available)
2. API keys for OMDb and TMDb services

## Step 1: Get API Keys

### OMDb API Key
1. Go to [OMDb API](http://www.omdbapi.com/apikey.aspx)
2. Sign up for a free API key
3. Copy your API key

### TMDb API Key
1. Go to [TMDb API](https://www.themoviedb.org/settings/api)
2. Create an account and request an API key
3. Copy your API key

## Step 2: Deploy to Render

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables**
   - In the Render dashboard, go to your service
   - Navigate to "Environment" tab
   - Add the following environment variables:
     - `OMDB_API_KEY`: Your OMDb API key
     - `TMDB_API_KEY`: Your TMDb API key

4. **Deploy**
   - Click "Deploy" and wait for the build to complete
   - Your app will be available at the provided URL

### Option 2: Manual Setup

1. **Create a new Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service**
   - **Name**: `movie-sentiment-analyzer`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - `OMDB_API_KEY`: Your OMDb API key
   - `TMDB_API_KEY`: Your TMDb API key
   - `HF_MODEL_NAME`: `distilbert-base-uncased-finetuned-sst-2-english`
   - `DATA_DIR`: `backend/data`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for the deployment to complete

## Step 3: Test Your Deployment

1. Visit your deployed URL
2. Check the health endpoint: `https://your-app.onrender.com/api/health`
3. Test the API documentation: `https://your-app.onrender.com/docs`

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OMDB_API_KEY` | OMDb API key for movie data | Yes | - |
| `TMDB_API_KEY` | TMDb API key for reviews | Yes | - |
| `HF_MODEL_NAME` | Hugging Face model name | No | `distilbert-base-uncased-finetuned-sst-2-english` |
| `DATA_DIR` | Data directory path | No | `backend/data` |

## Free Tier Limitations

- **Sleep Mode**: Free tier services sleep after 15 minutes of inactivity
- **Build Time**: 90 minutes per month
- **Bandwidth**: 100GB per month
- **Memory**: 512MB RAM

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is compatible

2. **Service Won't Start**
   - Verify the start command is correct
   - Check environment variables are set

3. **API Keys Not Working**
   - Ensure API keys are correctly set in environment variables
   - Verify API keys are valid and active

4. **Slow Cold Starts**
   - This is normal for free tier due to sleep mode
   - Consider upgrading to paid plan for better performance

### Getting Help

- Check Render logs in the dashboard
- Review the application logs for errors
- Ensure all required environment variables are set

## Production Considerations

For production use, consider:

1. **Upgrading to a paid plan** for better performance
2. **Setting up a database** for persistent data storage
3. **Adding monitoring and logging**
4. **Implementing rate limiting**
5. **Adding authentication** if needed

## API Endpoints

Once deployed, your API will be available at:

- **Health Check**: `GET /api/health`
- **API Documentation**: `GET /docs`
- **Movie Search**: `GET /api/movies/search?query={query}`
- **Movie Details**: `GET /api/movies/{imdb_id}`
- **Analyze Reviews**: `POST /api/analyze/{imdb_id}`
- **Get Summary**: `GET /api/summary/{imdb_id}`
- **Single Text Analysis**: `POST /api/analyze-text`

## Support

For issues with this deployment guide, please check:
- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- Project README.md for application-specific information
