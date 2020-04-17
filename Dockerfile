FROM ubuntu:latest

RUN apt-get update \
&& apt-get install -y python3 python3-pip default-jdk \
&& python3 -m pip install "dask[complete]" \
&& pip3 install rasterio \
&& pip3 install Shapely \
&& pip3 install opencv-python

WORKDIR /root/Distributed-Systems/
VOLUME /root/Distributed-Systems
