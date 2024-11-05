#!/bin/sh

set -e

HOST="$1"
PORT="$2"

shift 2

until nc -z "$HOST" "$PORT"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"
