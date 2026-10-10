#!/bin/sh
# Notify IndexNow search engines (Bing, Yandex, Seznam, Naver…) about every URL in the live sitemap.
#   sh scripts/indexnow.sh
set -e
HOST=pdfshrink.gumber.ai
KEYFILE=$(ls "$(dirname "$0")/../static/root/" | grep -E '^[0-9a-f]{32}\.txt$' | head -1)
KEY=${KEYFILE%.txt}
URLS=$(curl -s "https://$HOST/sitemap.xml" | grep -o '<loc>[^<]*' | sed 's/<loc>//' | sed 's/.*/"&"/' | paste -sd, -)
BODY="{\"host\":\"$HOST\",\"key\":\"$KEY\",\"keyLocation\":\"https://$HOST/$KEY.txt\",\"urlList\":[$URLS]}"
echo "Submitting $(echo "$URLS" | tr ',' '\n' | wc -l | tr -d ' ') URLs…"
curl -s -o /dev/null -w "IndexNow response: HTTP %{http_code}\n" -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" --data "$BODY"
