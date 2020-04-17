# Distributed-Systems

-----
```
git clone https://github.com/SylvainDeker/Distributed-Systems
cd Distributed-Systems
chmod u+x setup.sh
./setup.sh
```

# Build docker:
-----
```
docker build -t distributed-systems-ubuntu .
```

# Run docker
-----
```
docker run -t -d -v `pwd`:/root/Distributed-Systems distributed-systems-ubuntu
```
# Open Bash shell
-----
```
docker exec -ti <ID> bash
```
#Then try them:
-----
```
./run_dask.sh
#or
./run_spark
```
Those last 2 commands produce file .tiff here 
