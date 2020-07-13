export IMAGE_VERSION=0.3
export DOCKER_REGISTRY=docker-prod.registry.kroger.com
export DOCKER_ARTIFACTORY_PASSWORD=${DOCKER_ARTIFACTORY_PASSWORD}
export DOCKER_IMAGE=$DOCKER_REGISTRY/shockwave/py-desp
docker build -t $DOCKER_IMAGE:$IMAGE_VERSION .
docker login $DOCKER_REGISTRY -u SVCDOCKERSHOCKWAVEP -p $DOCKER_ARTIFACTORY_PASSWORD
docker push $DOCKER_IMAGE:$IMAGE_VERSION
