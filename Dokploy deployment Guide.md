# Dokploy Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Git Repository

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Math & Chat API"

# Add your remote repository
git remote add origin https://github.com/yourusername/math-chat-api.git

# Push to main branch
git push -u origin main
```

### 2. Deploy on Dokploy

#### Step-by-Step Guide

1. **Login to Dokploy Dashboard**
   - Navigate to your Dokploy dashboard (usually `https://dokploy.yourdomain.com`)
   - Or access via IP: `http://your-vps-ip:3000`

2. **Create New Project** (if needed)
   - Click "Projects" in the sidebar
   - Click "+ New Project"
   - Enter project name (e.g., "math-chat-api")
   - Click "Create"

3. **Create New Application**
   - Inside your project, click "+ Add Service"
   - Select "Application"
   - Choose "Git" as source

4. **Configure Git Repository**
   - **Provider:** GitHub / GitLab / Gitea (or paste Git URL)
   - **Repository URL:** `https://github.com/yourusername/math-chat-api.git`
   - **Branch:** `main` (or `master`)
   - **Build Type:** Dockerfile (auto-detected)

5. **Configure Application Settings**
   - **Application Name:** `math-chat-api`
   - **Build Path:** `/` (root directory)
   - **Dockerfile Path:** `./Dockerfile` (should be auto-detected)

6. **Configure Port**
   - Click on "Ports" tab
   - **Container Port:** `8000`
   - **Published Port:** Leave empty (Dokploy will auto-assign)
   - **Protocol:** HTTP

7. **Configure Environment Variables**
   - Click on "Environment" tab
   - Add the following variables:
     - **Key:** `BYTEZ_API_KEY`
     - **Value:** `03ba600d1e40ba3aaa1b44538b3543a0` (or your own key)
   - Click "Add Variable"

8. **Configure Domain (Optional)**
   - Click on "Domains" tab
   - Click "+ Add Domain"
   - Enter your domain: `math-api.yourdomain.com`
   - Select "Enable SSL" (Let's Encrypt)
   - Click "Add"

9. **Configure Health Check (Optional but Recommended)**
   - Click on "Advanced" or "Health Check" tab
   - **Path:** `/health`
   - **Interval:** `30s`
   - **Timeout:** `10s`
   - **Retries:** `3`

10. **Deploy**
    - Click "Deploy" button
    - Watch the build logs in real-time
    - Wait for "Deployment successful" message

### 3. Verify Deployment

Once deployed, test your endpoints:

```bash
# Replace with your actual domain or IP
DOMAIN="https://math-api.yourdomain.com"

# Test health check
curl $DOMAIN/health

# Test math calculation
curl -X POST $DOMAIN/calculate \
  -H "Content-Type: application/json" \
  -d '{"x": 10, "y": 5}'

# Test chat
curl -X POST $DOMAIN/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello!"}'
```

Expected responses:
```json
// Health check
{"status": "healthy"}

// Calculate
{"sum": 15.0, "mult": 50.0}

// Chat
{"answer": "Hello! How can I help you today?", "error": null}
```

### 4. Access API Documentation

Visit these URLs (replace with your domain):
- Swagger UI: `https://math-api.yourdomain.com/docs`
- ReDoc: `https://math-api.yourdomain.com/redoc`

## Dokploy Configuration Details

### Application Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Build Type | Dockerfile | Auto-detected |
| Container Port | 8000 | Internal port |
| Health Check Path | /health | Recommended |
| Restart Policy | always | Recommended |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BYTEZ_API_KEY` | Bytez API key for chat | Yes (default provided) |
| `ENVIRONMENT` | Application environment | No |

### Port Configuration

Dokploy will automatically:
- Detect that your app runs on port 8000
- Assign a public port or use domain routing
- Handle SSL termination if domain is configured
- Set up reverse proxy with Traefik

### Domain & SSL

Dokploy uses Traefik for routing and Let's Encrypt for SSL:
- Add your domain in the "Domains" tab
- Enable SSL/TLS
- Certificates auto-renew
- Automatic HTTPS redirect

## Automatic Deployments (CI/CD)

### Option 1: Webhook (Recommended)

1. In Dokploy, go to your application
2. Click "Settings" → "Webhooks"
3. Copy the webhook URL
4. In your Git repository (GitHub/GitLab):
   - Go to Settings → Webhooks
   - Paste the Dokploy webhook URL
   - Select "Push events"
   - Click "Add webhook"

Now every push to your main branch will trigger automatic deployment!

### Option 2: Git Polling

1. In Dokploy, go to your application
2. Click "Settings" → "Build & Deploy"
3. Enable "Auto Deploy"
4. Set polling interval (e.g., 5 minutes)

## Monitoring & Logs

### View Logs

1. In Dokploy dashboard
2. Go to your application
3. Click "Logs" tab
4. View real-time logs or historical logs

### View Metrics

1. Click "Metrics" tab
2. Monitor:
   - CPU usage
   - Memory usage
   - Network I/O
   - Request count

### View Deployments History

1. Click "Deployments" tab
2. See all previous deployments
3. Click on any deployment to see logs
4. Rollback if needed

## Updating the Application

```bash
# Make your changes locally
git add .
git commit -m "Update: your changes"
git push origin main
```

If webhooks are enabled, Dokploy will automatically:
1. Pull the latest code
2. Rebuild the Docker image
3. Deploy the new version
4. Zero-downtime deployment

## Rollback

If something goes wrong:

1. Go to Dokploy dashboard
2. Click on your application
3. Go to "Deployments" tab
4. Find a successful previous deployment
5. Click "Redeploy" on that version

## Scaling

### Vertical Scaling (Resources)

1. Go to your application settings
2. Click "Resources" tab
3. Set limits:
   - **CPU Limit:** e.g., `1.0` (1 core)
   - **Memory Limit:** e.g., `512M` or `1G`
   - **CPU Reservation:** e.g., `0.25`
   - **Memory Reservation:** e.g., `256M`

### Horizontal Scaling (Multiple Instances)

1. Go to your application settings
2. Click "Scale" or "Replicas"
3. Set number of replicas (e.g., 3)
4. Dokploy will load-balance between instances

## Troubleshooting

### Build Failed

**Check build logs:**
1. Go to application → Logs
2. Filter by "Build logs"
3. Look for error messages

**Common issues:**
- Dockerfile not found → Ensure Dockerfile is in root directory
- Dependencies failed → Check requirements.txt
- Out of memory → Increase build resources

### Application Not Starting

**Check runtime logs:**
1. Go to application → Logs
2. Filter by "Application logs"

**Common issues:**
- Port mismatch → Ensure port 8000 is configured
- Missing environment variables → Check Environment tab
- Health check failing → Verify /health endpoint works

### Cannot Access API

**Check domain/routing:**
1. Verify domain DNS points to your VPS
2. Check Traefik dashboard for routing rules
3. Ensure SSL certificate is issued
4. Check firewall allows ports 80/443

**Check application status:**
1. Go to your application
2. Verify status is "Running" (green)
3. Check exposed ports

### Health Check Failing

1. Test health endpoint manually:
   ```bash
   curl http://your-app:8000/health
   ```
2. Adjust health check settings:
   - Increase timeout
   - Increase interval
   - Reduce retry count

### High Memory Usage

1. Set memory limits in Resources tab
2. Monitor in Metrics
3. Consider optimization or scaling

## Advanced Configuration

### Custom Dockerfile

If you need to modify the Dockerfile:
1. Edit locally
2. Commit and push
3. Redeploy

### Multiple Environments

Deploy separate applications for different environments:
- `math-api-dev` (development)
- `math-api-staging` (staging)
- `math-api-prod` (production)

Each with different:
- Branches (dev, staging, main)
- Environment variables
- Domains

### Using Docker Compose (Alternative)

If you prefer docker-compose over Dockerfile:
1. In Dokploy, select "Docker Compose" build type
2. Dokploy will use your docker-compose.yml
3. Configure environment variables through Dokploy UI

### Database Integration

To add a database:
1. In your project, click "+ Add Service"
2. Select "Database"
3. Choose PostgreSQL/MySQL/MongoDB/Redis
4. Configure and deploy
5. Add database connection string to your app's environment variables

## Backup & Recovery

### Backup Configuration

1. Export your application config:
   - Click "Settings" → "Export"
   - Save JSON file

### Database Backups

If using Dokploy databases:
1. Go to database service
2. Click "Backups"
3. Configure automatic backups
4. Set retention period

## Security Best Practices

1. **Use Environment Variables** for sensitive data
2. **Enable SSL/TLS** for all domains
3. **Set Resource Limits** to prevent DoS
4. **Regular Updates** - keep application updated
5. **Monitor Logs** for suspicious activity
6. **Use Strong API Keys** - rotate periodically

## Performance Optimization

1. **Enable Caching** in Traefik
2. **Set Appropriate Resource Limits**
3. **Use Health Checks** for faster failure detection
4. **Monitor Metrics** regularly
5. **Scale Horizontally** if needed

## Dokploy vs Coolify

**Similarities:**
- Both use Docker
- Both support Dockerfile deployment
- Both handle SSL automatically
- Both have web UI

**Dokploy Advantages:**
- More modern UI
- Better real-time logs
- Built-in metrics
- Easier scaling
- More active development

## Support & Resources

- Dokploy Documentation: https://docs.dokploy.com
- Dokploy GitHub: https://github.com/dokploy/dokploy
- Community Discord: Check Dokploy website
- This API Docs: `/docs` endpoint

## Quick Commands Reference

```bash
# View logs (via SSH to VPS)
docker logs -f <container-name>

# Check running containers
docker ps

# Restart application
# (Do this via Dokploy UI instead)

# Check Dokploy status
docker ps | grep dokploy

# Access Dokploy container
docker exec -it dokploy sh
```

## Next Steps

1. ✅ Deploy your application
2. ✅ Configure domain and SSL
3. ✅ Set up automatic deployments (webhooks)
4. ✅ Monitor logs and metrics
5. ✅ Set up resource limits
6. ✅ Configure backups (if using databases)
7. ✅ Test your endpoints

---

**Need Help?**
- Check Dokploy logs in the dashboard
- Review this guide
- Check README.md for API details
- Visit Dokploy documentation

**Happy Deploying! 🚀**