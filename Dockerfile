FROM ubuntu:latest

RUN apt-get update \
 && apt-get install -y python3 python3-pip default-jdk wget \
 && pip3 install "dask[complete]" numpy rasterio fiona Shapely bokeh opencv-python pytest \
 && apt-get clean

WORKDIR /root/Distributed-Systems/
VOLUME /root/Distributed-Systems
