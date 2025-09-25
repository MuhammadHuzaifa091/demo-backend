# 🔧 Troubleshooting Vercel API URL Issue

## ❌ Current Issue:
```
POST https://demo.publicvm.com/api/v1/auth/register-with-role net::ERR_FAILED
```

The frontend is still using the old hardcoded URL instead of the environment variable.

## 🔍 Debugging Steps:

### 1. Check Browser Console
Open browser console and look for these debug messages:
```
=== Axios Configuration Debug ===
NODE_ENV: production
PROD: true
DEV: false
VITE_API_BASE_URL: https://your-actual-backend-url.com
================================
```

### 2. Verify Environment Variable in Vercel

**Go to Vercel Dashboard:**
1. Select your project
2. Go to Settings → Environment Variables
3. Ensure you have:
   ```
   VITE_API_BASE_URL = https://your-backend-url.com
   ```
4. **IMPORTANT**: Make sure it's set for "Production" environment

### 3. Force Rebuild in Vercel

**Option A: Trigger Redeploy**
1. Go to Deployments tab in Vercel
2. Click "..." on latest deployment
3. Select "Redeploy"

**Option B: Push New Commit**
1. Make a small change to any file
2. Commit and push to trigger new build

### 4. Clear All Caches

**Local Development:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
rm -rf dist

# Rebuild
npm run build
```

**Browser:**
1. Open DevTools (F12)
2. Right-click refresh button
3. Select "Empty Cache and Hard Reload"

## 🚨 Common Issues & Solutions:

### Issue 1: Environment Variable Not Set
**Symptom:** Console shows `ENVIRONMENT_VARIABLE_NOT_SET`
**Solution:** Set `VITE_API_BASE_URL` in Vercel dashboard

### Issue 2: Wrong Environment Scope
**Symptom:** Variable works in preview but not production
**Solution:** Ensure variable is set for "Production" environment in Vercel

### Issue 3: Cached Build
**Symptom:** Still seeing old URL despite changes
**Solution:** Force redeploy in Vercel + clear browser cache

### Issue 4: CORS Issues
**Symptom:** API calls fail with CORS errors
**Solution:** Ensure backend allows requests from Vercel domain

## ✅ Verification Checklist:

- [ ] Environment variable `VITE_API_BASE_URL` set in Vercel
- [ ] Variable scope is set to "Production"
- [ ] Triggered new deployment after setting variable
- [ ] Browser cache cleared
- [ ] Console shows correct baseURL in debug messages
- [ ] Backend is accessible from the URL
- [ ] Backend allows CORS from Vercel domain

## 🔧 Quick Fix Commands:

### For Local Testing:
```bash
# Set environment variable locally
echo "VITE_API_BASE_URL=https://your-backend-url.com" > .env

# Clear cache and rebuild
rm -rf dist node_modules/.vite
npm run build
npm run preview
```

### For Vercel:
1. Set environment variable in dashboard
2. Redeploy
3. Check console for debug messages

## 📞 If Still Not Working:

1. **Check Network Tab**: See what URL is actually being called
2. **Check Console**: Look for debug messages from axios.js
3. **Verify Backend**: Ensure your backend URL is correct and accessible
4. **Test Locally**: Use `npm run build && npm run preview` to test production build locally
