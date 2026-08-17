#!/bin/bash
# ============================================================================
# Kucibok Prospector — PostgreSQL Backup Script
# ============================================================================
# Usage: ./scripts/backup.sh
# Backs up the PostgreSQL database to backups/ directory

set -e

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/kucibok_backup_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Source environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

DB_USER="${DB_USER:-kucibok}"
DB_PASSWORD="${DB_PASSWORD:-changeme}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-kucibok_prospector}"

echo "🔄 Backing up PostgreSQL database..."
echo "   Host: $DB_HOST:$DB_PORT"
echo "   Database: $DB_NAME"
echo "   Output: $BACKUP_FILE"

# Perform backup
PGPASSWORD="$DB_PASSWORD" pg_dump \
    -U "$DB_USER" \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -d "$DB_NAME" \
    > "$BACKUP_FILE"

# Compress the backup
gzip "$BACKUP_FILE"
BACKUP_FILE="${BACKUP_FILE}.gz"

echo "✅ Backup completed: $BACKUP_FILE"
echo "   Size: $(du -h $BACKUP_FILE | cut -f1)"

# Clean up old backups (keep only last 30 days by default)
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
echo "🧹 Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "kucibok_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup and cleanup complete!"
