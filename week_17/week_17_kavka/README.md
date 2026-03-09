# week_17_kavka

docker compose logs --tail=200 producer
docker compose logs --tail=200 consumer
docker compose logs --tail=200 analytics-api




docker compose down -v
docker compose build --no-cache
docker compose up -d
docker compose ps