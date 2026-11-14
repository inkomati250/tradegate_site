#!/usr/bin/env bash
# Runs the Django deploy steps against the LIVE database, with exactly the settings the
# live site (systemd service "tradegate") uses. Called by .github/workflows/deploy-prod.yml
# as the deploy user.
#
# Why: before 2026-11-14 these steps ran without the service settings, fell back to
# development settings and migrated a local SQLite file, so the live PostgreSQL database
# stayed at migration 0008.
#
# Safety: the live database is backed up before any migration; if the backup fails,
# nothing is migrated.
#
# Usage: deploy_manage.sh "<env files separated by spaces>"
set -euo pipefail
APP_DIR="${APP_DIR:-/srv/tradegate/app}"
PY="${PY:-/srv/tradegate/venv/bin/python}"
BACKUP_DIR="${BACKUP_DIR:-/srv/tradegate/backups}"
ENV_FILES="${1:-/srv/tradegate/.env}"
[ -n "$ENV_FILES" ] || ENV_FILES="/srv/tradegate/.env"

for f in $ENV_FILES; do
  [ -r "$f" ] || { echo "Cannot read environment file $f"; exit 1; }
  set -a; . "$f"; set +a
done
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-tradegate.settings.prod}"

cd "$APP_DIR"
echo "Settings: $DJANGO_SETTINGS_MODULE"
VENDOR="$("$PY" manage.py shell -c "from django.db import connection as c; print(c.vendor)" | tail -1)"
echo "Database: $VENDOR"

# 1. Back up the live database before changing anything.
mkdir -p "$BACKUP_DIR"
STAMP="$(date -u +%Y%m%d-%H%M%S)"
if [ "$VENDOR" = "postgresql" ] && command -v pg_dump >/dev/null 2>&1; then
  PGPASSWORD="${DB_PASSWORD:-}" pg_dump -h "${DB_HOST:-127.0.0.1}" -p "${DB_PORT:-5432}" -U "${DB_USER:-}" \
    -Fc -f "$BACKUP_DIR/db-$STAMP.dump" "${DB_NAME}"
  echo "Backup: $BACKUP_DIR/db-$STAMP.dump"
else
  "$PY" manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission \
    -e sessions -e admin.logentry -o "$BACKUP_DIR/db-$STAMP.json"
  echo "Backup: $BACKUP_DIR/db-$STAMP.json"
fi
# keep the 20 newest backups
ls -1t "$BACKUP_DIR"/db-* 2>/dev/null | tail -n +21 | xargs -r rm -f

# 2. Checks, migrations, static files.
"$PY" manage.py makemigrations --check --dry-run
"$PY" manage.py check --deploy
"$PY" manage.py migrate --noinput
"$PY" manage.py collectstatic --noinput
"$PY" manage.py shell -c "from website.models import TradeFair as T; print('Trade fairs published:', T.objects.filter(is_published=True).count())"
