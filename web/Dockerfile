FROM python:3
RUN apt update && \
    apt install nano
	
#JUMAN++のインストール 
RUN wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc2/jumanpp-2.0.0-rc2.tar.xz && \
    tar xvf jumanpp-2.0.0-rc2.tar.xz && \
    apt update -y && \ 
	apt upgrade -y && \ 
	apt install build-essential -y && \ 
    apt install cmake -y && \
    cd jumanpp-2.0.0-rc2 && \ 
	mkdir build && \ 
	cd build && \ 
	cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local && \ 
	make && \ 
    make install
	
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
