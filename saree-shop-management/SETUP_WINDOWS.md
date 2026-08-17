# Saree Shop Management System - Windows Setup Guide

## Prerequisites

Before you begin, install the following on your Windows computer:

1. **Node.js** (v18 or higher)
   - Download from: https://nodejs.org/
   - Choose the LTS version
   - During installation, check "Automatically install necessary tools" if prompted

2. **Python 3.11** (or 3.12)
   - Download from: https://www.python.org/downloads/
   - ⚠️ IMPORTANT: Check "Add Python to PATH" during installation

3. **PostgreSQL** (v14 or higher)
   - Download from: https://www.postgresql.org/download/windows/
   - Use the EnterpriseDB installer
   - Remember the password you set for the `postgres` user

4. **Git** (if not already installed)
   - Download from: https://git-scm.com/download/win

---

## Step 1: Clone the Repository

Open Command Prompt or PowerShell and run:

```bash
cd D:\inventory-management
git clone <your-github-repo-url> saree-shop-management
cd saree-shop-management
```

---

## Step 2: Set Up PostgreSQL Database

### Option A: Using pgAdmin (Recommended for beginners)

1. Open pgAdmin (installed with PostgreSQL)
2. Connect to your PostgreSQL server (use the password you set during installation)
3. Right-click on "Databases" → "Create" → "Database"
   - Database name: `saree_shop_db`
   - Owner: `postgres`
4. Click "Save"

### Option B: Using SQL Shell (psql)

1. Open "SQL Shell (psql)" from Start Menu
2. Press Enter to accept defaults until prompted for password
3. Enter your PostgreSQL password
4. Run these commands:

```sql
CREATE DATABASE saree_shop_db;
\\q
```

---

## Step 3: Configure Backend

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # In Command Prompt:
   venv\Scripts\activate.bat
   
   # In PowerShell:
   venv\Scripts\Activate.ps1
   ```
   
   If you get an error in PowerShell about execution policy, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create the `.env` file:
   
   Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
   
   Or create it manually with this content:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/saree_shop_db
   SECRET_KEY=change-this-secret-key-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   APP_NAME=SareeShopManagement
   DEBUG=True
   SERVER_HOST=127.0.0.1
   SERVER_PORT=8000
   PAYMENT_TEST_MODE=True
   ```
   
   ⚠️ Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

---

## Step 4: Initialize Database

With the virtual environment still activated, run:

```bash
# Run database migrations
alembic upgrade head

# Seed initial data (creates admin user)
python -m app.scripts.seed_data
```

You should see:
```
✓ Database tables created successfully
✓ Created 12 permissions
✓ Created 3 roles
✓ Created admin user (username: admin, password: admin123)
```

---

## Step 5: Install Frontend & Desktop Dependencies

Open a NEW Command Prompt or PowerShell window (keep the backend terminal open):

```bash
cd D:\inventory-management\saree-shop-management

# Install root dependencies
npm install

# Install frontend dependencies
cd frontend
npm install
cd ..

# Install desktop dependencies
cd desktop
npm install
cd ..
```

---

## Step 6: Run the Application

You need TWO terminals running simultaneously.

### Terminal 1: Backend Server

```bash
cd D:\inventory-management\saree-shop-management\backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Electron Desktop App

```bash
cd D:\inventory-management\saree-shop-management
npm run electron:dev
```

The Electron window will open automatically with the login screen.

---

## Step 7: Login

Use these default credentials:
- **Username**: `admin`
- **Password**: `admin123`

⚠️ Change the password after your first login!

---

## Verify Installation

### Check Backend API
Open your browser and go to: http://127.0.0.1:8000/docs

You should see the Swagger API documentation.

### Check Health Endpoint
Go to: http://127.0.0.1:8000/health

You should see: `{"status": "healthy"}`

---

## Common Issues & Solutions

### Issue: "python is not recognized"
**Solution**: 
- Make sure Python is installed
- Make sure "Add Python to PATH" was checked during installation
- Restart your terminal after installing Python

### Issue: "Access denied" when activating venv in PowerShell
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Connection refused" to database
**Solution**:
- Make sure PostgreSQL service is running
- Check if the password in `.env` matches your PostgreSQL password
- Verify the database `saree_shop_db` exists

### Issue: Port 8000 already in use
**Solution**:
- Close any other application using port 8000
- Or change the port in `.env`: `SERVER_PORT=8001`

### Issue: npm modules not found
**Solution**:
```bash
# Delete node_modules folders
rmdir /s /q node_modules
rmdir /s /q frontend\node_modules
rmdir /s /q desktop\node_modules

# Reinstall
npm install
cd frontend && npm install && cd ..
cd desktop && npm install && cd ..
```

---

## Building Production Installer

To create a Windows installer (.exe):

```bash
# Build frontend
cd frontend
npm run build
cd ..

# Build Electron app and create installer
npm run dist
```

The installer will be created at: `desktop/dist/SareeShopManagement-Setup.exe`

---

## Next Steps After First Login

1. Go to Settings → Update your shop details
2. Add Brands (e.g., Kanchipuram, Banarasi, etc.)
3. Add Categories (e.g., Silk, Cotton, etc.)
4. Create your first Saree product
5. Try the POS workflow
6. Explore Reports

---

## Support

For more information, see:
- `README.md` - Project overview
- `DEVELOPMENT.md` - Development guide
- `TROUBLESHOOTING.md` - Troubleshooting guide
