FROM ubuntu:latest

RUN apt-get update \
&& apt-get install -y python3 python3-pip default-jdk wget valgrind graphviz \
&& pip3 install "dask[complete]" pyspark numpy rasterio fiona Shapely bokeh opencv-python pytest pytest-datafiles pyprof2calltree graphviz cachey \
&& apt-get clean

WORKDIR /root/Distributed-Systems/
VOLUME /root/Distributed-Systems
