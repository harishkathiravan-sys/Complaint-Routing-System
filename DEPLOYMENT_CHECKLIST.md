# Deployment Checklist - Vercel + Render

Quick checklist to deploy your Smart Complaint Routing System to production.

## Preparation Phase

- [ ] Create GitHub account (if not already done)
- [ ] Create Vercel account (https://vercel.com)
- [ ] Create Render account (https://render.com)
- [ ] Clone entire project as two separate repositories:
  - `complaint-routing-backend`
  - `complaint-routing-frontend`

## Backend Deployment (Render)

### Local Preparation

- [ ] Navigate to `backend/` directory
- [ ] Verify `requirements.txt` has all dependencies
- [ ] Verify `Procfile` exists
- [ ] Verify `render.yaml` exists
- [ ] Update `.env` with production values:
  - [ ] `DATABASE_TYPE=postgresql`
  - [ ] `SECRET_KEY` (generate a strong key!)
  - [ ] `ALLOWED_ORIGINS` (leave blank for now)

### GitHub Setup

- [ ] Initialize git in backend folder: `git init`
- [ ] Create GitHub repository: `complaint-routing-backend`
- [ ] Add remote: `git remote add origin https://github.com/your-username/complaint-routing-backend`
- [ ] Add all files: `git add .`
- [ ] Commit: `git commit -m "Initial backend setup"`
- [ ] Push: `git push -u origin main`

### Render Deployment

- [ ] Log in to Render dashboard
- [ ] Create PostgreSQL database:
  - [ ] Click "New +" → "PostgreSQL"
  - [ ] Name: `complaint-routing-db`
  - [ ] Copy database URL (you'll need this next)
- [ ] Create Web Service:
  - [ ] Click "New +" → "Web Service"
  - [ ] Connect to your `complaint-routing-backend` GitHub repo
  - [ ] Name: `complaint-routing-api`
  - [ ] Environment: Python 3
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add Environment Variables:
  - [ ] `DATABASE_TYPE`: `postgresql`
  - [ ] `DATABASE_URL`: Paste the PostgreSQL URL
  - [ ] `SECRET_KEY`: Generate and paste a strong key
  - [ ] `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
  - [ ] `ALLOWED_ORIGINS`: `http://localhost:5173` (update after Vercel deployment)
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (5-10 minutes)
- [ ] Copy the API URL: `https://complaint-routing-api.onrender.com` (or your custom URL)

## Frontend Deployment (Vercel)

### Local Preparation

- [ ] Navigate to `frontend/` directory
- [ ] Update `.env`:
  ```
  VITE_API_URL=https://complaint-routing-api.onrender.com
  ```
- [ ] Verify `vercel.json` exists
- [ ] Verify `.vercelignore` exists
- [ ] Test build locally: `npm run build`
  - [ ] Check for build errors
  - [ ] Verify `dist/` folder created

### GitHub Setup

- [ ] Initialize git in frontend folder: `git init`
- [ ] Create GitHub repository: `complaint-routing-frontend`
- [ ] Add remote: `git remote add origin https://github.com/your-username/complaint-routing-frontend`
- [ ] Add all files: `git add .`
- [ ] Commit: `git commit -m "Initial frontend setup"`
- [ ] Push: `git push -u origin main`

### Vercel Deployment

- [ ] Log in to Vercel dashboard
- [ ] Click "Add New" → "Project"
- [ ] Import `complaint-routing-frontend` repository
- [ ] Project Settings:
  - [ ] Framework: React
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `dist`
- [ ] Add Environment Variables:
  - [ ] `VITE_API_URL`: `https://complaint-routing-api.onrender.com`
- [ ] Click "Deploy"
- [ ] Wait for deployment (2-5 minutes)
- [ ] Copy the frontend URL: `https://your-app.vercel.app`

## Post-Deployment Configuration

- [ ] Test frontend loads: Visit `https://your-app.vercel.app`
- [ ] Test student login with demo credentials:
  - [ ] Email: `demo@karunya.edu.in`
  - [ ] Password: `student123`
- [ ] Check browser console for CORS errors
- [ ] If CORS errors, update Render `ALLOWED_ORIGINS`:
  - [ ] Go to Render dashboard
  - [ ] Update `ALLOWED_ORIGINS`: `https://your-app.vercel.app`
  - [ ] Service will auto-redeploy
- [ ] Test faculty login: `cse@karunya.edu / admin123`
- [ ] Test complaint submission and routing

## Optional: Custom Domain Setup

### Domain Registration

- [ ] Register domain (e.g., `complaints.karunya.edu`)
- [ ] Get domain nameservers/DNS settings

### Vercel Custom Domain

- [ ] Go to Vercel Project Settings → Domains
- [ ] Add domain: `complaints.karunya.edu`
- [ ] Follow DNS configuration steps
- [ ] Update `ALLOWED_ORIGINS` in Render (add domain)

### Render Custom Domain (Optional)

- [ ] Go to Render Service Settings → Custom Domain
- [ ] Add domain: `api.complaints.karunya.edu`
- [ ] Follow DNS configuration steps

## Auto-Deployment Testing

- [ ] Make a small change to frontend (e.g., fix typo)
- [ ] Commit: `git add . && git commit -m "Test auto-deploy"`
- [ ] Push: `git push origin main`
- [ ] Verify deployment in Vercel dashboard (should auto-deploy)
- [ ] Check live site for the change

- [ ] Make a small change to backend (e.g., update comment)
- [ ] Commit: `git add . && git commit -m "Test auto-deploy"`
- [ ] Push: `git push origin main`
- [ ] Verify deployment in Render dashboard (should auto-deploy)

## Monitoring & Maintenance

- [ ] Set up error tracking (Sentry - optional)
- [ ] Monitor Render logs weekly
- [ ] Monitor Vercel analytics monthly
- [ ] Update dependencies regularly: `npm update`, `pip install --upgrade -r requirements.txt`
- [ ] Backup database regularly (Render provides auto-backups on paid plans)
- [ ] Monitor usage and upgrade plan if needed

## Security Hardening

- [ ] Verify `SECRET_KEY` is strong (50+ characters)
- [ ] Ensure database credentials are in environment variables (not in code)
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Set up rate limiting (optional)
- [ ] Enable database backups
- [ ] Monitor for suspicious activity

## Troubleshooting Reference

**Frontend won't load:**
- Check Vercel deployment logs
- Verify `NODE_ENV` is not set to incompatible value
- Check for build errors: `npm run build`

**Can't connect to API:**
- Check `VITE_API_URL` in Vercel env vars
- Check backend is running: Visit `/health` endpoint
- Check `ALLOWED_ORIGINS` in Render includes frontend URL
- Check browser console for CORS errors

**Database errors:**
- Verify `DATABASE_URL` is correct in Render
- Test connection locally if possible
- Check database is running in Render

**Build failures:**
- Pull latest code and test locally
- Check for missing environment variables
- Check for new dependency requirements

---

## Deployment Summary

| Component | Service | URL | Status |
|-----------|---------|-----|--------|
| Frontend | Vercel | `https://your-app.vercel.app` | ✓ |
| Backend API | Render | `https://complaint-api.onrender.com` | ✓ |
| Database | Render PostgreSQL | Internal | ✓ |
| Custom Domain | DNS | `complaints.karunya.edu` | ⬜ |

---

## Quick Commands Reference

```bash
# Clone and setup locally
git clone https://github.com/your-username/complaint-routing-backend
git clone https://github.com/your-username/complaint-routing-frontend

# Backend - test before deployment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload

# Frontend - test before deployment  
cd frontend
npm install
npm run dev
# Visit http://localhost:5173

# Deploy changes
cd backend
git add . && git commit -m "Your message" && git push

cd ../frontend
git add . && git commit -m "Your message" && git push
```

---

**Need Help?**
- Vercel Support: https://vercel.com/support
- Render Support: https://render.com/support
- Project Issues: Check GitHub Actions logs

**Last Updated:** April 2026
