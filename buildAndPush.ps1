# dclare the image name

$IMG = "viliusvv/private:lemongym-scrape-latest"

docker build -t $IMG .
docker push $IMG