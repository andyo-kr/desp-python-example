docker run -v $(pwd)/secrets:/app/secrets \
           -v $(pwd)/test-data:/app/test-data \
           -v $(pwd):/app \
  docker-prod.registry.kroger.com/shockwave/py-desp:0.3 $@