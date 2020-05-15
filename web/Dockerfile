FROM python:3
RUN apt update && \
    apt install nano
	
#JUMANのインストール 
RUN apt install gcc && \
    wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2 && \
    tar jxvf juman-7.01.tar.bz2 && \
    cd juman-7.01 && \ 
    ./configure && \
    make && \ 
    make install && \ 
    echo include /usr/local/lib >> /etc/ld.so.conf
RUN ldconfig
	
#KNPのインストール 
RUN wget -O knp-4.20.tar.bz2 http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.20.tar.bz2 
RUN tar jxvf knp-4.20.tar.bz2
WORKDIR knp-4.20 
RUN	./configure
RUN	make 
RUN	make install
	
COPY . /app
WORKDIR /app
RUN pip install -U pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
