# JNF Payroll System

A full-stack web application demonstrating React frontend and Flask backend integration deployed on Azure App Service.

## 🚀 Features

- **React Frontend**: Modern, responsive login interface using Material-UI
- **Flask Backend**: RESTful API with JWT authentication
- **Azure Deployment**: Automated CI/CD pipeline with GitHub Actions
- **Authentication**: Secure login system with token-based authentication
- **Demo Accounts**: Pre-configured demo users for testing

## 🏗️ Architecture

```
Frontend (React)  →  Backend (Flask)  →  Azure App Service
     ↓                    ↓                    ↓
Material-UI UI    →   JWT Auth API    →   Auto Deployment
```

## 🧪 Demo Accounts

| Username | Password    | Role  |
|----------|-------------|-------|
| admin    | password123 | admin |
| demo     | demo123     | user  |

## 🛠️ Local Development

### Prerequisites

- Node.js 18+ and npm
- Python 3.13+
- Git

### Backend Setup

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask server:**

   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Update environment for local development:**
   - Edit `frontend/.env`
   - Uncomment: `REACT_APP_API_URL=http://localhost:5000`
   - Comment out the Azure URL

4. **Start the React development server:**

   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## 🚀 Azure Deployment

The application is automatically deployed to Azure App Service using GitHub Actions when code is pushed to the `development` branch.

### Deployment Process

1. **Build Phase:**
   - Sets up Node.js and Python environments
   - Installs frontend dependencies and builds React app
   - Installs Python dependencies
   - Copies React build files to Flask static/templates folders
   - Creates deployment artifact

2. **Deploy Phase:**
   - Downloads build artifact
   - Authenticates with Azure
   - Deploys to Azure App Service

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves React app |
| GET | `/health` | Health check |
| POST | `/api/login` | User authentication |
| POST | `/api/verify-token` | Token verification |
| GET | `/api/protected` | Protected route (requires auth) |

### Example API Usage

**Login Request:**

```json
POST /api/login
{
  "username": "admin",
  "password": "password123"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1Q...",
  "user": {
    "username": "admin",
    "email": "admin@jnfpayroll.com",
    "role": "admin"
  }
}
```

## 🔧 Technology Stack

### Frontend

- **React 19** - UI framework
- **Material-UI** - Component library
- **Axios** - HTTP client
- **Create React App** - Build tooling

### Backend

- **Flask 3.0** - Web framework
- **PyJWT** - JWT token handling
- **Flask-CORS** - Cross-origin resource sharing
- **Werkzeug** - Password hashing

### DevOps

- **GitHub Actions** - CI/CD pipeline
- **Azure App Service** - Cloud hosting
- **Azure CLI** - Deployment automation

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Werkzeug secure password hashing
- **CORS Configuration**: Controlled cross-origin requests
- **Token Expiration**: 24-hour token lifetime
- **Protected Routes**: Authorization required for sensitive endpoints

## 🚀 Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd jnf-payroll
   ```

2. **Start backend:**

   ```bash
   pip install -r requirements.txt
   python app.py
   ```

3. **Start frontend (in new terminal):**

   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application:**
   - Frontend: <http://localhost:3000>
   - Backend API: <http://localhost:5000>
