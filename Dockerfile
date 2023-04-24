# base ubuntu 18.04 image
FROM ubuntu:bionic

## system-wide dependencies
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
build-essential git ffmpeg bc \
python3 python3-dev python3-pip python3-setuptools python3-wheel

# install video-server app
WORKDIR /opt/video-server-app
COPY ./ /opt/video-server-app
RUN pip3 install honcho==1.0.1
RUN pip3 install gunicorn==19.7.1
RUN pip3 install -e video-server/[dev]

# run
ENTRYPOINT ["honcho"]
CMD ["start"]