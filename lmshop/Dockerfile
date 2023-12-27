FROM archlinux:latest
LABEL maintainer="dmitry.starushko@gmail.com"
RUN pacman -Sy --noconfirm ttf-bitstream-vera ttf-croscore ttf-dejavu ttf-droid ttf-liberation wt boost openssl zlib crypto++
ENV PORT 7777
ENV WKD /usr/bin/lmshop
RUN mkdir -p $WKD
WORKDIR $WKD
COPY . .
EXPOSE $PORT
ENTRYPOINT $WKD/lmshop --docroot $WKD --http-address 0.0.0.0 --http-port $PORT -c $WKD/wt_config.xml
