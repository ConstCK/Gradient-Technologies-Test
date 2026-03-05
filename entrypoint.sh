#!/bin/sh
set -e

echo "Ожидание готовности БД..."
for i in 1 2 3 4 5 6 7 8 9 10; do
  if alembic upgrade head 2>/dev/null; then
    echo "Миграции применены."
    break
  fi
  echo "Попытка $i/10 — повтор через 2 с..."
  sleep 2
done

echo "Запуск приложения..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
