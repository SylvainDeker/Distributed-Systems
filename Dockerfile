FROM ubuntu:19.10

RUN apt-get update \
&& apt-get install -y python3 python3-pip openjdk-11-jdk wget valgrind graphviz git \
&& pip3 install "dask[complete]" dask-kubernetes --upgrade numpy rasterio fiona Shapely bokeh opencv-python pytest pytest-datafiles pyprof2calltree graphviz cachey cffi pyyaml git+git://github.com/jcrist/pycallgrind \
&& apt-get clean
WORKDIR /root/
RUN wget https://downloads.apache.org/spark/spark-3.0.0-preview2/spark-3.0.0-preview2-bin-hadoop2.7.tgz \
&& mkdir /opt/spark \
&& tar xzf spark-3.0.0-preview2-bin-hadoop2.7.tgz -C /opt/spark/
WORKDIR /opt/spark/spark-3.0.0-preview2-bin-hadoop2.7/python/
RUN python3 setup.py sdist \
&& pip3 install dist/*.tar.gz

ENV PATH $PATH:/opt/spark/spark-2.4.5-bin-hadoop2.7/sbin
WORKDIR /root/Distributed-Systems/
VOLUME /root/Distributed-Systems
CMD pip3 install -e . && export PYSPARK_PYTHON=python3 && bash
