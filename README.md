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
docker run -it --rm -v $PWD:/root/Distributed-Systems distributed-systems-ubuntu bash
```
# Install
-----
```
pip3 install .
#or pip3 install -e .
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
