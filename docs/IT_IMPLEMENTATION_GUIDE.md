# OCSS Command Center - IT Implementation & Deployment Guide

## Quick Start for IT Teams

This guide is designed for IT administrators and infrastructure teams responsible for deploying and maintaining the OCSS Command Center in production environments.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Installation Methods](#installation-methods)
3. [Configuration & Setup](#configuration--setup)
4. [Security Hardening](#security-hardening)
5. [Monitoring & Alerting](#monitoring--alerting)
6. [Disaster Recovery](#disaster-recovery)
7. [Troubleshooting](#troubleshooting)
8. [Commands Reference](#commands-reference)

---

## Pre-Deployment Checklist

### Infrastructure Requirements
- [ ] Server provisioned (Ubuntu 22.04+ or RHEL 8+)
- [ ] Network connectivity verified (1+ Mbps minimum)
- [ ] DNS record created (if applicable)
- [ ] SSL certificate obtained and staged
- [ ] Firewall rules configured (see section 4.1)
- [ ] Backup system in place
- [ ] Monitoring tools installed

### Software Requirements
- [ ] Python 3.8+ installed
- [ ] pip/venv available
- [ ] Docker installed (if containerized)
- [ ] Git installed and configured
- [ ] Nginx/Apache installed (for reverse proxy)
- [ ] PostgreSQL/MySQL ready (for Phase 2)

### Documentation
- [ ] Backups of all configuration files
- [ ] Network diagram updated
- [ ] Access control list documented
- [ ] Incident response plan reviewed
- [ ] Support escalation procedures defined

---

## Installation Methods

### Method 1: Direct Python Installation (Easiest)

**Time to Deploy:** 10-15 minutes

**Best For:** Small deployments, non-containerized environments

**Steps:**

```bash
# 1. Connect to server and update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and system dependencies
sudo apt install -y python3 python3-pip python3-venv \
    git curl wget build-essential libpq-dev

# 3. Create application directory
sudo mkdir -p /opt/ocss-command-center
sudo chown $USER:$USER /opt/ocss-command-center

# 4. Clone repository
cd /opt/ocss-command-center
git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git .

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r app/requirements.txt

# 7. Create systemd service file
sudo tee /etc/systemd/system/ocss-command-center.service > /dev/null <<EOF
[Unit]
Description=OCSS Command Center Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ocss-command-center
Environment="PATH=/opt/ocss-command-center/venv/bin"
ExecStart=/opt/ocss-command-center/venv/bin/streamlit run app/app.py \
    --server.port=8501 \
    --server.address=127.0.0.1 \
    --server.headless=true \
    --logger.level=info
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 8. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ocss-command-center
sudo systemctl start ocss-command-center

# 9. Verify status
sudo systemctl status ocss-command-center

# 10. Check application is running
curl http://127.0.0.1:8501
```

**Verification:**
```bash
# Check service status
sudo systemctl status ocss-command-center

# Monitor logs in real-time
sudo journalctl -u ocss-command-center -f
```

### Method 2: Docker Containerized (Recommended for Production)

**Time to Deploy:** 20-30 minutes

**Best For:** Production environments, scaling, isolation

**Steps:**

```bash
# 1. Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# 2. Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# 3. Clone and navigate to repository
git clone https://github.com/arhawkins01-dotcom/ocss-command-center.git
cd ocss-command-center

# 4. Create Dockerfile (save as Dockerfile in root)
cat > Dockerfile <<'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ .

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--logger.level=info"]
EOF

# 5. Create docker-compose.yml
cat > docker-compose.yml <<'EOF'
version: '3.8'

services:
  ocss-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ocss-command-center
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
      - TZ=UTC
    restart: unless-stopped
    networks:
      - ocss-network
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "10"

networks:
  ocss-network:
    driver: bridge
EOF

# 6. Build base image
docker build -t ocss-command-center:1.0.0 .

# 7. Tag for local repository
docker tag ocss-command-center:1.0.0 ocss-command-center:latest

# 8. Start containers
docker-compose up -d

# 9. Verify container is running
docker-compose ps
docker logs ocss-command-center

# 10. Test application
curl http://localhost:8501

# 11. Set up Docker to start on boot
sudo systemctl enable docker
sudo systemctl enable docker.service
```

**Docker Compose Commands:**

```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs -f ocss-app

# Restart service
docker-compose restart ocss-app

# Update application
docker-compose down
git pull origin main
docker-compose up -d --build

# Check resource usage
docker stats ocss-command-center

# Execute command in container
docker-compose exec ocss-app bash
```

### Method 3: Kubernetes Deployment (Enterprise)

**Time to Deploy:** 45-60 minutes

**Best For:** Large-scale deployments, high availability

**Kubernetes manifests (save in k8s/ directory):**

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ocss
---

# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ocss-command-center
  namespace: ocss
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: ocss-command-center
  template:
    metadata:
      labels:
        app: ocss-command-center
    spec:
      containers:
      - name: ocss-app
        image: ocss-command-center:1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8501
          name: web
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 10
          periodSeconds: 5
---

# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ocss-command-center
  namespace: ocss
spec:
  type: LoadBalancer
  selector:
    app: ocss-command-center
  ports:
  - port: 80
    targetPort: 8501
    protocol: TCP
---

# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ocss-ingress
  namespace: ocss
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - ocss.yourdomain.com
    secretName: ocss-tls
  rules:
  - host: ocss.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ocss-command-center
            port:
              number: 80
```

**Deploy to Kubernetes:**

```bash
# Apply manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n ocss
kubectl get svc -n ocss

# Monitor rollout
kubectl rollout status deployment/ocss-command-center -n ocss

# View logs
kubectl logs -f -n ocss deployment/ocss-command-center
```

---

## Configuration & Setup

### Configuration Files

**Location:** `/opt/ocss-command-center/` or `/app/` in Docker

**Key Configuration Points:**

```python
# streamlit_config.toml (create in ~/.streamlit/)
[server]
port = 8501
address = "127.0.0.1"  # Use 0.0.0.0 for Docker
headless = true
enableXsrfProtection = true
maxUploadSize = 200  # MB

[client]
toolbarMode = "minimal"
showErrorDetails = false

[logger]
level = "info"

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

**Environment Variables:**

```bash
# Create .env file
cat > /opt/ocss-command-center/.env <<EOF
# Application
APP_ENV=production
APP_PORT=8501
APP_HOST=0.0.0.0

# Database (Phase 2)
DATABASE_URL=postgresql://user:password@localhost:5432/ocss
DATABASE_POOL_SIZE=20
DATABASE_TIMEOUT=30

# Security
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/ocss/app.log

# File Upload
MAX_UPLOAD_SIZE=209715200  # 200MB in bytes
UPLOAD_DIR=/var/data/ocss/uploads

# SMTP (for future notifications)
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
SMTP_FROM=noreply@yourdomain.com

# Backup
BACKUP_ENABLED=true
BACKUP_PATH=/backup/ocss
BACKUP_SCHEDULE="0 2 * * *"  # 2 AM daily
EOF

# Set permissions
chmod 600 /opt/ocss-command-center/.env
```

### Nginx Reverse Proxy Configuration

```nginx
# /etc/nginx/sites-available/ocss-command-center
upstream streamlit_backend {
    server 127.0.0.1:8501;
    keepalive 32;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=upload:10m rate=2r/s;

server {
    listen 80;
    listen [::]:80;
    server_name ocss.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name ocss.yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/ssl/certs/ocss.yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/ocss.yourdomain.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Logging
    access_log /var/log/nginx/ocss-access.log;
    error_log /var/log/nginx/ocss-error.log;

    # Client max upload size
    client_max_body_size 200M;

    # Root location
    location / {
        limit_req zone=general burst=20 nodelay;

        proxy_pass http://streamlit_backend;
        proxy_http_version 1.1;
        
        # Websocket support (required for Streamlit)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffering
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # File upload endpoint (with rate limiting)
    location /upload {
        limit_req zone=upload burst=5 nodelay;
        proxy_pass http://streamlit_backend;
        # ... (same headers as above)
    }

    # Deny access to sensitive files
    location ~ /\.env$ {
        deny all;
    }

    location ~ /\.git {
        deny all;
    }

    location ~ /(logs|data|backup)/ {
        deny all;
    }

    # Health check endpoint
    location /health {
        access_log off;
        proxy_pass http://streamlit_backend;
    }
}
```

**Enable Nginx site:**

```bash
sudo ln -s /etc/nginx/sites-available/ocss-command-center \
           /etc/nginx/sites-enabled/

sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

---

## Security Hardening

### Step 1: Firewall Configuration

```bash
# UFW (Ubuntu Uncomplicated Firewall)
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (CRITICAL - do this first!)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow from specific IPs only (optional)
sudo ufw allow from 192.168.1.0/24 to any port 8501

# View rules
sudo ufw status numbered
```

### Step 2: Fail2Ban Installation

```bash
# Install Fail2Ban
sudo apt install fail2ban

# Create local configuration
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true

[nginx-botsearch]
enabled = true
EOF

# Restart Fail2Ban
sudo systemctl restart fail2ban
sudo fail2ban-client status
```

### Step 3: SSL/TLS Certificate Management

```bash
# Option A: Let's Encrypt with Certbot (Free, Automated)
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot certonly --nginx -d ocss.yourdomain.com

# Auto-renewal (runs automatically via systemd timer)
sudo certbot renew --dry-run

# Check renewal status
sudo systemctl status certbot.timer
```

### Step 4: System Hardening

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install UFW and fail2ban (already done above)

# Disable unnecessary services
sudo systemctl disable avahi-daemon
sudo systemctl disable cups

# Enable automatic security updates
sudo apt install unattended-upgrades
sudo systemctl enable unattended-upgrades

# SSH hardening
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# TimeZone and NTP
sudo timedatectl set-timezone UTC
sudo timedatectl set-ntp on
```

### Step 5: Data Encryption

```bash
# Create encrypted data directory
sudo apt install cryptsetup

# Create loop device
sudo dd if=/dev/zero of=/var/lib/ocss.img bs=1M count=5000
sudo losetup -f /var/lib/ocss.img

# Setup LUKS encryption
sudo cryptsetup luksFormat /dev/loop0
sudo cryptsetup luksOpen /dev/loop0 ocss-data

# Format and mount
sudo mkfs.ext4 /dev/mapper/ocss-data
sudo mkdir -p /mnt/ocss-data
sudo mount /dev/mapper/ocss-data /mnt/ocss-data
sudo chown www-data:www-data /mnt/ocss-data
sudo chmod 700 /mnt/ocss-data

# Add to fstab for automatic mounting
echo "ocss-data /mnt/ocss-data ext4 defaults 0 2" | sudo tee -a /etc/crypttab
```

---

## Monitoring & Alerting

### System Monitoring Setup

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Install Prometheus node exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
sudo cp node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter

# Create systemd service
sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
```

### Application Logging

```bash
# Create log directory
sudo mkdir -p /var/log/ocss
sudo chown www-data:www-data /var/log/ocss
sudo chmod 755 /var/log/ocss

# Enable application logging in systemd service
# Edit: /etc/systemd/system/ocss-command-center.service

# View logs
journalctl -u ocss-command-center -n 50  # Last 50 lines
journalctl -u ocss-command-center -f     # Follow in real-time
journalctl -u ocss-command-center --since today

# Log rotation
sudo tee /etc/logrotate.d/ocss > /dev/null <<EOF
/var/log/ocss/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload ocss-command-center > /dev/null 2>&1 || true
    endscript
}
EOF
```

### Alert Configuration

```bash
# Example: Send alert if disk usage >80%
cat > /usr/local/bin/check_disk.sh <<'EOF'
#!/bin/bash
THRESHOLD=80
USAGE=$(df -h /var | awk 'NR==2 {print $(NF-1)}' | sed 's/%//')

if [ $USAGE -gt $THRESHOLD ]; then
    echo "ALERT: Disk usage is ${USAGE}%" | mail -s "OCSS Alert" admin@yourdomain.com
fi
EOF

chmod +x /usr/local/bin/check_disk.sh

# Add to crontab
echo "*/30 * * * * /usr/local/bin/check_disk.sh" | crontab -
```

---

## Disaster Recovery

### Backup Strategy

```bash
# Create backup script
cat > /usr/local/bin/backup-ocss.sh <<'EOF'
#!/bin/bash

BACKUP_DIR="/backup/ocss"
DATE=$(date +%Y%m%d_%H%M%S)
SOURCE_DIR="/opt/ocss-command-center"
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application
tar -czf $BACKUP_DIR/app_$DATE.tar.gz $SOURCE_DIR/app/

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz \
    /etc/nginx/sites-available/ocss-command-center \
    /etc/systemd/system/ocss-command-center.service

# Backup database (Phase 2)
if command -v pg_dump &> /dev/null; then
    pg_dump ocss | gzip > $BACKUP_DIR/db_$DATE.sql.gz
fi

# Upload to S3 (if configured)
# aws s3 cp $BACKUP_DIR/ s3://ocss-backups/ --recursive

# Cleanup old backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Log backup
echo "Backup completed: $DATE" >> /var/log/ocss/backup.log
EOF

chmod +x /usr/local/bin/backup-ocss.sh

# Schedule daily backups at 2 AM
echo "0 2 * * * /usr/local/bin/backup-ocss.sh" | crontab -
```

### Recovery Procedures

```bash
# Restore from backup
BACKUP_FILE="/backup/ocss/app_20260218_020000.tar.gz"

# Stop application
sudo systemctl stop ocss-command-center

# Restore files
sudo tar -xzf $BACKUP_FILE -C /

# Restore permissions
sudo chown -R www-data:www-data /opt/ocss-command-center

# Start application
sudo systemctl start ocss-command-center

# Verify
sudo systemctl status ocss-command-center
curl http://127.0.0.1:8501

# Restore database (Phase 2)
# gunzip < /backup/ocss/db_20260218_020000.sql.gz | psql ocss
```

---

## Troubleshooting

### Common Issues

**Issue: Application won't start**

```bash
# Check service status
sudo systemctl status ocss-command-center

# View detailed error logs
sudo journalctl -u ocss-command-center -n 100

# Check port in use
sudo lsof -i :8501

# Manually test python
cd /opt/ocss-command-center
source venv/bin/activate
python3 -c "import streamlit; print(streamlit.__version__)"
```

**Issue: High memory usage**

```bash
# Monitor memory
watch -n 1 'free -m'

# Check process memory
ps aux | grep streamlit

# Restart service
sudo systemctl restart ocss-command-center

# Review application logs for memory leaks
journalctl -u ocss-command-center | grep -i memory
```

**Issue: Slow performance**

```bash
# Check disk I/O
iostat -x 1 5

# Check network connectivity
ping -c 5 8.8.8.8
mtr -r -c 10 ocss.yourdomain.com

# Monitor system load
uptime
top

# Check CSS/JS loading in browser
# Inspector → Network tab → Look for slow requests
```

**Issue: SSL certificate not working**

```bash
# Test certificate
openssl s_client -connect ocss.yourdomain.com:443

# Check certificate expiration
echo | openssl s_client -servername ocss.yourdomain.com -connect ocss.yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates

# Certbot renewal
sudo certbot renew --force-renewal

# Nginx reload
sudo systemctl reload nginx
```

---

## Commands Reference

### Service Management

```bash
# Start service
sudo systemctl start ocss-command-center

# Stop service
sudo systemctl stop ocss-command-center

# Restart service
sudo systemctl restart ocss-command-center

# View service status
sudo systemctl status ocss-command-center

# Enable on boot
sudo systemctl enable ocss-command-center

# Disable on boot
sudo systemctl disable ocss-command-center

# View recent logs
sudo journalctl -u ocss-command-center -n 50

# Follow logs live
sudo journalctl -u ocss-command-center -f

# View logs from specific time
sudo journalctl -u ocss-command-center --since "2 hours ago"
```

### Docker Commands

```bash
# Build image
docker build -t ocss-command-center:1.0.0 .

# Run container
docker run -d -p 8501:8501 --name ocss-app ocss-command-center:1.0.0

# View running containers
docker ps

# View all containers
docker ps -a

# Stop container
docker stop ocss-app

# Start container
docker start ocss-app

# Remove container
docker rm ocss-app

# View logs
docker logs ocss-app
docker logs -f ocss-app

# Execute command in container
docker exec -it ocss-app bash

# Get container stats
docker stats ocss-app

# Docker Compose (from project directory)
docker-compose up -d
docker-compose ps
docker-compose logs -f
docker-compose down
```

### System Commands

```bash
# Check disk space
df -h

# Check memory
free -m

# Check CPU usage
top
htop

# Check network
netstat -an | grep 8501
ss -tlnp | grep 8501

# Check firewall
sudo ufw status
sudo ufw status numbered

# See what's using a port
sudo lsof -i :8501
sudo netstat -tlnp | grep :8501
```

---

## Support & Escalation

**For deployment issues:** Contact the development team with logs from `journalctl`

**For performance issues:** Monitor metrics and compare with baseline in Technical Guide

**For security concerns:** Run security audit and follow Phase 1 recommendations

---

**Document Version:** 1.0  
**Last Updated:** February 18, 2026  
**Approved for:** IT Administrative Personnel
