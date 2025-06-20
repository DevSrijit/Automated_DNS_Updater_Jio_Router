# Dockerized JIO Router DNS Updater

A containerized Selenium automation script for updating JIO Fiber router DNS settings. Optimized for **Raspberry Pi Zero 2W** and other ARM-based devices.

## 🌟 Features

- **Dockerized**: Runs in an isolated container for better performance and security
- **ARM Optimized**: Specifically optimized for Raspberry Pi Zero 2W
- **Auto-restart**: Container automatically restarts on failure
- **Resource Limited**: Memory and CPU limits to prevent system overload
- **Comprehensive Logging**: Detailed logs with timestamps
- **Health Checks**: Built-in health monitoring
- **Graceful Shutdown**: Proper cleanup on container stop

## 🔧 Prerequisites

### On Raspberry Pi Zero 2W:

1. **Install Docker**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

2. **Install Docker Compose** (if not included):
   ```bash
   sudo pip3 install docker-compose
   ```

3. **Reboot** to apply Docker group changes:
   ```bash
   sudo reboot
   ```

## 🚀 Quick Start

1. **Clone or download this repository** to your Raspberry Pi

2. **Configure your settings**:
   ```bash
   cp .env.example .env
   nano .env  # Edit with your router credentials and DNS preferences
   ```

3. **Run the setup script**:
   ```bash
   ./start.sh
   ```

That's it! The DNS updater will now run automatically in the background.

## ⚙️ Configuration

Edit the `.env` file with your specific settings:

```bash
# Router Configuration
router_url=http://192.168.29.1          # Your JIO router IP
user_name=admin                         # Router username
password=your_router_password_here      # Router password

# IPv4 DNS Servers (Cloudflare DNS by default)
ipv4_dns_server1=1.1.1.1
ipv4_dns_server2=1.0.0.1

# IPv6 DNS Servers (Cloudflare DNS by default)  
ipv6_dns_server1=2606:4700::1111
ipv6_dns_server2=2606:4700:4700::1001

# Update interval in seconds (28800 = 8 hours)
update_interval_time=28800
```

### Popular DNS Servers:

| Provider | IPv4 Primary | IPv4 Secondary | IPv6 Primary | IPv6 Secondary |
|----------|-------------|----------------|-------------|----------------|
| **Cloudflare** | 1.1.1.1 | 1.0.0.1 | 2606:4700::1111 | 2606:4700:4700::1001 |
| **Google** | 8.8.8.8 | 8.8.4.4 | 2001:4860:4860::8888 | 2001:4860:4860::8844 |
| **Quad9** | 9.9.9.9 | 149.112.112.112 | 2620:fe::fe | 2620:fe::9 |

## 📊 Management Commands

```bash
# View real-time logs
docker-compose logs -f dns-updater

# Check service status
docker-compose ps

# Stop the service
docker-compose down

# Restart the service
docker-compose restart

# Update and restart (after code changes)
docker-compose up -d --build

# View resource usage
docker stats jio-dns-updater
```

## 🔍 Monitoring

### Log Files
- Container logs: `docker-compose logs dns-updater`
- Persistent logs: `./logs/dns_updater.log` (if logs directory exists)

### Health Checks
The container includes built-in health monitoring:
```bash
docker inspect --format='{{.State.Health.Status}}' jio-dns-updater
```

## 🏗️ Architecture

### Container Specifications:
- **Base Image**: Python 3.11 slim (ARM compatible)
- **Browser**: Chromium (optimized for ARM)
- **Memory Limit**: 512MB (suitable for Pi Zero 2W)
- **CPU Limit**: 1.0 cores
- **Network**: Isolated bridge network
- **Security**: Non-root user execution

### Optimization for Raspberry Pi Zero 2W:
- Minimal resource usage
- Chromium browser optimizations
- Headless operation
- Memory-efficient Python options
- Disabled unnecessary browser features

## 🛠️ Troubleshooting

### Container Won't Start
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs dns-updater

# Check system resources
free -h
df -h
```

### Memory Issues on Pi Zero 2W
```bash
# Reduce update frequency in .env
update_interval_time=43200  # 12 hours instead of 8

# Monitor memory usage
docker stats --no-stream
```

### DNS Update Failures
```bash
# Check if router is accessible
ping 192.168.29.1

# Verify credentials in .env file
cat .env

# Test with manual run
docker-compose run --rm dns-updater python main.py
```

### Performance Optimization
```bash
# Clean up unused Docker resources
docker system prune -f

# Monitor Pi temperature
vcgencmd measure_temp
```

## 🔒 Security Features

- **Isolated Environment**: Runs in containerized environment
- **Non-root Execution**: Container runs as unprivileged user
- **No Host Network Access**: Uses bridge networking
- **Credential Protection**: Environment variables not exposed in logs
- **Minimal Attack Surface**: Only necessary packages installed

## 📈 Performance Notes

### Raspberry Pi Zero 2W Specifications:
- **CPU**: Quad-core ARM Cortex-A53 @ 1GHz
- **RAM**: 512MB
- **Recommended Settings**:
  - Update interval: 8+ hours
  - Monitor temperature regularly
  - Ensure adequate power supply (2.5A recommended)

### Resource Usage:
- **Memory**: ~200-300MB during operation
- **CPU**: Peaks during browser operations, idle otherwise
- **Storage**: ~1GB for container and dependencies

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use. Use at your own risk. Always ensure you have proper authorization to modify router settings.


