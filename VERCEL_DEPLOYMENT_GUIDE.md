# Vercel + Render Deployment Guide

Complete guide to deploy the Smart Complaint Routing System using Vercel for frontend and Render for backend.

## Architecture Overview

```
Students/Faculty Browser
        |
        v
Vercel (React Frontend)
  (https://your-app.vercel.app)
        |
        v
Render/Railway (FastAPI Backend)
  (https://complaint-api.onrender.com)
        |
        v
PostgreSQL Database (Render)
```

## Prerequisites

- GitHub account (for auto-deployment)
- Vercel account (https://vercel.com)
- Render account (https://render.com) or Railway account
- PostgreSQL database on Render/Railway
- Git installed locally

---

## Step 1: Prepare Backend for Render

### 1.1 Create `requirements.txt` (Already Done ✓)

Make sure `backend/requirements.txt` includes all dependencies:
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic[email]==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
bcrypt==4.0.1
```

### 1.2 Create `backend/Procfile`

Create a `Procfile` in the backend directory for Render deployment:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 1.3 Create `backend/render.yaml`

Create a configuration file for Render deployment:

```yaml
services:
  - type: web
    name: complaint-routing-api
    env: python
    region: singapore # or your preferred region
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_TYPE
        value: postgresql
      - key: ALLOWED_ORIGINS
        scope: run,build
      - key: SECRET_KEY
        scope: run,build
        isFile: false
```

### 1.4 Update Backend `.env` for Production

Create `.env` file for backend with production values:

```
# Production Database
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://username:password@host:5432/complaint_routing_db

# Security - Generate a strong key!
SECRET_KEY=generate-a-strong-random-key-here

# Token
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Allow Vercel frontend
ALLOWED_ORIGINS=https://your-app.vercel.app,https://complaints.karunya.edu

# Server
UVICORN_HOST=0.0.0.0
```

---

## Step 2: Push Backend to GitHub

### 2.1 Initialize Git (if not already done)

```bash
cd backend
git init
git add .
git commit -m "Initial backend setup for Render deployment"
```

### 2.2 Add Remote GitHub Repository

```bash
git remote add origin https://github.com/your-username/complaint-routing-backend.git
git push -u origin main
```

---

## Step 3: Deploy Backend on Render

### 3.1 Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Connect your GitHub account

### 3.2 Create PostgreSQL Database

1. In Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Fill in database details:
   - Name: `complaint-routing-db`
   - Plan: Free tier (for testing)
4. Click **"Create Database"**
5. Copy the database URL (looks like `postgresql://...`)

### 3.3 Deploy Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repository (backend)
3. Fill in details:
   - **Name**: `complaint-routing-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `DATABASE_TYPE`: `postgresql`
   - `DATABASE_URL`: Paste the PostgreSQL URL from step 3.2
   - `SECRET_KEY`: Generate a strong random key
   - `ALLOWED_ORIGINS`: `https://your-app.vercel.app` (we'll update this after Vercel deployment)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

5. Click **"Create Web Service"**
6. Wait for deployment to complete (5-10 minutes)
7. Copy the URL: `https://complaint-routing-api.onrender.com`

---

## Step 4: Prepare Frontend for Vercel

### 4.1 Create `.env.local` for Development

In `frontend/.env`:

```
VITE_API_URL=https://complaint-routing-api.onrender.com
VITE_APP_NAME=Smart Complaint Routing System
```

### 4.2 Create `.env.production` for Production

In `frontend/.env.production`:

```
VITE_API_URL=https://complaint-routing-api.onrender.com
VITE_APP_NAME=Smart Complaint Routing System
```

### 4.3 Verify API Configuration

Check `src/services/api.js` uses environment variables:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### 4.4 Create `frontend/vercel.json`

Create configuration for Vercel:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "headers": [
    {
      "source": "/api/:path*",
      "headers": [
        {
          "key": "Access-Control-Allow-Credentials",
          "value": "true"
        },
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET,OPTIONS,PATCH,DELETE,POST,PUT"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization"
        }
      ]
    }
  ]
}
```

### 4.5 Create `frontend/.vercelignore`

```
README.md
.gitignore
.DS_Store
backend/
node_modules/
.env
.env.local
.git
```

---

## Step 5: Push Frontend to GitHub

```bash
cd frontend
git init
git add .
git commit -m "Initial frontend setup for Vercel deployment"
git remote add origin https://github.com/your-username/complaint-routing-frontend.git
git push -u origin main
```

---

## Step 6: Deploy Frontend on Vercel

### 6.1 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Connect your GitHub account

### 6.2 Import Frontend Repository

1. Click **"Add New"** → **"Project"**
2. Select your frontend GitHub repository
3. Fill in project details:
   - **Project Name**: `complaint-routing-frontend`
   - **Framework**: React
   - **Root Directory**: `./` (or `frontend/` if in monorepo)

### 6.3 Add Environment Variables

1. Go to **Project Settings** → **Environment Variables**
2. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://complaint-routing-api.onrender.com`
   - **Environments**: Production, Preview, Development

### 6.4 Deploy

1. Click **"Deploy"**
2. Wait for deployment (2-5 minutes)
3. Copy the deployment URL: `https://your-app.vercel.app`

---

## Step 7: Update Backend CORS

### 7.1 Update Render Environment Variables

1. Go to your Render service dashboard
2. Click **"Environment"** 
3. Update `ALLOWED_ORIGINS`:
   ```
   https://your-app.vercel.app,https://complaints.karunya.edu
   ```
4. Click **"Save"**
5. Service will redeploy automatically

---

## Step 8: Set Up Custom Domain (Optional)

### 8.1 Frontend Custom Domain

1. In Vercel, go to **Project Settings** → **Domains**
2. Add your custom domain: `complaints.karunya.edu`
3. Follow DNS instructions
4. Update `ALLOWED_ORIGINS` in Render backend

### 8.2 Backend Custom Domain

Similar process in Render dashboard for API subdomain.

---

## Step 9: Auto-Deployment Setup

### 9.1 GitHub Webhook (Automatic)

Both Vercel and Render automatically create GitHub webhooks, so:

**Frontend Auto-Deploy:**
```bash
cd frontend
git add .
git commit -m "Update complaint form"
git push origin main
# Vercel automatically rebuilds and deploys!
```

**Backend Auto-Deploy:**
```bash
cd backend
git add .
git commit -m "Fix complaint routing"
git push origin main
# Render automatically rebuilds and deploys!
```

---

## Step 10: Database Setup

### 10.1 Initialize Production Database

1. Connect to Render PostgreSQL from local machine using `psql`
2. Run SQL schema:

```bash
psql $DATABASE_URL < database/schema.sql
```

### 10.2 Initialize Default Data

Create a script to run on first deployment:

```bash
python init_db.py
```

---

## Troubleshooting

### Frontend can't connect to Backend

**Symptoms**: Login fails, API errors in console

**Solutions**:
1. Check `VITE_API_URL` in Vercel environment variables
2. Check backend `ALLOWED_ORIGINS` includes frontend URL
3. Verify backend service is running on Render
4. Check browser console for CORS errors

### Database Connection Error

**Symptoms**: 500 errors on request

**Solutions**:
1. Verify `DATABASE_URL` is correct in Render
2. Check database exists and is running
3. Verify schema is initialized
4. Check network connectivity from backend to database

### Build Failures

**Frontend**:
```bash
# Check build locally
npm run build

# Check logs in Vercel dashboard
```

**Backend**:
```bash
# Check logs in Render dashboard
# Pull latest code and test locally
```

---

## Monitoring

### Vercel Analytics

Go to **Analytics** tab in Vercel to view:
- Page load times
- Core Web Vitals
- Traffic patterns

### Render Logs

View backend logs:
1. Go to Render service dashboard
2. Click **"Logs"** tab
3. Filter by date/level

---

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Use strong database password
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Configure CORS properly
- [ ] Use environment variables for sensitive data
- [ ] Enable database backups on Render
- [ ] Monitor logs for errors
- [ ] Set up error tracking (e.g., Sentry)

---

## Cost Estimates (Free Tier)

| Service | Free Tier | Cost |
|---------|-----------|------|
| Vercel Frontend | 100GB bandwidth/month | Free |
| Render Backend | 750 hours/month | Free |
| PostgreSQL | 256MB storage | Free |
| **Total** | - | **Free** |

> Upgrade to paid plans as you scale!

---

## Next Steps

1. ✅ Deploy backend on Render
2. ✅ Deploy frontend on Vercel
3. ⬜ Configure custom domain
4. ⬜ Set up monitoring
5. ⬜ Configure backups
6. ⬜ Set up error tracking
7. ⬜ Implement rate limiting
8. ⬜ Add analytics

---

## Support Resources

- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Railway Alternative: https://railway.app/docs

---

**Happy Deploying! 🚀**
