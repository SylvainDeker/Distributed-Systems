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
docker run -it --rm -p 8787:8787 -p 8081:8081 -v $PWD:/root/Distributed-Systems distributed-systems-ubuntu
docker run -it --rm --network host -v $PWD:/root/Distributed-Systems distributed-systems-ubuntu

```

#Test:
-----
```
pytest test/
```

#Then try them:
-----
```
./run_dask.sh
#or
./run_spark
```
Those last 2 commands produce file .tiff here
