# Smart Complaint Routing System (NLP-Based)

An intelligent complaint management system for Karunya Institute of Technology that automatically classifies and routes complaints to appropriate departments using Natural Language Processing.

## 🎯 Features

### For Students
- 📝 **Complaint Submission**: Submit complaints with automatic NLP classification
- 📊 **Status Tracking**: Real-time status updates with visual progress bar
- 📱 **Dashboard**: View complaint history and statistics
- 🔔 **Notifications**: Get faculty responses in real-time
- 🔐 **Secure**: JWT-based authentication

### For Faculty
- 📋 **Complaint Management**: View all complaints for their department
- ✅ **Mark as Read**: Acknowledge complaint receipt
- 💬 **Reply Management**: Send detailed responses to students
- 🔄 **Status Updates**: Mark complaints as resolved
- 📈 **Analytics**: View department-wise complaint statistics

### System Features
- 🤖 **NLP Classification**: Intelligent keyword-based complaint routing
- 🔐 **JWT Authentication**: Secure token-based authentication
- 📊 **Real-time Updates**: Live status tracking
- 🎨 **Modern UI**: Responsive TailwindCSS design
- ⚡ **Fast**: FastAPI backend with PostgreSQL/SQLite

## 🏗️ System Architecture

```
smart-complaint-system/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main application
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── auth.py         # JWT authentication
│   │   ├── routers/
│   │   │   ├── student_routes.py
│   │   │   ├── faculty_routes.py
│   │   │   └── complaint_routes.py
│   │   └── nlp/
│   │       └── classifier.py  # NLP classifier
│   ├── requirements.txt
│   ├── init_db.py          # Database initialization
│   └── .env.example
├── frontend/               # React Vite frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── StudentDashboard.jsx
│   │   │   ├── FacultyDashboard.jsx
│   │   │   ├── ComplaintForm.jsx
│   │   │   └── ComplaintStatus.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatusBar.jsx
│   │   │   ├── ComplaintCard.jsx
│   │   │   └── FacultyComplaintModal.jsx
│   │   ├── services/
│   │   │   ├── api.js      # API communication
│   │   │   └── auth.js     # Auth utilities
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env
└── database/
    └── schema.sql          # Database schema
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL or SQLite3

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Run server
uvicorn app.main:app --reload --port 8000
```

Backend will be at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file (already created)
# VITE_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Frontend will be at `http://localhost:5173`

## 🔐 Authentication

### Student Login
- **Email Format**: `name@karunya.edu.in`
- **Password**: Any format (or URK25CSXXXX for authenticity)
- **New Students**: Can register with same format

### Faculty Login
- **Email Format**: `department@karunya.edu`
- **Password**: `admin123`
- **Departments**: 
  - `cse@karunya.edu` (CSE Department)
  - `it@karunya.edu` (IT Department)
  - `electrical@karunya.edu` (Electrical Department)
  - `plumbing@karunya.edu` (Plumbing & Facilities)
  - `administration@karunya.edu` (Administration)

## 🤖 NLP Complaint Classification

The system automatically classifies complaints to departments based on keywords:

### CSE (Computer Science & Engineering)
Keywords: computer, lab, program, software, server, coding, system, desktop, workstation, etc.

### IT (Information Technology)
Keywords: wifi, internet, network, router, connection, bandwidth, ethernet, etc.

### ELECTRICAL (Electrical Engineering)
Keywords: light, fan, power, electric, voltage, switch, bulb, circuit, etc.

### PLUMBING (Plumbing & Facilities)
Keywords: water, leak, pipe, bathroom, toilet, drain, tap, sink, etc.

### ADMINISTRATION
Keywords: certificate, office, fees, id card, document, approval, admission, etc.

## 📊 API Endpoints

### Student Routes

```
POST   /student/login              # Login
POST   /student/register           # Register
GET    /student/profile            # Get profile
GET    /student/dashboard          # Get dashboard
POST   /student/complaint/submit   # Submit complaint
GET    /student/complaints         # Get complaints
GET    /student/complaint/{id}     # Get complaint details
GET    /student/complaint/{id}/status  # Get complaint status
```

### Faculty Routes

```
POST   /faculty/login              # Login
GET    /faculty/profile            # Get profile
GET    /faculty/dashboard          # Get dashboard
GET    /faculty/complaints         # Get complaints
GET    /faculty/complaint/{id}     # Get complaint details
PUT    /faculty/complaint/{id}/read     # Mark as read
PUT    /faculty/complaint/{id}/reply    # Add reply
PUT    /faculty/complaint/{id}/resolve  # Resolve complaint
```

### Shared Routes

```
GET    /complaint/departments      # Get all departments
GET    /complaint/department/{code} # Get department
GET    /complaint/statistics       # Get statistics
GET    /health                     # Health check
```

## 💾 Database Schema

### Key Tables

- **departments**: Department information
- **students**: Student accounts
- **faculty**: Faculty accounts
- **complaints**: Student complaints
- **complaint_replies**: Faculty responses
- **status_history**: Status change tracking

## 🔄 Complaint Status Flow

```
Submitted
    ↓
Sent to Department
    ↓
Read by Faculty
    ↓
Resolved
```

### Status Updates
1. **Submitted**: When student submits complaint
2. **Sent to Department**: Automatically after submission
3. **Read by Faculty**: When faculty marks as read
4. **Resolved**: When faculty marks as resolved

## 🎨 Frontend Technologies

- **React 18**: UI framework
- **Vite**: Build tool (fast development)
- **TailwindCSS**: Styling
- **Axios**: HTTP client
- **React Router**: Navigation
- **Lucide React**: Icons

## 🔧 Backend Technologies

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Pydantic**: Data validation
- **Python-Jose**: JWT tokens
- **Passlib**: Password hashing
- **PostgreSQL/SQLite**: Database

## 📦 Environment Variables

### Backend `.env`
```
DATABASE_TYPE=sqlite              # or postgresql
DATABASE_URL=...                  # For PostgreSQL
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
SQL_ECHO=false
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
UVICORN_RELOAD=true
```

### Frontend `.env`
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Smart Complaint Routing System
```

## 🧪 Testing

### Test Accounts

**Student**
- Email: `john@karunya.edu.in`
- Password: `any_password` (or register new)

**Faculty**
- Email: `cse@karunya.edu`
- Password: `admin123`

### Test Complaints

Try submitting these complaints to see auto-routing:

1. "WiFi in hostel is not working" → IT
2. "Computer lab PCs not working" → CSE
3. "Water leakage in bathroom" → PLUMBING
4. "Lights not working in classroom" → ELECTRICAL
5. "Certificate approval delayed" → ADMINISTRATION

## 📈 Features Implemented

✅ Student registration and login
✅ Faculty login
✅ Complaint submission
✅ NLP-based automatic routing
✅ Status tracking
✅ Faculty review and response
✅ JWT authentication
✅ Responsive UI
✅ Real-time updates
✅ Email format validation
✅ Database models and schema
✅ API endpoints
✅ Error handling

## 🚀 Deployment

### Production Backend
```bash
# Using Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### Production Frontend
```bash
# Build
npm run build

# Serve with any static server (nginx, apache, etc.)
# Or deploy to Vercel, Netlify
```

### Docker Deployment
Create `Dockerfile` for containerization and deploy on:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

## 🔐 Security Considerations

1. ✅ JWT authentication with secure tokens
2. ✅ Password hashing with bcrypt
3. ✅ Environment variables for secrets
4. ✅ Email validation
5. ✅ Student can only access their complaints
6. ✅ Faculty can only access department complaints
7. ✅ CORS configured for frontend
8. ⚠️ TODO: Rate limiting
9. ⚠️ TODO: HTTPS enforcement
10. ⚠️ TODO: Security headers

## 📝 Future Enhancements

- [ ] Email notifications
- [ ] Sentiment analysis for priority detection
- [ ] Advanced ML-based classification
- [ ] Multi-language support
- [ ] File attachments
- [ ] Complaint escalation
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] SMS notifications
- [ ] Automated responses

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Support

For issues, questions, or feedback:
- Create an issue on GitHub
- Contact: admin@karunya.edu.in

## 🎓 Developed for

**Karunya Institute of Technology and Sciences**
Coimbatore, India

---

**Made with ❤️ for better complaint management**
