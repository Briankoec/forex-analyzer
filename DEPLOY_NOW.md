# 🎯 Deploy Your Forex Analyzer in 5 Minutes!

Your app is ready to go live 24/7. Follow these EXACT steps:

---

## ⚡ FASTEST METHOD: Render.com (Recommended)

### Step 1: Create GitHub Account & Repo
1. Go to https://github.com/signup (2 minutes)
2. Click "Create a new repository"
3. Name it: `forex-analyzer`
4. Click "Create repository"

### Step 2: Push Your Code to GitHub
```bash
cd /workspaces/codespaces-blank
git remote add origin https://github.com/YOUR-USERNAME/forex-analyzer.git
git branch -M main
git push -u origin main
```

*(Replace `YOUR-USERNAME` with your GitHub username)*

### Step 3: Deploy to Render.com
1. Go to https://render.com/signup
2. Click "New" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Click "Connect GitHub"
5. Find and select `forex-analyzer` repo
6. Fill in these values:
   - **Name**: `forex-analyzer`
   - **Region**: Leave default
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && cd forex_analyzer && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `cd forex_analyzer && gunicorn forex_analyzer.wsgi:application`

7. Click "Advanced" and add Environment Variables:
   - Key: `DEBUG` | Value: `False`
   - Key: `SECRET_KEY` | Value: Generate at https://djecrety.ir/ (press refresh button)

8. Click "Create Web Service"

### Step 4: Wait for Deployment
- Render will automatically deploy (takes 2-5 minutes)
- You'll get a live URL like: `https://forex-analyzer.onrender.com`

---

## 🌐 YOUR APP WILL BE LIVE AT:

**You'll receive your live URL in the Render dashboard**

Example: `https://forex-analyzer-xxxx.onrender.com`

---

## 📋 Deployment Checklist

- ✅ Code ready to deploy
- ✅ Database configured
- ✅ Static files configured
- ✅ Procfile created
- ✅ Git repository initialized
- ✅ Requirements.txt updated
- ✅ Production settings enabled

---

## ❓ FAQ

**Q: Do I need a credit card?**
A: No! Render.com offers 750 free hours/month (enough for 24/7 for one app)

**Q: How do I update the app?**
A: Just push to GitHub (`git push origin main`) - Render auto-deploys!

**Q: Will the app be fast?**
A: Yes! Live charts from TradingView, data stored in database

**Q: Can I use it daily?**
A: Yes! It runs 24/7 on Render

---

## 🎬 After Deployment

1. **Visit your live app** - Use the URL from Render
2. **Add currency pairs** - Add EUR/USD, GBP/USD, etc.
3. **View real-time charts** - TradingView live charts work globally
4. **Check trading signals** - All indicators update automatically
5. **Share the URL** - Works on any device, anywhere

---

## 🔧 Need Help?

**Still have your local server running?**
- Homepage: http://localhost:8000
- Pair Detail: http://localhost:8000/pair/1
- Admin: http://localhost:8000/admin

**After deployment:**
- Visit your Render URL (https://your-app-name.onrender.com)
- Same features, available globally 24/7

---

## 📝 Important Notes

1. **First deploy takes 5-10 minutes** ⏳
2. **Choose strong SECRET_KEY from https://djecrety.ir/** 🔐
3. **Replace YOUR-USERNAME with your GitHub username** 👤
4. **Keep your SECRET_KEY private** 🤐

---

**Ready? Start with Step 1 above!** 🚀

Questions? Each platform has:
- Render support: https://render.com/support
- GitHub help: https://docs.github.com
- Django docs: https://docs.djangoproject.com
