FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -o Acquire::Max-FutureTime=86400 update && apt-get install -y \
                git \
                cmake \
                software-properties-common \
                python3.8 \
                python3-pip \
                libpq-dev \
                libspatialindex-dev

RUN python3 -m pip install pandas \
                        Rtree \
                        psycopg2 \
                        numpy \
                        sqlalchemy \
                        datetime \
                        geopandas \
                        folium \
                        shapely \
                        branca \
                        descartes

RUN mkdir -p /local/lib/python3.8/dist-packages/

ENV PYTHONPATH=/local/lib/python3.8/dist-packages/

WORKDIR /opt/visual/