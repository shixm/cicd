From registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow

MAINTAINER LiuChuang  chuangliu18@creditease.cn

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y libgtk2.0-dev libsm6 libxext6 git
RUN apt-get install -y libevent-dev

RUN easy_install pip
RUN pip install gevent
RUN pip install gunicorn
RUN pip install opencv-contrib-python
RUN pip install keras flask h5py jsonify
RUN pip install -U scikit-image
 
WORKDIR /home
ADD .netrc /root
RUN git clone https://gitee.com/piginzoo/captcha.git

EXPOSE 8080

WORKDIR /home/captcha/web
CMD gunicorn -w 4 -k gevent api_server:app -b 0.0.0.0:8080

