# JiaWeiTong Home Service Connect

A comprehensive full-stack web application for connecting homeowners with trusted service providers, built with FastAPI and Vue.js 3.5 with role-based authentication and modern UI/UX.

## Features

### Backend (FastAPI)
- ✅ **Role-Based Authentication**: JWT-based authentication with 3 user roles
- ✅ **Custom JWT Claims**: Role information embedded in tokens
- ✅ **Repair Requests**: CRUD operations for repair requests
- ✅ **Service Providers**: CRUD operations for service provider profiles
- ✅ **Authorization**: Users can only edit/delete their own content
- ✅ **Database**: SQLAlchemy with async support and role-based fields
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs

### Frontend (Vue.js 3.5 + TailwindCSS)
- ✅ **Step-Form Registration**: Modern wizard-style registration flow
- ✅ **Role-Based UI**: Different interfaces for Users vs Service Providers
- ✅ **TailwindCSS**: Modern, responsive design with utility classes
- ✅ **Role-Based Routing**: Automatic redirects based on user role
- ✅ **State Management**: Pinia for global state management
- ✅ **API Integration**: Axios for HTTP requests with interceptors
- ✅ **Animated Components**: Smooth transitions and modern animations

### User Roles
- **User**: Can post repair requests and browse service providers
- **Service Provider (Individual)**: Solo professionals offering services
- **Service Provider (Organization)**: Companies with teams

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - Basic user registration
- `POST /api/v1/auth/register-with-role` - **New**: Role-based registration with step form
- `GET /api/v1/users/me` - Get current user info

### Repair Requests
- `GET /api/v1/repair-requests/` - List all repair requests
- `POST /api/v1/repair-requests/` - Create new repair request (auth required)
- `GET /api/v1/repair-requests/{id}` - Get single repair request
- `PUT /api/v1/repair-requests/{id}` - Update repair request (owner only)
- `DELETE /api/v1/repair-requests/{id}` - Delete repair request (owner only)

### Service Providers
- `GET /api/v1/providers/` - List all service providers
- `POST /api/v1/providers/` - Create new service provider (auth required)
- `GET /api/v1/providers/{id}` - Get single service provider
- `PUT /api/v1/providers/{id}` - Update service provider (owner only)
- `DELETE /api/v1/providers/{id}` - Delete service provider (owner only)

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd demo_mvp
   pip install -e .
   ```

2. **Set up environment variables** (optional):
   ```bash
   cp .env.dev .env
   # Edit .env file if needed
   ```

3. **Run database migrations**:
   ```bash
   # Option 1: Use our migration script (recommended for development)
   python create_migration.py
   
   # Option 2: Use alembic (if you have migrations set up)
   alembic upgrade head
   ```

4. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies** (includes TailwindCSS):
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at: http://localhost:3000

## 🎯 **Complete Role-Based System**

### **Role-Based Access Control**
- **Users**: Can create repair requests (text or voice) + browse services
- **Providers**: Can create services + view all repair requests with voice playback
- **JWT Claims**: Include role information for frontend access control

### **Voice Upload & Playback System**
- **Users**: Upload voice recordings (.mp3, .wav, .m4a) up to 10MB
- **Providers**: Listen to voice recordings with built-in audio player
- **File Storage**: Secure file storage in `/uploads/voices/` directory
- **API Endpoint**: `/api/v1/repair-requests/voice/{filename}` (providers only)

### **New API Endpoints**
```
POST /api/v1/repair-requests/     # Create request (users only) - supports FormData with voice files
GET  /api/v1/repair-requests/     # List requests (providers only)
GET  /api/v1/repair-requests/voice/{filename}  # Serve voice files (providers only)

POST /api/v1/services/            # Create service (providers only)
GET  /api/v1/services/            # List services (users only)
GET  /api/v1/services/my/services # Get provider's own services
PUT  /api/v1/services/{id}        # Update service (owner only)
DELETE /api/v1/services/{id}      # Delete service (owner only)
```

### **Frontend Features**
- **Step-Form Registration**: Modern 3-step wizard with role selection
- **Role-Based Dashboards**: 
  - User Dashboard: Create requests with voice upload, browse services
  - Provider Dashboard: Manage services, browse requests with voice playback
- **Voice Support**: File upload with validation, audio playback controls
- **Modern UI**: TailwindCSS with animations, gradients, and responsive design

### **Database Schema Updates**
```sql
-- Users table (updated)
ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user';
ALTER TABLE users ADD COLUMN service_type TEXT;
ALTER TABLE users ADD COLUMN experience TEXT;
ALTER TABLE users ADD COLUMN contact_info TEXT;
ALTER TABLE users ADD COLUMN company_name TEXT;
ALTER TABLE users ADD COLUMN team_size INTEGER;

-- Repair requests table (updated)
ALTER TABLE repair_requests ADD COLUMN voice_file TEXT;
-- description is now optional

-- Services table (new)
CREATE TABLE services (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    service_type TEXT NOT NULL,
    description TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    provider_id TEXT NOT NULL,
    FOREIGN KEY (provider_id) REFERENCES users (id) ON DELETE CASCADE
);
```

## Database Schema

### Users Table (Updated)
- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `hashed_password` (String)
- `first_name` (String, Optional)
- `last_name` (String, Optional)
- `is_active` (Boolean)
- `is_superuser` (Boolean)
- `is_verified` (Boolean)
- **`role`** (Enum: user, provider_individual, provider_organization)
- **`service_type`** (String, Optional) - For providers
- **`experience`** (Text, Optional) - For individual providers
- **`contact_info`** (Text, Optional) - For providers
- **`company_name`** (String, Optional) - For organizations
- **`team_size`** (Integer, Optional) - For organizations

### Repair Requests Table
- `id` (UUID, Primary Key)
- `title` (String)
- `description` (Text)
- `created_at` (DateTime)
- `user_id` (UUID, Foreign Key → Users)

### Service Providers Table
- `id` (UUID, Primary Key)
- `name` (String)
- `service_type` (String)
- `description` (Text)
- `contact_info` (Text)
- `created_at` (DateTime)
- `user_id` (UUID, Foreign Key → Users)

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **FastAPI-Users**: Authentication and user management
- **SQLAlchemy**: SQL toolkit and ORM with async support
- **Alembic**: Database migration tool
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **SQLite/PostgreSQL**: Database (SQLite for dev, PostgreSQL for prod)

### Frontend
- **Vue.js 3.5**: Progressive JavaScript framework with Composition API
- **Vue Router 4**: Official router for Vue.js
- **Pinia**: State management library for Vue
- **Axios**: HTTP client for API requests
- **Vite**: Fast build tool and development server
- **CSS3**: Modern styling with Grid, Flexbox, and gradients

## Development

### Running Tests
```bash
# Backend tests
pytest

# Frontend tests (if added)
cd frontend
npm run test
```

### Code Quality
```bash
# Python linting and formatting
ruff check .
ruff format .

# Type checking
mypy app/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Production Deployment

### Backend
- Use `gunicorn` with `uvicorn` workers
- Set up PostgreSQL database
- Configure environment variables
- Use reverse proxy (nginx)

### Frontend
- Build for production: `npm run build`
- Serve static files with nginx or CDN
- Update API base URL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🚀 Quick Start Guide

### Testing the Role-Based System

1. **Start both servers**:
   ```bash
   # Terminal 1 - Backend
   uvicorn app.main:app --reload --port 8000
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

2. **Test User Registration**:
   - Visit http://localhost:3000/register
   - Try registering as different roles:
     - **User**: Simple flow, redirects to User Dashboard
     - **Individual Provider**: Additional service fields
     - **Organization**: Company details and team size

3. **Test Role-Based Features**:
   - **Users**: Can create repair requests, browse providers
   - **Providers**: Can create services, browse repair requests
   - **Navigation**: Changes based on user role
   - **Dashboards**: Different interfaces for each role

4. **Test JWT Claims**:
   - Login and check browser dev tools → Application → Local Storage
   - JWT token contains role information
   - API calls include role in Authorization header

### Key URLs
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/v1/docs
- **Step Registration**: http://localhost:3000/register
- **User Dashboard**: http://localhost:3000/dashboard
- **Provider Dashboard**: http://localhost:3000/provider-dashboard

## 🔧 Troubleshooting

### Common Issues

1. **400 Bad Request on Registration**:
   - Run the database migration: `python create_migration.py`
   - Check if the backend server is running on port 8000
   - Verify the frontend is making requests to the correct endpoint

2. **Authentication Errors**:
   - Clear browser localStorage and cookies
   - Restart both frontend and backend servers
   - Check browser console for detailed error messages

3. **Database Issues**:
   - Delete `app.db` file and run migration again
   - Make sure SQLite is installed and accessible

4. **Frontend Build Issues**:
   - Delete `node_modules` and run `npm install` again
   - Make sure Node.js version is 16 or higher

### Debug Endpoints
- **Test Roles**: `GET /api/v1/auth/test-roles` - Check if role system is working
- **API Health**: `GET /api/v1/docs` - View all available endpoints

## License

This project is licensed under the MIT License.
