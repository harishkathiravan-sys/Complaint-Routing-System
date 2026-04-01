# Deployment Configuration Files

This directory contains all necessary configuration files for deploying the Smart Complaint Routing System.

## 📁 Files Overview

### Backend Configuration

| File | Purpose | Location |
|------|---------|----------|
| `Procfile` | Render deployment entry point | `backend/` |
| `render.yaml` | Render infrastructure definition | `backend/` |
| `requirements.txt` | Python dependencies | `backend/` |
| `.env.example` | Environment variable template | `backend/` |

**Example Procfile:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### Frontend Configuration

| File | Purpose | Location |
|------|---------|----------|
| `vercel.json` | Vercel deployment config | `frontend/` |
| `.vercelignore` | Files to ignore in Vercel | `frontend/` |
| `package.json` | npm dependencies & scripts | `frontend/` |
| `.env` | Environment variables | `frontend/` |
| `.env.example` | Environment variable template | `frontend/` |

**Example vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

---

## 🚀 Quick Deployment Steps

### For Vercel + Render (Recommended)

1. **Backend Deployment (Render)**
   ```bash
   # 1. Create Render account
   # 2. Create PostgreSQL database
   # 3. Deploy backend from GitHub
   # 4. Set DATABASE_URL environment variable
   ```

2. **Frontend Deployment (Vercel)**
   ```bash
   # 1. Create Vercel account
   # 2. Import frontend GitHub repo
   # 3. Set VITE_API_URL to Render backend URL
   # 4. Deploy
   ```

3. **Configure CORS**
   ```
   Update Render environment:
   ALLOWED_ORIGINS=https://your-app.vercel.app
   ```

---

## 📋 Environment Variables

### Backend (`backend/.env`)

```env
# Database
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@host:5432/db

# Security
SECRET_KEY=generate-strong-key-here

# Server
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000

# CORS
ALLOWED_ORIGINS=https://your-app.vercel.app,https://custom-domain.com
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=https://complaint-routing-api.onrender.com
VITE_APP_NAME=Smart Complaint Routing System
```

---

## 🔄 Deployment Workflow

```
Git Push to GitHub
        ↓
[Frontend] Vercel Auto-Deploy → https://yourapp.vercel.app
        
[Backend] Render Auto-Deploy → https://api.yourapp.com
        ↓
PostgreSQL Database (Render)
```

**Auto-deployment is automatic!** Just push code to GitHub.

---

## 📄 Detailed Guides

- **[VERCEL_DEPLOYMENT_GUIDE.md](../VERCEL_DEPLOYMENT_GUIDE.md)** - Full step-by-step Vercel + Render deployment
- **[DATABASE_MIGRATION_GUIDE.md](../DATABASE_MIGRATION_GUIDE.md)** - SQLite → PostgreSQL migration
- **[DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md)** - Pre-deployment checklist
- **[SETUP_GUIDE.md](../SETUP_GUIDE.md)** - Local development setup
- **[DEPLOYMENT.md](../DEPLOYMENT.md)** - General deployment info

---

## ✅ Deployment Checklist

- [ ] Create GitHub accounts for repos (frontend & backend)
- [ ] Create Vercel account
- [ ] Create Render account
- [ ] Create PostgreSQL database on Render
- [ ] Push backend to GitHub
- [ ] Deploy backend on Render
- [ ] Update backend `ALLOWED_ORIGINS`
- [ ] Push frontend to GitHub
- [ ] Deploy frontend on Vercel
- [ ] Set `VITE_API_URL` in Vercel
- [ ] Test login with demo credentials
- [ ] Test complaint submission
- [ ] (Optional) Configure custom domain

---

## 🔐 Security Notes

### Before Deployment

- [ ] Change `SECRET_KEY` (50+ random characters)
- [ ] Ensure no credentials in code (use `.env` only)
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Configure CORS properly (not `*` in production)
- [ ] Database backups enabled (Render paid plans)

### Production Checklist

- [ ] Use strong passwords
- [ ] Enable 2FA on hosting accounts
- [ ] Monitor logs regularly
- [ ] Set up error tracking (optional)
- [ ] Implement rate limiting (optional)
- [ ] Regular security updates

---

## 💰 Cost Breakdown

### Free Tier (Development/Testing)

| Service | Free Limits | Cost |
|---------|-------------|------|
| Vercel | 100GB/month bandwidth | Free |
| Render | 750 hours/month runtime | Free |
| PostgreSQL | 256MB storage, 1 database | Free |
| **Total** | - | **Free** |

### Paid Tier (Production)

Estimated costs for 1000+ monthly users:

| Service | Plan | Cost/month |
|---------|------|-----------|
| Vercel | Pro | $20 |
| Render | Paid Web Service | $10-50 |
| PostgreSQL | Paid Database | $15-100 |
| **Total** | - | **~$50-170/month** |

---

## 🆘 Troubleshooting

### Frontend Can't Connect to Backend

```
Error: CORS error or 'API unreachable'
```

**Fix:**
1. Check `VITE_API_URL` in Vercel environment
2. Check Render `ALLOWED_ORIGINS` includes frontend URL
3. Verify backend is running: `https://api-url.onrender.com/health`
4. Check browser console for exact error

### Database Connection Failed

```
Error: 'could not connect to server'
```

**Fix:**
1. Verify `DATABASE_URL` is correct
2. Check PostgreSQL database exists
3. Verify credentials are correct
4. Check firewall/network access

### Build Failures

**Frontend:**
```bash
npm run build  # Test locally first
```

**Backend:**
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app
```

---

## 📚 External Resources

- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## 🎯 Next Steps

1. ✅ Review deployment guides
2. ⬜ Set up GitHub repositories (2)
3. ⬜ Create Vercel account
4. ⬜ Create Render account
5. ⬜ Deploy backend on Render
6. ⬜ Deploy frontend on Vercel
7. ⬜ Configure CORS
8. ⬜ Test production environment
9. ⬜ (Optional) Set up custom domain
10. ⬜ Monitor and maintain

---

**Status:** Ready for Production Deployment 🚀

Last Updated: April 2026
