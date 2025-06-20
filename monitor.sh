#!/bin/bash

# DNS Updater Monitoring Script
# Quick status check for the containerized DNS updater

echo "🔍 JIO DNS Updater Status"
echo "========================"

# Check if container is running
if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "jio-dns-updater"; then
    echo "✅ Container Status: Running"
    
    # Get container uptime
    uptime=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep "jio-dns-updater" | awk '{print $2, $3, $4}')
    echo "⏱️  Uptime: $uptime"
    
    # Check health status
    health=$(docker inspect --format='{{.State.Health.Status}}' jio-dns-updater 2>/dev/null || echo "unknown")
    echo "🏥 Health: $health"
    
    # Show resource usage
    echo ""
    echo "📊 Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" jio-dns-updater
    
    # Show recent logs (last 10 lines)
    echo ""
    echo "📋 Recent Logs (last 10 lines):"
    echo "--------------------------------"
    docker logs --tail 10 jio-dns-updater
    
else
    echo "❌ Container Status: Not Running"
    echo ""
    echo "🔧 To start the service:"
    echo "   ./start.sh"
    echo ""
    echo "📋 To check what went wrong:"
    echo "   docker compose logs dns-updater"
fi

echo ""
echo "🛠️  Management Commands:"
echo "   Status:    ./monitor.sh"
echo "   Logs:      docker compose logs -f dns-updater"
echo "   Restart:   docker compose restart"
echo "   Stop:      docker compose down"
