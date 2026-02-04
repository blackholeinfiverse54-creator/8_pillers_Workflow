# 🚀 BHIV Bucket Render Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. External Services Setup
- [ ] Redis Cloud account created
- [ ] Redis database provisioned
- [ ] Redis connection details obtained (host, port, password)
- [ ] MongoDB Atlas account created
- [ ] MongoDB cluster created
- [ ] MongoDB connection string obtained
- [ ] Database access configured (IP whitelist: 0.0.0.0/0 for Render)

### 2. Code Preparation
- [ ] requirements.txt updated with all dependencies
- [ ] Dockerfile created and tested
- [ ] main.py updated to use PORT environment variable
- [ ] CORS origins configured for production
- [ ] Production logging configured
- [ ] .gitignore created to exclude sensitive files

### 3. Render Account Setup
- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Repository access granted to Render

## 🚀 Deployment Steps

### Step 1: Create Web Service
1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Select your GitHub repository
4. Choose branch: `main`
5. Configure service:
   ```
   Name: bhiv-bucket-service
   Environment: Python 3
   Region: Singapore (or closest to users)
   Branch: main
   Root Directory: BHIV_Central_Depository-main
   ```

### Step 2: Configure Build & Deploy
```
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

### Step 3: Set Environment Variables
```env
PORT=10000
ENVIRONMENT=production
LOG_LEVEL=INFO
REDIS_HOST=your-redis-host.com
REDIS_PASSWORD=your-redis-password
REDIS_PORT=6379
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/bucket_db
CORS_ORIGINS=https://your-frontend.com,https://api.your-domain.com
```

### Step 4: Configure Advanced Settings
- [ ] Auto-Deploy: Enabled
- [ ] Health Check Path: `/health`
- [ ] Instance Type: Free (or upgrade as needed)

### Step 5: Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for initial deployment (5-10 minutes)
- [ ] Monitor build logs for errors

## ✅ Post-Deployment Verification

### 1. Health Checks
Run the health check script:
```bash
python health_check.py https://your-service.onrender.com
```

Expected results:
- [ ] Service Health: ✅ Status 200
- [ ] Agents List: ✅ Status 200
- [ ] Baskets List: ✅ Status 200
- [ ] Redis Status: ✅ Status 200 or 503 (if not connected)
- [ ] Core Integration: ✅ Status 200
- [ ] PRANA Stats: ✅ Status 200
- [ ] Governance Info: ✅ Status 200

### 2. Manual Testing
Test key endpoints:
```bash
# Health check
curl https://your-service.onrender.com/health

# Core integration
curl -X POST https://your-service.onrender.com/core/write-event \
  -H "Content-Type: application/json" \
  -d '{
    "requester_id": "bhiv_core",
    "event_data": {
      "event_type": "test",
      "agent_id": "test_agent"
    }
  }'

# Check events
curl https://your-service.onrender.com/core/events
```

### 3. Integration Testing
- [ ] Test Core → Bucket integration
- [ ] Test PRANA telemetry ingestion
- [ ] Test governance endpoints
- [ ] Test audit middleware
- [ ] Verify MongoDB connection
- [ ] Verify Redis connection

### 4. Performance Testing
- [ ] Response time < 5 seconds for health check
- [ ] Memory usage within limits
- [ ] No memory leaks after 1 hour
- [ ] Concurrent request handling

## 🔧 Troubleshooting

### Common Issues

**Build Fails**
- Check requirements.txt for missing dependencies
- Verify Python version compatibility
- Check for syntax errors in main.py

**Service Won't Start**
- Verify PORT environment variable is set
- Check MongoDB connection string format
- Verify Redis credentials

**Health Check Fails**
- Check if service is listening on correct port
- Verify /health endpoint is accessible
- Check application logs in Render dashboard

**Database Connection Issues**
- Verify MongoDB Atlas IP whitelist includes 0.0.0.0/0
- Check connection string format
- Verify Redis Cloud credentials

### Monitoring & Logs
- [ ] Render dashboard logs accessible
- [ ] Application logs being written
- [ ] Error alerts configured
- [ ] Performance metrics monitored

## 📊 Success Criteria

Deployment is successful when:
- [ ] Service starts without errors
- [ ] Health check returns 200 status
- [ ] All critical endpoints respond correctly
- [ ] Database connections established
- [ ] Integration tests pass
- [ ] Performance meets requirements

## 🔄 Maintenance

### Regular Tasks
- [ ] Monitor service health daily
- [ ] Check logs for errors weekly
- [ ] Update dependencies monthly
- [ ] Review performance metrics monthly
- [ ] Backup database configurations

### Scaling Considerations
- [ ] Monitor request volume
- [ ] Track response times
- [ ] Monitor memory usage
- [ ] Plan for traffic growth
- [ ] Consider upgrading instance type when needed

---

**Deployment Owner**: Ashmit Pandey  
**Last Updated**: 2026-01-31  
**Service URL**: https://your-service.onrender.com  
**Status**: 🚀 Ready for Production