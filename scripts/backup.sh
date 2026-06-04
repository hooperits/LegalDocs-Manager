#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e
set -o pipefail

# Install AWS CLI on startup (only if not already installed)
if ! command -v aws >/dev/null 2>&1; then
    echo "Installing AWS CLI..."
    apk add --no-cache aws-cli
fi

# Configure AWS CLI endpoint if custom URL is set
AWS_ARGS=""
if [ -n "$AWS_S3_ENDPOINT_URL" ]; then
    AWS_ARGS="--endpoint-url $AWS_S3_ENDPOINT_URL"
fi

# Export AWS credentials for AWS CLI
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=${AWS_S3_REGION_NAME:-us-east-1}

BACKUP_DIR="/tmp/backups"
mkdir -p "$BACKUP_DIR"

run_backup() {
    echo "Starting database backup at $(date)..."
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"

    # Disable exit-on-error temporarily to handle cleanup and reporting manually
    set +e

    # Run pg_dump
    PGPASSWORD="$DB_PASSWORD" pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_FILE"
    PG_STATUS=$?

    if [ $PG_STATUS -ne 0 ]; then
        echo "ERROR: Database dump failed with exit code $PG_STATUS" >&2
        rm -f "$BACKUP_FILE"
        set -e
        return 1
    fi
    echo "Backup file created locally: $BACKUP_FILE ($(du -sh $BACKUP_FILE | cut -f1))"

    echo "Uploading backup to S3 bucket $AWS_STORAGE_BUCKET_NAME..."
    aws s3 cp "$BACKUP_FILE" "s3://$AWS_STORAGE_BUCKET_NAME/backups/db_backup_$TIMESTAMP.sql.gz" $AWS_ARGS
    S3_STATUS=$?

    # Always clean up local backup file
    echo "Cleaning up local backup file..."
    rm -f "$BACKUP_FILE"

    if [ $S3_STATUS -ne 0 ]; then
        echo "ERROR: S3 upload failed with exit code $S3_STATUS" >&2
        set -e
        return 1
    fi

    # Enforce retention policy on S3
    if [ -n "$BACKUP_RETENTION_DAYS" ]; then
        echo "Enforcing backup retention policy (keeping last $BACKUP_RETENTION_DAYS days)..."
        # List backups in S3
        BACKUPS=$(aws s3 ls "s3://$AWS_STORAGE_BUCKET_NAME/backups/" $AWS_ARGS | awk '{print $4}')
        LS_STATUS=$?
        if [ $LS_STATUS -ne 0 ]; then
            echo "ERROR: Listing S3 backups failed with exit code $LS_STATUS" >&2
            set -e
            return 1
        fi

        # Calculate cutoff date in YYYYMMDD
        CUTOFF_TIMESTAMP=$(( $(date +%s) - BACKUP_RETENTION_DAYS*86400 ))
        # Supports busybox date
        CUTOFF_DATE=$(date -d "@$CUTOFF_TIMESTAMP" +%Y%m%d 2>/dev/null || date -u -d "@$CUTOFF_TIMESTAMP" +%Y%m%d 2>/dev/null || date -d "$BACKUP_RETENTION_DAYS days ago" +%Y%m%d)

        for b in $BACKUPS; do
            # Extract date YYYYMMDD from filename
            FILE_DATE=$(echo "$b" | grep -oE '[0-9]{8}')
            if [ -n "$FILE_DATE" ] && [ "$FILE_DATE" -lt "$CUTOFF_DATE" ]; then
                echo "Deleting expired backup: $b"
                aws s3 rm "s3://$AWS_STORAGE_BUCKET_NAME/backups/$b" $AWS_ARGS || true
            fi
        done
    fi

    # Re-enable exit-on-error
    set -e
    echo "Backup completed successfully."
    return 0
}

# Touch the file on container start to initialize health status
touch /tmp/last_backup_success

if [ "$1" = "--now" ]; then
    if run_backup; then
        exit 0
    else
        exit 1
    fi
fi

echo "Database backup service initialized in daemon mode."
while :; do
    # Calculate seconds until next 2:00 AM UTC
    TARGET_HOUR=2
    NOW=$(date +%s)
    TARGET_TODAY=$(date -d "today $TARGET_HOUR:00" +%s 2>/dev/null || date -u -d "today $TARGET_HOUR:00" +%s 2>/dev/null || date -d "$TARGET_HOUR:00" +%s)
    if [ "$NOW" -gt "$TARGET_TODAY" ]; then
        SLEEP_SECONDS=$(( TARGET_TODAY + 86400 - NOW ))
    else
        SLEEP_SECONDS=$(( TARGET_TODAY - NOW ))
    fi

    echo "Next backup scheduled in $SLEEP_SECONDS seconds (at 02:00 UTC)."
    sleep $SLEEP_SECONDS & wait $!
    
    if run_backup; then
        touch /tmp/last_backup_success
    else
        echo "ERROR: Scheduled backup failed at $(date)." >&2
    fi
done
