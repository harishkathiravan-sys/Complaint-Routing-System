#!/bin/bash
# Quick Start Script for Smart Complaint Routing System

echo "=========================================="
echo "Smart Complaint Routing System"
echo "Quick Start Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}Checking Python...${NC}"
python --version
if [ $? -ne 0 ]; then
    echo "Python not found. Please install Python 3.8+"
    exit 1
fi

# Check Node
echo -e "${BLUE}Checking Node.js...${NC}"
node --version
npm --version
if [ $? -ne 0 ]; then
    echo "Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Backend Setup
echo ""
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}Created .env file${NC}"
fi

# Initialize database
echo "Initializing database..."
python init_db.py

echo -e "${GREEN}Backend setup complete!${NC}"
echo ""

# Frontend Setup
echo -e "${BLUE}Setting up Frontend...${NC}"
cd ../frontend

# Install npm dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo -e "${GREEN}Frontend setup complete!${NC}"
echo ""

# Final instructions
echo "=========================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "To run the system:"
echo ""
echo -e "${YELLOW}Terminal 1 - Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo -e "${YELLOW}Terminal 2 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:5173"
echo ""
echo "Test Accounts:"
echo "  Student: test@karunya.edu.in (register new)"
echo "  Faculty: cse@karunya.edu / admin123"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
