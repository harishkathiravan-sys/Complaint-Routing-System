# Database Migration Guide: SQLite → PostgreSQL

Guide to migrate from development SQLite database to production PostgreSQL database.

## Why PostgreSQL for Production?

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Concurrent Users | 1-2 | Hundreds |
| Reliability | File-based | Production-grade |
| Backups | Manual | Automatic |
| Scaling | Limited | Excellent |
| Security | Limited | Advanced |

## Step 1: Export Data from SQLite (Optional)

If you have existing complaints/data to migrate:

### 1.1 Using Python Script

Create `migrate_db.py` in backend:

```python
import sqlite3
import json
from datetime import datetime

# Connect to SQLite
sqlite_conn = sqlite3.connect('complaint_routing.db')
sqlite_cursor = sqlite_conn.cursor()

# Export all tables
tables = ['students', 'faculty', 'departments', 'complaints', 'complaint_replies', 'status_history']

for table in tables:
    sqlite_cursor.execute(f"SELECT * FROM {table}")
    rows = sqlite_cursor.fetchall()
    print(f"Table {table}: {len(rows)} rows")

sqlite_conn.close()
```

Run: `python migrate_db.py`

## Step 2: Update Database Configuration

### 2.1 Update Backend `.env`

Change from:
```
DATABASE_TYPE=sqlite
```

To:
```
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/complaint_routing_db
```

### 2.2 Connection String Format

PostgreSQL connection strings follow this pattern:

```
postgresql://username:password@host:port/database_name
```

**Examples:**

Local PostgreSQL:
```
postgresql://postgres:password@localhost:5432/complaint_routing_db
```

Render PostgreSQL:
```
postgresql://user_xxxxx:password_xxxxx@dpg-xxxxx-a.region.databases.render.com:5432/complaint_routing_db
```

## Step 3: Update Database Configuration in Code

The code already supports PostgreSQL via SQLAlchemy across both:
- `database.py` - Reads `DATABASE_TYPE` environment variable
- `models.py` - Uses SQLAlchemy ORM (database-agnostic)
- `schemas.py` - Pydantic schemas (database-agnostic)

**No code changes needed!** ✓

## Step 4: Create PostgreSQL Database

### Option A: Local PostgreSQL (for testing)

```bash
# Install PostgreSQL
# Windows: https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Start PostgreSQL service
# Windows: net start postgresql-x64-XXX
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
createdb complaint_routing_db

# Create user (optional)
createuser complaint_user
psql -U postgres -d complaint_routing_db -c "ALTER USER complaint_user WITH PASSWORD 'your_password';"

# Get connection string
echo "postgresql://complaint_user:your_password@localhost:5432/complaint_routing_db"
```

### Option B: Render PostgreSQL (Recommended for Production)

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Fill in details:
   - Name: `complaint-routing-db`
   - Plan: Free (or paid)
   - Region: Same as backend
4. Click "Create Database"
5. Copy the External Database URL

## Step 5: Initialize PostgreSQL Schema

### 5.1 Using init_db.py

The existing `init_db.py` script already handles PostgreSQL initialization:

```bash
cd backend

# Set environment variables
export DATABASE_TYPE=postgresql
export DATABASE_URL=postgresql://user:password@host:5432/db

# Run initialization
python init_db.py
```

This will:
- Create all 6 tables
- Create default departments
- Create default faculty accounts
- **Note**: Won't create demo student (to avoid duplicates)

### 5.2 Manual Schema Creation

If you prefer manual setup:

```bash
# Using psql
psql $DATABASE_URL < database/schema.sql
```

Or copy-paste SQL from [database/schema.sql](database/schema.sql)

## Step 6: Test PostgreSQL Connection

### 6.1 Local Testing

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Test connection
python -c "
from app.database import SessionLocal, engine
try:
    db = SessionLocal()
    db.execute('SELECT 1')
    print('✓ PostgreSQL connection successful!')
except Exception as e:
    print(f'✗ Connection failed: {e}')
"
```

### 6.2 Verify Tables Created

```bash
cd backend

python -c "
from app.database import Base, engine
from app.models import Student, Faculty, Department, Complaint, ComplaintReply

tables = Base.metadata.tables.keys()
print('Created tables:')
for table in tables:
    print(f'  ✓ {table}')
"
```

## Step 7: Migrate Existing Data (If Any)

### 7.1 Export SQLite Data

```python
# export_sqlite.py
import sqlite3
import json
from datetime import datetime

sqlite_conn = sqlite3.connect('complaint_routing.db')
sqlite_conn.row_factory = sqlite3.Row

data = {}
tables = ['students', 'faculty', 'departments', 'complaints']

for table in tables:
    cursor = sqlite_conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    data[table] = [dict(row) for row in rows]
    print(f"Exported {table}: {len(rows)} rows")

sqlite_conn.close()

# Save to JSON
with open('export_data.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

print("Data exported to export_data.json")
```

Run: `python export_sqlite.py`

### 7.2 Import to PostgreSQL

```python
# import_postgres.py
import json
from app.database import SessionLocal
from app.models import Department, Faculty, Student
from app.auth import hash_password

db = SessionLocal()

with open('export_data.json', 'r') as f:
    data = json.load(f)

# Import departments
for dept in data['departments']:
    existing = db.query(Department).filter(
        Department.code == dept['code']
    ).first()
    if not existing:
        db.add(Department(**dept))
        print(f"✓ Imported department: {dept['code']}")

db.commit()
print("Migration complete!")
```

## Step 8: Deploy to Render

### 8.1 Update Render Environment Variables

1. Go to Render Dashboard
2. Select your `complaint-routing-api` service
3. Go to "Environment"
4. Update:
   - `DATABASE_TYPE`: `postgresql`
   - `DATABASE_URL`: Paste PostgreSQL URL from Step 4
5. Click "Save"
6. Service will auto-redeploy

### 8.2 Initialize Database on Render

Option 1: Run manually after deployment
```bash
# SSH into Render instance (if available)
# Run: python init_db.py
```

Option 2: Add to build command in render.yaml
```yaml
services:
  - type: web
    buildCommand: pip install -r requirements.txt && python init_db.py
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Step 9: Verify Production Database

### 9.1 Check Backend Logs

```bash
# In Render dashboard, go to Logs tab
# Look for successful messages like:
# "Creating database tables..."
# "✓ Tables created successfully"
# "Initializing departments..."
```

### 9.2 Test API Endpoints

```bash
# Test health check
curl https://complaint-routing-api.onrender.com/health

# Should return:
# {"status": "healthy", "message": "..."}
```

### 9.3 Test Database Connectivity

```bash
# Using psql (if you have credentials)
psql $DATABASE_URL

# In psql:
\dt  # List tables
SELECT COUNT(*) FROM students;
```

## Step 10: Cleanup

### 10.1 Delete Local SQLite Database

```bash
# Keep backup first
cp backend/complaint_routing.db backup/complaint_routing.db.bak

# Delete local file
rm backend/complaint_routing.db
```

### 10.2 Update .gitignore

Add PostgreSQL environment files:

```
# .gitignore
.env
.env.local
.env.*.local
complaint_routing.db
```

## Rollback Plan

If something goes wrong:

### 1. Quick Rollback to SQLite

```bash
# Change DATABASE_TYPE back to sqlite
DATABASE_TYPE=sqlite

# Start backend
python -m uvicorn app.main:app --reload
```

### 2. Rollback on Render

1. Go to Render Service Settings
2. Change `DATABASE_TYPE` to `sqlite`
3. Click "Save"
4. Service redeploys with SQLite

### 3. Restore from Backup

```bash
# Use exported JSON
python import_postgres.py
```

## Performance Tips for PostgreSQL

### Enable Connection Pooling

In production, use connection pooling for better performance:

```bash
# Add to requirements.txt
pgbouncer

# Or use SQLAlchemy with pool configuration
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool  # For serverless/scaled environments
)
```

### Optimize Queries

Already done in code with:
- Proper indexes on `student_id`, `status`, `created_at`
- Lazy loading where appropriate
- Batch operations

### Monitor Performance

```sql
-- Login to PostgreSQL and run:
SELECT 
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Troubleshooting

### Connection Refused

**Error**: `could not connect to server`

**Solutions**:
- Verify PostgreSQL service is running
- Check `DATABASE_URL` is correct
- Verify firewall allows connection
- Check credentials: user/password

### Invalid Connection String

**Error**: `ValueError: could not parse`

**Format**: `postgresql://user:password@host:port/dbname`

- `user`: PostgreSQL username
- `password`: Password (with special chars URL-encoded)
- `host`: Server address
- `port`: Usually 5432
- `dbname`: Database name

### Operation Not Permitted

**Error**: `permission denied for schema public`

**Solution**: Grant privileges:
```sql
GRANT ALL PRIVILEGES ON SCHEMA public TO your_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
```

### Database Doesn't Exist

**Error**: `database "complaint_routing_db" does not exist`

**Solution**:
```bash
# Create database
createdb complaint_routing_db -U postgres

# Or in psql:
CREATE DATABASE complaint_routing_db;
```

## Summary Checklist

- [ ] PostgreSQL service running
- [ ] Database created with correct name
- [ ] Connection string verified
- [ ] `DATABASE_URL` set in `.env`
- [ ] `init_db.py` executed successfully
- [ ] Tables verified: `\dt` in psql
- [ ] Test API endpoints working
- [ ] Frontend connects successfully
- [ ] Login works with default credentials
- [ ] Data persists after server restart

---

**Migration Status**: ✅ Ready for Production!

For production on Render, follow [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)
