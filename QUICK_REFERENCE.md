# Quick Reference Guide

## 🚀 Start Here

### First Time Setup
```bash
# Option 1: Automated (Recommended)
cd d:\Complaint-Routing-System
setup.bat              # Windows

# Option 2: Step by Step
# See SETUP_GUIDE.md
```

## ⚡ Quick Commands

### Backend
```bash
cd backend
venv\Scripts\activate              # Windows
source venv/bin/activate           # Mac/Linux

# Run development server
uvicorn app.main:app --reload

# Initialize database (first run)
python init_db.py

# Access API docs
# http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install                        # First time only
npm run dev                       # Development
npm run build                     # Production build
# http://localhost:5173
```

## 🔐 Test Credentials

### Student Login
```
Email: test@karunya.edu.in (or any @karunya.edu.in)
Password: any password
```

### Faculty Login
```
Email: cse@karunya.edu
Password: admin123

Other departments:
- it@karunya.edu
- electrical@karunya.edu
- plumbing@karunya.edu
- administration@karunya.edu
```

## 📚 Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI main app |
| `backend/app/models.py` | Database models |
| `backend/app/nlp/classifier.py` | NLP classifier |
| `frontend/src/App.jsx` | React main component |
| `frontend/src/pages/StudentDashboard.jsx` | Student view |
| `frontend/src/pages/FacultyDashboard.jsx` | Faculty view |

## 🔧 Troubleshooting

### Port in use?
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Database error?
```bash
# Reset database
rm backend/complaint_routing.db
python backend/init_db.py
```

### Module not found?
```bash
# Activate virtual environment first!
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
```

## 📱 Test Workflow

### As Student:
1. Go to http://localhost:5173
2. Click "Student" tab
3. Click "Register"
4. Enter email like `john@karunya.edu.in`
5. Enter any password
6. Submit
7. Click "Submit New Complaint"
8. Type complaint like "WiFi is slow"
9. Click "Track Complaint" to see status

### As Faculty:
1. Go to http://localhost:5173
2. Click "Faculty" tab
3. Enter `cse@karunya.edu` / `admin123`
4. Click on a complaint
5. Click "Mark as Read"
6. Type response
7. Click "Send Reply"
8. Click "Mark as Resolved"

## 🎯 NLP Auto-Routing Examples

| Complaint | Routes To |
|-----------|-----------|
| "WiFi not working" | IT |
| "Computer lab down" | CSE |
| "Water leak" | Plumbing |
| "Lights broken" | Electrical |
| "Certificate delayed" | Administration |

## 📊 Database Reset

```bash
# If database is corrupted:
1. Delete: backend/complaint_routing.db
2. Run: python backend/init_db.py
3. Restart backend and frontend
```

## 🔗 Important URLs

| URL | Purpose |
|-----|---------|
| http://localhost:5173 | Frontend app |
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | API documentation |
| http://localhost:8000/health | Health check |

## 📝 Environment Variables

### Backend `.env` (Optional)
```
DATABASE_TYPE=sqlite
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend `.env`
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Smart Complaint Routing System
```

## 🆘 Common Issues

### "Module not found" error
→ Activate virtual environment: `venv\Scripts\activate`

### Database locked error
→ Delete `.db` file and reinitialize

### Frontend won't connect to backend
→ Check backend is running on port 8000

### Can't register student
→ Email must end with `@karunya.edu.in`

## 📖 Documentation

- **SETUP_GUIDE.md** - Detailed installation steps
- **DEPLOYMENT.md** - Production deployment
- **README.md** - Project overview
- **IMPLEMENTATION_SUMMARY.md** - What was built

## ✅ Checklist

Before using in production:
- [ ] Change SECRET_KEY in backend/.env
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set HTTPS in frontend
- [ ] Configure email notifications (optional)
- [ ] Set up backup system
- [ ] Configure rate limiting
- [ ] Set up monitoring
- [ ] Create admin interface (optional)

## 🚀 Next Steps

1. **Explore the code** - Understand architecture
2. **Customize** - Modify for your needs
3. **Deploy** - Use DEPLOYMENT.md guide
4. **Add features** - Implement email, SMS, etc.

## 📞 Support

For questions:
1. Check SETUP_GUIDE.md
2. Review README.md
3. Check API docs at `/docs`
4. Read IMPLEMENTATION_SUMMARY.md

---

**Need help? Read the docs! 📚**
