#!/bin/bash
# ============================================================================
# Kucibok Prospector — PostgreSQL Restore Script
# ============================================================================
# Usage: ./scripts/restore.sh <backup_file>
# Restores the PostgreSQL database from a backup file

set -e

if [ -z "$1" ]; then
    echo "❌ Usage: ./scripts/restore.sh <backup_file>"
    echo "   Example: ./scripts/restore.sh backups/kucibok_backup_20240101_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Source environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

DB_USER="${DB_USER:-kucibok}"
DB_PASSWORD="${DB_PASSWORD:-changeme}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-kucibok_prospector}"

echo "⚠️  WARNING: This will restore the database from $BACKUP_FILE"
echo "   Host: $DB_HOST:$DB_PORT"
echo "   Database: $DB_NAME"
echo ""
read -p "Are you sure? (type 'yes' to continue): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Restore cancelled."
    exit 1
fi

echo "🔄 Restoring database from backup..."

# Decompress if needed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "   Decompressing $BACKUP_FILE..."
    TEMP_FILE="${BACKUP_FILE%.gz}"
    gunzip -k -f "$BACKUP_FILE"
    BACKUP_FILE="$TEMP_FILE"
fi

# Restore backup
PGPASSWORD="$DB_PASSWORD" psql \
    -U "$DB_USER" \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -d "$DB_NAME" \
    < "$BACKUP_FILE"

echo "✅ Restore completed successfully!"
echo "   Database: $DB_NAME"
