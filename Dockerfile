FROM ubuntu:latest

RUN apt-get update \
&& apt-get install -y python3 python3-pip default-jdk wget \
&& pip3 install "dask[complete]" pyspark numpy rasterio fiona Shapely bokeh opencv-python pytest pytest-datafiles\
&& apt-get clean

WORKDIR /root/Distributed-Systems/
VOLUME /root/Distributed-Systems
