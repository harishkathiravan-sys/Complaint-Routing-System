# Smart Complaint Routing System (NLP-Based)

![Karunya Institute](https://img.shields.io/badge/For-Karunya%20Institute-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)

An intelligent, production-ready complaint management system for Karunya Institute of Technology that automatically classifies and routes complaints to appropriate departments using Natural Language Processing.

## 🌟 Features

### ✨ Core Features
- 🤖 **AI-Powered Classification**: NLP-based automatic complaint routing
- 🔐 **Secure Authentication**: JWT-based authentication system
- 📊 **Real-time Tracking**: Live status updates with visual progress indicators
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- ⚡ **High Performance**: FastAPI backend with optimized database queries
- 🎨 **Modern UI**: Beautiful TailwindCSS interface

### 👨‍🎓 Student Features
- ✍️ Submit complaints with detailed descriptions
- 🔍 Track complaint status in real-time
- 📋 View complete complaint history
- 💬 Receive faculty responses
- 📊 Dashboard with statistics

### 👨‍💼 Faculty Features
- 📥 View complaints routed to their department
- ✅ Mark complaints as read
- 💬 Send detailed responses to students
- 🔄 Manage complaint status
- 📈 Department-wide analytics

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                 │
│  • Login Page • Student Dashboard • Faculty Dashboard      │
│  • Complaint Form • Status Tracker • Complaint Manager     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                    ↓ Axios
                       │
┌──────────────────────┴──────────────────────────────────────┐
│              Backend (FastAPI + Uvicorn)                    │
│  • JWT Authentication • API Routes • NLP Classifier        │
│  • Database Models • Business Logic                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                    ↓ SQLAlchemy
                       │
┌──────────────────────┴──────────────────────────────────────┐
│     Database (PostgreSQL / SQLite)                          │
│  • Students • Faculty • Departments • Complaints           │
│  • Status History • Complaint Replies                       │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Technology Stack

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **Axios**: HTTP client
- **React Router**: Navigation
- **Lucide React**: Icons

### Backend
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **PostgreSQL/SQLite**: Database
- **JWT**: Authentication
- **Pydantic**: Data validation
- **Passlib**: Password hashing

### NLP
- **Keyword-based classifier**: Initial implementation
- **Extensible**: Ready for ML models (scikit-learn, spaCy)

## 🔐 Default Credentials

### Student Login
- **Email**: `john@karunya.edu.in` (any @karunya.edu.in email)
- **Password**: Any password
- **Register**: New account option available

### Faculty Login
| Department | Email | Password |
|-----------|-------|----------|
| CSE | cse@karunya.edu | admin123 |
| IT | it@karunya.edu | admin123 |
| Electrical | electrical@karunya.edu | admin123 |
| Plumbing | plumbing@karunya.edu | admin123 |
| Administration | administration@karunya.edu | admin123 |

## 📚 Project Structure

```
smart-complaint-system/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── database.py                # SQLAlchemy config
│   │   ├── models.py                  # Database models
│   │   ├── schemas.py                 # Pydantic schemas
│   │   ├── auth.py                    # JWT auth
│   │   ├── routers/
│   │   │   ├── student_routes.py      # Student endpoints
│   │   │   ├── faculty_routes.py      # Faculty endpoints
│   │   │   └── complaint_routes.py    # Shared endpoints
│   │   └── nlp/
│   │       └── classifier.py          # NLP classifier
│   ├── init_db.py                     # Database init
│   ├── requirements.txt               # Dependencies
│   ├── .env.example                   # Config template
│   └── README.md                      # Backend docs
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── StudentDashboard.jsx
│   │   │   ├── FacultyDashboard.jsx
│   │   │   ├── ComplaintForm.jsx
│   │   │   ├── ComplaintStatus.jsx
│   │   │   └── NotFound.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatusBar.jsx
│   │   │   ├── ComplaintCard.jsx
│   │   │   └── FacultyComplaintModal.jsx
│   │   ├── services/
│   │   │   ├── api.js                 # API client
│   │   │   └── auth.js                # Auth utils
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── .env
│
├── database/
│   └── schema.sql
│
├── SETUP_GUIDE.md                     # Detailed setup
├── DEPLOYMENT.md                      # Production guide
├── setup.sh                           # Linux/Mac setup
├── setup.bat                          # Windows setup
└── README.md                          # This file
```

## 🚀 Running the System

### Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate              # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```
Backend: http://localhost:8000

### Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
Frontend: http://localhost:5173

### API Documentation
Open http://localhost:8000/docs for interactive API docs (Swagger UI)

## 🤖 NLP Classification

The system intelligently routes complaints based on keywords:

| Department | Keywords |
|-----------|----------|
| **CSE** | computer, lab, program, software, server, coding, system |
| **IT** | wifi, internet, network, router, connection, bandwidth |
| **Electrical** | light, fan, power, electric, voltage, switch, bulb |
| **Plumbing** | water, leak, pipe, bathroom, toilet, drain, tap |
| **Admin** | certificate, office, fees, id card, document, approval |

## 📊 Complaint Status Flow

```
1. Submitted
   ↓
2. Sent to Department
   ↓
3. Read by Faculty
   ↓
4. Resolved
```

## 🔌 API Endpoints

### Authentication
```
POST   /student/login              # Student login
POST   /student/register           # Student registration
POST   /faculty/login              # Faculty login
```

### Student Endpoints
```
GET    /student/profile            # Get profile
GET    /student/dashboard          # Get dashboard
POST   /student/complaint/submit   # Submit complaint
GET    /student/complaints         # Get complaints
GET    /student/complaint/{id}     # Get details
GET    /student/complaint/{id}/status  # Get status
```

### Faculty Endpoints
```
GET    /faculty/profile            # Get profile
GET    /faculty/dashboard          # Get dashboard
GET    /faculty/complaints         # Get complaints
GET    /faculty/complaint/{id}     # Get details
PUT    /faculty/complaint/{id}/read    # Mark read
PUT    /faculty/complaint/{id}/reply   # Add reply
PUT    /faculty/complaint/{id}/resolve # Resolve
```

### Shared Endpoints
```
GET    /complaint/departments      # Get departments
GET    /complaint/statistics       # Get statistics
GET    /health                     # Health check
```

## 🧪 Testing

### Test Cases
1. **Student Registration**: Create new account with @karunya.edu.in email
2. **Student Login**: Login with created credentials
3. **Complaint Submission**: Submit test complaints
4. **Auto-Routing**: Verify NLP classification
5. **Faculty Response**: Login as faculty and reply
6. **Status Tracking**: Monitor complaint progress

### Sample Complaints
```
"WiFi in hostel is not working" → IT
"Computer lab systems are down" → CSE
"Water leakage in bathroom" → Plumbing
"Lights in classroom are off" → Electrical
"Certificate approval delayed" → Administration
```

## 💾 Database

### Tables
- `departments`: Department master data
- `students`: Student accounts
- `faculty`: Faculty accounts
- `complaints`: Complaint records
- `complaint_replies`: Faculty responses
- `status_history`: Status change log

### Automatic Initialization
Run `python init_db.py` to:
- Create all tables
- Insert departments
- Create faculty accounts
- Set up indexes

## 🔐 Security Features

✅ JWT authentication with expiration
✅ Password hashing with bcrypt
✅ Email validation (@karunya.edu.in for students)
✅ CORS configured for frontend
✅ SQL injection prevention (SQLAlchemy ORM)
✅ Environment variables for secrets
✅ Role-based access control
✅ Student can only see own complaints
✅ Faculty can only see department complaints

## 📦 Dependencies

### Backend
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pydantic==2.5.0
- python-jose==3.3.0
- passlib==1.7.4
- psycopg2-binary==2.9.9

### Frontend
- react@^18.2.0
- axios@^1.6.2
- tailwindcss@^3.4.1

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Backend port 8000
lsof -ti:8000 | xargs kill -9

# Frontend port 5173
lsof -ti:5173 | xargs kill -9
```

### Database Issues
```bash
# Reset database
rm backend/complaint_routing.db
python backend/init_db.py
```

### Virtual Environment Issues
```bash
# Recreate venv
rm -r backend/venv
python -m venv backend/venv
source backend/venv/bin/activate
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

## 🚀 Deployment

For production deployment:
1. See [DEPLOYMENT.md](DEPLOYMENT.md)
2. Use PostgreSQL instead of SQLite
3. Set up environment variables
4. Enable HTTPS
5. Configure rate limiting
6. Set up monitoring

## 📈 Future Enhancements

- [ ] Email notifications
- [ ] SMS alerts
- [ ] Sentiment analysis
- [ ] Advanced ML classification
- [ ] File attachments
- [ ] Complaint escalation
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Analytics dashboard
- [ ] Automated responses

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file

## 👥 Contact & Support

**Developed for**: Karunya Institute of Technology and Sciences

For issues or questions:
- Create GitHub issue
- Contact: admin@karunya.edu.in

## 📸 Screenshots

### Login Page
- Clean, modern design
- Student & Faculty tabs
- Registration option

### Student Dashboard
- Welcome message
- Complaint statistics
- Recent complaints list
- Quick submit button

### Faculty Dashboard
- Department complaints
- Unread count
- Quick response modal
- Resolution tracking

### Status Tracker
- Visual progress bar
- Timeline view
- Faculty responses
- Status history

## 🎓 Learning Resources

This project demonstrates:
- FastAPI best practices
- React hooks & routing
- SQLAlchemy ORM
- JWT authentication
- NLP classification
- Responsive design
- RESTful API design

## 📝 Notes

- SQLite used for development (auto-created)
- PostgreSQL recommended for production
- All endpoints require valid JWT token (except login)
- Student emails must end with @karunya.edu.in
- Faculty emails must end with @karunya.edu

---

**Made with ❤️ for better complaint management at Karunya Institute**

![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)
![React](https://img.shields.io/badge/Made%20with-React-blue?logo=react)
![Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)