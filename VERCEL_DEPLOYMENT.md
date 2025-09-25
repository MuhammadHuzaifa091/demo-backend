# Vercel Deployment Guide for JiaWeiTong Home Service Connect

## 🚀 Frontend Configuration Fixed

### ✅ What Was Fixed:

1. **Axios Configuration**: Updated to use environment variables instead of hardcoded URLs
2. **API Service**: All API calls now use the configured axios instance
3. **Auth Store**: Updated to use the configured axios instance
4. **Environment Variables**: Created proper .env files for different environments

### 📁 Files Modified:

- `frontend/src/services/axios.js` - Now uses `VITE_API_BASE_URL` environment variable
- `frontend/src/services/api.js` - All API calls use configured axios instance
- `frontend/src/stores/auth.js` - Authentication uses configured axios instance
- `frontend/.env` - Local development environment variables
- `frontend/.env.example` - Template for environment variables

## 🔧 Vercel Deployment Steps:

### 1. Set Environment Variables in Vercel Dashboard:

Go to your Vercel project settings → Environment Variables and add:

```
VITE_API_BASE_URL=https://your-backend-api-url.com
```

**Replace `https://your-backend-api-url.com` with your actual backend URL**

### 2. Build Configuration:

Your `vite.config.js` should already be configured correctly. The app will:
- Use `VITE_API_BASE_URL` from Vercel environment variables in production
- Fall back to `http://127.0.0.1:8000` for local development

### 3. Deploy Process:

1. **Push to GitHub**: Commit all changes to your repository
2. **Connect to Vercel**: Link your GitHub repository to Vercel
3. **Set Environment Variables**: Add `VITE_API_BASE_URL` in Vercel dashboard
4. **Deploy**: Vercel will automatically build and deploy

### 4. Verify Deployment:

After deployment, check:
- ✅ Frontend loads correctly
- ✅ API calls go to the correct backend URL
- ✅ Authentication works
- ✅ All features function properly

## 🔍 Environment Variable Usage:

### Local Development:
```bash
# .env file
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### Production (Vercel):
```bash
# Set in Vercel dashboard
VITE_API_BASE_URL=https://your-backend-api.vercel.app
```

## 🛠️ Troubleshooting:

### If API calls still go to wrong URL:

1. **Check Environment Variables**: Ensure `VITE_API_BASE_URL` is set in Vercel
2. **Rebuild**: Trigger a new deployment in Vercel
3. **Clear Cache**: Clear browser cache and try again
4. **Check Console**: Look for any error messages in browser console

### Common Issues:

- **CORS Errors**: Ensure your backend allows requests from your Vercel domain
- **Environment Variables**: Make sure they start with `VITE_` prefix
- **Build Errors**: Check Vercel build logs for any issues

## 📋 Checklist:

- [ ] Environment variable `VITE_API_BASE_URL` set in Vercel
- [ ] Backend URL is correct and accessible
- [ ] Frontend builds successfully
- [ ] API calls work in production
- [ ] Authentication functions properly
- [ ] All features tested and working

## 🎯 Result:

Your frontend will now correctly use the environment variable for API calls, making it work properly in both local development and Vercel production environments!
