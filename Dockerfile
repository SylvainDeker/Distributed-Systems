FROM debian:9

RUN apt-get update \
&& apt-get install -y python3 python3-pip git default-jdk \
&& python3 -m pip install "dask[complete]" \
&& pip3 install rasterio \
&& pip3 install Shapely \
&& pip3 install opencv-python

ADD . /root/distributed-Systems/
WORKDIR /root/distributed-Systems/
