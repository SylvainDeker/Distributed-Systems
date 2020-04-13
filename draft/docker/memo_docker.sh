exit 0

docker run hello-world
docker -d run hello-world

# redirect the port 8080 to the container s port 80:
docker run -d -p 8080:80 nginx
4f1214c9ac7c011a664a97d6ab0c09db6baa8299446f8924264532e7afa3b263
# Execute cmd
docker exec -ti 4f1214c9ac7c011a664a97d6ab0c09db6baa8299446f8924264532e7afa3b263 echo hello
#list imgs:
docker image ls
# running containers:
docker ps --all
# Stop a container:
docker stop 4f1214c9ac7c
#rm a container
docker rm hello-world
