# Coolify Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Git Repository

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Math Operations API"

# Add your remote repository
git remote add origin https://github.com/yourusername/math-api.git

# Push to main branch
git push -u origin main
```

### 2. Deploy on Coolify

#### Option A: Using Coolify Dashboard (Recommended)

1. **Login to Coolify** on your VPS
   - Navigate to your Coolify dashboard (usually `https://coolify.yourdomain.com`)

2. **Create New Application**
   - Click "+ New" or "New Resource"
   - Select "Application"
   - Choose "Public Repository" or connect your GitHub/GitLab account

3. **Configure Repository**
   - **Repository URL:** `https://github.com/yourusername/math-api.git`
   - **Branch:** `main` (or `master`)
   - **Build Pack:** Dockerfile (auto-detected)

4. **Configure Application Settings**
   - **Port:** `8000` (Important!)
   - **Health Check Path:** `/health`
   - **Build Method:** Dockerfile (should be auto-detected)

5. **Configure Domain (Optional)**
   - Add your domain or subdomain
   - Example: `math-api.yourdomain.com`
   - Coolify will automatically provision SSL certificate

6. **Deploy**
   - Click "Deploy" or "Save & Deploy"
   - Watch the build logs
   - Wait for deployment to complete

#### Option B: Using Git Push Deploy

If you have Git-based deployment enabled in Coolify:

```bash
# Add Coolify as a git remote
git remote add coolify <coolify-git-url>

# Push to deploy
git push coolify main
```

### 3. Verify Deployment

Once deployed, test your endpoints:

```bash
# Replace with your actual domain
DOMAIN="https://math-api.yourdomain.com"

# Test health check
curl $DOMAIN/health

# Test API
curl -X POST $DOMAIN/calculate \
  -H "Content-Type: application/json" \
  -d '{"x": 10, "y": 5}'
```

Expected response:
```json
{
  "sum": 15.0,
  "mult": 50.0
}
```

### 4. Access API Documentation

Visit these URLs (replace with your domain):
- Swagger UI: `https://math-api.yourdomain.com/docs`
- ReDoc: `https://math-api.yourdomain.com/redoc`

## Configuration Details

### Environment Variables

This application doesn't require any environment variables for basic operation, but you can add these in Coolify if needed:

- `ENVIRONMENT`: `production`
- `LOG_LEVEL`: `info`

To add environment variables in Coolify:
1. Go to your application
2. Click "Environment Variables"
3. Add key-value pairs
4. Redeploy

### Port Configuration

**Important:** Make sure Coolify is configured to expose port **8000**

In Coolify:
- Go to "Network" settings
- Set "Port" to `8000`
- Coolify will automatically handle the reverse proxy

### Health Check

Coolify will use the `/health` endpoint to monitor your application:
- **Path:** `/health`
- **Interval:** 30s
- **Timeout:** 10s
- **Retries:** 3

### Automatic Deployments

To enable automatic deployments on git push:

1. In Coolify, go to your application settings
2. Enable "Automatic Deployment"
3. Coolify will create a webhook
4. Add the webhook to your Git repository settings
5. Now every push to main branch will trigger a deployment

## Troubleshooting

### Build Failed

1. Check Coolify build logs
2. Ensure Dockerfile is in the root directory
3. Verify all files are committed to git

### Application Not Starting

1. Check application logs in Coolify
2. Verify port 8000 is exposed
3. Check health endpoint is responding

### Cannot Access API

1. Verify domain DNS is pointing to your VPS
2. Check Coolify reverse proxy configuration
3. Ensure firewall allows port 80/443
4. Check SSL certificate status

### View Logs

In Coolify dashboard:
- Click on your application
- Go to "Logs" tab
- View build logs and runtime logs

## Updating the Application

```bash
# Make your changes
git add .
git commit -m "Update: your changes"
git push origin main
```

If automatic deployments are enabled, Coolify will automatically rebuild and redeploy.

Otherwise, go to Coolify dashboard and click "Deploy" button.

## Rollback

If something goes wrong:
1. Go to Coolify dashboard
2. Click on your application
3. Go to "Deployments" tab
4. Select a previous successful deployment
5. Click "Rollback"

## Monitoring

Coolify provides:
- Application status monitoring
- Resource usage (CPU, Memory)
- Request logs
- Health check status

Access these from your application dashboard in Coolify.

## SSL Certificate

Coolify automatically provisions SSL certificates via Let's Encrypt:
- Certificates auto-renew
- Supports multiple domains
- Forces HTTPS redirect (configurable)

## Performance Tips

1. **Enable Docker layer caching** in Coolify for faster builds
2. **Set appropriate resource limits** (CPU, Memory) in Coolify
3. **Use CDN** for static assets if needed
4. **Monitor logs** for performance issues

## Support

- Coolify Documentation: https://coolify.io/docs
- This API Documentation: `/docs` endpoint
- GitHub Issues: Create issue in your repository