# 🚀 Quick Deploy to Render - 5 Minutes

## Prerequisites (2 minutes)
1. **Redis Cloud**: Get free account at https://redis.com/try-free/
   - Create database → Copy host, port, password
2. **MongoDB Atlas**: Get free account at https://mongodb.com/cloud/atlas
   - Create cluster → Get connection string

## Deploy Steps (3 minutes)

### 1. Create Render Service
- Go to https://render.com → Sign up with GitHub
- Click "New +" → "Web Service"
- Connect your GitHub repo
- Select branch: `main`

### 2. Configure Service
```
Name: bhiv-bucket
Environment: Python 3
Root Directory: BHIV_Central_Depository-main
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

### 3. Set Environment Variables
```env
PORT=10000
ENVIRONMENT=production
REDIS_HOST=your-redis-host.com
REDIS_PASSWORD=your-redis-password
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/bucket_db
```

### 4. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for deployment

## Test Deployment
```bash
# Replace with your Render URL
curl https://your-service.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "bucket_version": "1.0.0"
}
```

## 🎉 Done!
Your BHIV Bucket service is now live at: `https://your-service.onrender.com`

## Next Steps
- Update Core service to use your new Bucket URL
- Configure CORS origins for your frontend
- Set up monitoring and alerts
- Run full integration tests

---
**Need help?** Check `DEPLOYMENT_CHECKLIST.md` for detailed instructions.