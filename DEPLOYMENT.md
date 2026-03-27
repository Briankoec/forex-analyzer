# 🚀 Forex Analyzer - Deploy to Cloud

Your app is ready to deploy publicly! Here are 3 easy deployment options:

## Option 1: Deploy to Render.com (RECOMMENDED - Easiest)

### Steps:
1. **Sign up** at https://render.com (free account)
2. **Connect GitHub**:
   - In Render dashboard, click "New" → "Web Service"
   - Select "Build and deploy from a Git repository"
   - Connect your GitHub account
   - Select this repository

3. **Configure**:
   - Name: `forex-analyzer`
   - Region: Choose closest to you
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt && cd forex_analyzer && python manage.py collectstatic --noinput`
   - Start Command: `cd forex_analyzer && gunicorn forex_analyzer.wsgi:application`

4. **Environment Variables** (Add these in Render dashboard):
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate one at https://djecrety.ir/

5. **Deploy!** - Render will automatically deploy from your GitHub repo

---

## Option 2: Deploy to Railway.app (Also FREE)

### Steps:
1. Sign up: https://railway.app
2. Connect GitHub
3. New Project → Use Railway starter template
4. Add environment variables same as above
5. Deploy!

---

## Option 3: Deploy to Heroku (Requires Credit Card)

### Steps:
1. Create account at https://www.heroku.com
2. Install Heroku CLI: 
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```
3. Login:
   ```bash
   heroku login
   ```
4. Create app:
   ```bash
   heroku create your-forex-analyzer-app
   ```
5. Set environment variables:
   ```bash
   heroku config:set DEBUG=False SECRET_KEY=your-secret-key
   ```
6. Deploy:
   ```bash
   git push heroku main
   ```

---

## Quick Setup for GitHub Push

1. **Initialize Git** (if not already done):
   ```bash
   cd /workspaces/codespaces-blank
   git init
   git add .
   git commit -m "Initial Forex Analyzer commit"
   ```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Create new repo (name: `forex-analyzer`)
   - Copy the git commands shown

3. **Push Code**:
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/forex-analyzer.git
   git branch -M main
   git push -u origin main
   ```

4. **Connect to Render/Railway** - Use GitHub integration

---

## Testing Locally Before Deploy

```bash
cd /workspaces/codespaces-blank/forex_analyzer
python manage.py runserver 0.0.0.0:8000
```

Visit: http://localhost:8000

---

## After Deployment

1. Your app will be live at: `https://your-app-name.onrender.com`
2. Access via browser
3. Use daily - it's always available!
4. App automatically restarts each day (free tier behavior)

---

## Troubleshooting

**Blank Page?**
- Check logs in Render/Railway dashboard
- Ensure database migrations ran
- Check environment variables are set

**CSS/JS Not Loading?**
- Run: `python manage.py collectstatic`
- Ensure STATIC_ROOT is set correctly

**Need Help?**
- Render docs: https://render.com/docs
- Railway docs: https://docs.railway.app
- Heroku docs: https://devcenter.heroku.com

---

**Your app will be publicly accessible 24/7 after deployment!** 🌐
