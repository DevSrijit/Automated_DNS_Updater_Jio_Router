#!/bin/bash

# DNS Updater Configuration Backup/Restore Script

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

case "$1" in
    backup)
        echo "📦 Creating configuration backup..."
        mkdir -p "$BACKUP_DIR"
        
        if [ -f ".env" ]; then
            cp .env "$BACKUP_DIR/.env_$TIMESTAMP"
            echo "✅ Backup created: $BACKUP_DIR/.env_$TIMESTAMP"
        else
            echo "❌ No .env file found to backup"
            exit 1
        fi
        
        # Also backup docker-compose.yml if it was modified
        if [ -f "docker-compose.yml" ]; then
            cp docker-compose.yml "$BACKUP_DIR/docker-compose_$TIMESTAMP.yml"
            echo "✅ Docker compose backup: $BACKUP_DIR/docker-compose_$TIMESTAMP.yml"
        fi
        
        echo "📂 Available backups:"
        ls -la "$BACKUP_DIR/"
        ;;
        
    restore)
        echo "📂 Available backups:"
        if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
            echo "❌ No backups found in $BACKUP_DIR"
            exit 1
        fi
        
        ls -la "$BACKUP_DIR/"
        echo ""
        echo "🔄 To restore a backup, copy the desired file:"
        echo "   cp $BACKUP_DIR/.env_YYYYMMDD_HHMMSS .env"
        echo "   cp $BACKUP_DIR/docker-compose_YYYYMMDD_HHMMSS.yml docker-compose.yml"
        ;;
        
    list)
        echo "📂 Available backups:"
        if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
            echo "❌ No backups found"
        else
            ls -la "$BACKUP_DIR/"
        fi
        ;;
        
    clean)
        if [ -d "$BACKUP_DIR" ]; then
            echo "🗑️  Cleaning old backups (keeping last 5)..."
            cd "$BACKUP_DIR"
            ls -t .env_* 2>/dev/null | tail -n +6 | xargs rm -f
            ls -t docker-compose_* 2>/dev/null | tail -n +6 | xargs rm -f
            cd ..
            echo "✅ Cleanup completed"
        fi
        ;;
        
    *)
        echo "🔧 DNS Updater Configuration Manager"
        echo "===================================="
        echo ""
        echo "Usage: $0 {backup|restore|list|clean}"
        echo ""
        echo "Commands:"
        echo "  backup   - Create a backup of current configuration"
        echo "  restore  - Show available backups for restoration"
        echo "  list     - List all available backups"
        echo "  clean    - Remove old backups (keep last 5)"
        echo ""
        exit 1
        ;;
esac
