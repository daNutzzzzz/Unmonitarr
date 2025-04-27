# Unmonitarr

docker build -t unmonitarr .
docker run -d -p 5000:5000 -v ./data:/app/data --name unmonitarr unmonitarr


mkdir -p data
docker-compose up -d --build


