#!/bin/bash
set -e

echo "🏗️  Compilando blog con Hugo..."
docker run --rm -v $(pwd):/app klakegg/hugo:latest hugo --minify

echo "📦 Construyendo imagen Docker..."
docker build -t jimenezgomez-blog:latest .

echo "✅ Build completado!"
echo ""
echo "Para ejecutar localmente:"
echo "  docker run -p 80:80 jimenezgomez-blog:latest"
echo ""
echo "O con docker-compose:"
echo "  docker-compose up -d"
