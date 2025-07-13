#!/bin/bash

if [ -z "$1" ]; then
  echo "❌ 사용법: $0 <migration_message>"
  exit 1
fi

MESSAGE=$1
REV_ID=$(date +%Y%m%d%H%M%S)

echo "🔧 마이그레이션 생성 중: $MESSAGE ($REV_ID)"
alembic revision --autogenerate --rev-id "$REV_ID" -m "$MESSAGE"

# ✅ 마이그레이션은 항상 반영
echo "📈 데이터베이스 스키마 반영 중..."
alembic upgrade head

# ✅ init 관련 메시지일 경우에만 seed 실행
if [[ "$MESSAGE" == "init"* || "$MESSAGE" == "initial"* ]]; then
  echo "🌱 초기 마이그레이션이므로 seed 데이터를 삽입합니다..."
  python scripts/seed.py
else
  echo "🚫 seed 데이터는 이번 마이그레이션에서 건너뜁니다."
fi

echo "✅ 완료되었습니다."
