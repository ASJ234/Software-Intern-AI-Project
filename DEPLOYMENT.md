# Deployment Guide - Regulatory Report Assistant

## Backend Deployment (Django)

### Option 1: Railway
1. **Create Railway account** and connect GitHub repository
2. **Add environment variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   ```
3. **Deploy**: Railway will automatically detect Django and deploy

### Option 2: Render
1. **Create Render account** and connect GitHub repository
2. **Create Web Service** with:
   - Build Command: `pip install -r requirements.txt && python setup.py`
   - Start Command: `python manage.py runserver 0.0.0.0:$PORT`
3. **Add environment variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com
   ```

### Option 3: Heroku
1. **Install Heroku CLI** and login
2. **Create Heroku app**: `heroku create your-app-name`
3. **Add buildpacks**:
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
   ```
4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   ```
5. **Deploy**: `git push heroku main`

## Frontend Deployment (React)

### Option 1: Vercel
1. **Connect GitHub repository** to Vercel
2. **Set environment variables**:
   ```
   REACT_APP_API_URL=https://your-backend-url.com/api
   ```
3. **Deploy**: Automatic deployment on push

### Option 2: Netlify
1. **Connect GitHub repository** to Netlify
2. **Build settings**:
   - Build command: `npm run build`
   - Publish directory: `build`
3. **Environment variables**:
   ```
   REACT_APP_API_URL=https://your-backend-url.com/api
   ```
4. **Deploy**: Automatic deployment on push

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=sqlite:///./db.sqlite3
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://your-backend-url.com/api
REACT_APP_ENV=production
```

## Testing Deployment

1. **Test backend endpoints**:
   ```bash
   curl https://your-backend-url.com/api/
   curl -X POST https://your-backend-url.com/api/process-report/ \
     -H "Content-Type: application/json" \
     -d '{"report": "Patient experienced severe nausea after taking Drug X. Patient recovered."}'
   ```

2. **Test frontend**: Visit your frontend URL and test the interface

## Troubleshooting

### Common Issues
1. **CORS errors**: Update `CORS_ALLOWED_ORIGINS` in Django settings
2. **Database issues**: Ensure migrations are run in production
3. **Static files**: Configure static file serving for production
4. **Environment variables**: Verify all required variables are set

### Logs
- **Railway**: View logs in Railway dashboard
- **Render**: View logs in Render dashboard
- **Heroku**: `heroku logs --tail`
- **Vercel**: View logs in Vercel dashboard
- **Netlify**: View logs in Netlify dashboard
