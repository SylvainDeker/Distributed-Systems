#!/usr/bin/env bash

echo "Download Spark"

wget https://www.apache.org/dyn/closer.lua/spark/spark-3.0.0-preview2/spark-3.0.0-preview2-bin-hadoop2.7.tgz
tar xzf spark-3.0.0-preview2-bin-hadoop2.7.tgz
rm -f spark-3.0.0-preview2-bin-hadoop2.7.tgz


echo "Download a GeoTiff image"
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/raster/NE1_50M_SR_W.zip
unzip NE1_50M_SR_W.zip -d data/
rm -f NE1_50M_SR_W.zip


echo "Download a Shapefile .shp"
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_urban_areas.zip
unzip ne_10m_urban_areas.zip -d data/ne_10m_urban_areas/
rm -f ne_10m_urban_areas.zip
