# Smart Complaint Routing System - Setup & Running Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Running the System](#running-the-system)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you start, ensure you have installed:

- **Python 3.8 or higher**
  ```bash
  python --version  # Check version
  ```

- **Node.js 16+ and npm**
  ```bash
  node --version
  npm --version
  ```

- **Git** (optional, for cloning)
  ```bash
  git --version
  ```

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in terminal.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- python-jose (JWT)
- passlib (Password hashing)
- And other dependencies

### Step 4: Configure Environment

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` file (optional for local development):
```
DATABASE_TYPE=sqlite
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
UVICORN_PORT=8000
```

For SQLite (default), no additional configuration needed.

### Step 5: Initialize Database

```bash
python init_db.py
```

You should see:
```
Creating database tables...
✓ Tables created successfully
Initializing departments...
✓ Created department: CSE
✓ Created department: IT
✓ Created department: ELECTRICAL
✓ Created department: PLUMBING
✓ Created department: ADMINISTRATION
...
✓ Database initialized successfully!

Default credentials for testing:
Faculty Login:
  Email: cse@karunya.edu
  Password: admin123
  ...
```

A file `complaint_routing.db` will be created.

### Step 6: Run Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

Or:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Visit `http://localhost:8000/docs` to see API documentation.

## Frontend Setup

### Step 1: Open New Terminal (Keep Backend Running)

Keep the previous terminal running with backend, open a new terminal.

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Dependencies

```bash
npm install
```

This installs:
- react
- react-dom
- axios
- react-router-dom
- tailwindcss
- vite
- And other dependencies

### Step 4: Configure Environment

Check `.env` file:
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Smart Complaint Routing System
```

No changes needed for local development (defaults already work).

### Step 5: Run Frontend Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

## Running the System

Now you have:
- ✅ Backend running on `http://localhost:8000`
- ✅ Frontend running on `http://localhost:5173`

### Access the Application

Open your browser and go to: `http://localhost:5173`

You should see the login page.

## Testing

### Create Test Student Account

1. Click **"Student"** tab on login page
2. Click **"Register"**
3. Fill in:
   - Email: `test@karunya.edu.in`
   - Password: `Test@123` (any password)
   - Full Name: `Test Student`
4. Click **Register**
5. You're logged in! 🎉

### Test Faculty Account

1. Click **"Faculty"** tab on login page
2. Enter:
   - Email: `cse@karunya.edu`
   - Password: `admin123`
3. Click **Login**
4. You're logged in as CSE Faculty! 🎉

### Test Complaint Submission (Student)

1. Login as student
2. Click **"Submit New Complaint"**
3. Enter:
   - Complaint: "WiFi in hostel is very slow and unreliable"
4. Click **"Submit Complaint"** (min 10 characters)
5. You'll see successful submission with complaint ID
6. Click **"Track Complaint"** to see status

### Test Complaint Management (Faculty)

1. Login as faculty (`cse@karunya.edu`)
2. You'll see complaints routed to your department
3. Click on a complaint to open details
4. Try:
   - **Mark as Read**: Acknowledges the complaint
   - **Send Reply**: Send response to student
   - **Mark as Resolved**: Close the complaint

### Test Auto-Routing

Submit different complaints to see auto-routing:

- **IT**: "WiFi is not working"
- **CSE**: "Computer lab systems are down"
- **ELECTRICAL**: "Lights in classroom are off"
- **PLUMBING**: "Water leakage in bathroom"
- **ADMINISTRATION**: "Certificate approval pending"

## Troubleshooting

### Issue: Port Already in Use

If you get "port already in use" error:

**For Backend (Port 8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

Then run backend on different port:
```bash
uvicorn app.main:app --port 8001
```

And update frontend `.env`:
```
VITE_API_URL=http://localhost:8001
```

**For Frontend (Port 5173):**
```bash
npm run dev -- --port 5174
```

### Issue: Database Error

If you see database errors:

1. Delete `complaint_routing.db` from backend directory
2. Run initialization again:
   ```bash
   python init_db.py
   ```

### Issue: Module Not Found

Make sure virtual environment is activated:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` before command prompt.

### Issue: npm dependencies issues

```bash
# Clear cache
npm cache clean --force

# Remove node_modules
rm -r node_modules

# Reinstall
npm install
```

### Issue: Can't reach backend from frontend

Check:
1. Backend is running on `http://localhost:8000` ✅
2. Frontend `.env` has correct `VITE_API_URL` ✅
3. No firewall blocking port 8000 ✅

### Issue: Login not working

- **Student**: Email must end with `@karunya.edu.in`
- **Faculty**: Email must end with `@karunya.edu` and use one of:
  - `cse@karunya.edu` - password: `admin123`
  - `it@karunya.edu` - password: `admin123`
  - (And other department emails)

### Issue: Complaint not appearing in Faculty Dashboard

Ensure:
1. Student submitted complaint ✅
2. You're logged in as correct faculty department ✅
3. Complaint was auto-routed to that department ✅
4. Refresh page (F5) ✅

## Development Commands

### Backend

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run without reload (production-like)
uvicorn app.main:app
```

### Frontend

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Project Structure Quick Reference

```
D:\Complaint-Routing-System\
├── backend/
│   ├── app/
│   │   ├── main.py              ← Start here (main app)
│   │   ├── models.py            ← Database models
│   │   ├── schemas.py           ← Request/Response models
│   │   ├── auth.py              ← Authentication logic
│   │   ├── nlp/
│   │   │   └── classifier.py    ← NLP classifier
│   │   └── routers/
│   │       ├── student_routes.py
│   │       └── faculty_routes.py
│   ├── init_db.py               ← Initialize database
│   ├── requirements.txt          ← Python dependencies
│   └── .env                      ← Configuration (create from .env.example)
│
├── frontend/
│   ├── src/
│   │   ├── pages/               ← Page components
│   │   ├── components/          ← Reusable components
│   │   ├── services/            ← API & Auth services
│   │   ├── App.jsx              ← Main app component
│   │   └── main.jsx             ← Entry point
│   ├── package.json             ← npm dependencies
│   ├── vite.config.js           ← Vite configuration
│   ├── tailwind.config.js       ← Tailwind CSS config
│   └── .env                     ← Configuration
│
├── database/
│   └── schema.sql               ← Database schema
│
└── README.md                    ← This file
```

## Next Steps

1. **Explore the code** - Understand the architecture
2. **Modify features** - Customize for your needs
3. **Deploy** - Move to production (see DEPLOYMENT.md)
4. **Add features** - Implement email notifications, etc.

## Support & Help

For detailed information:
- Backend API docs: `http://localhost:8000/docs`
- See `DEPLOYMENT.md` for production setup
- See `README.md` for project overview

---

**Happy Complaining! 🚀** (In a good way 😄)
