FROM verdel/centos-base:latest
LABEL maintainer="Vadim Aleksandrov <valeksandrov@me.com>"

# Install zabbix
RUN yum install -y http://repo.yandex.ru/yandex-disk/yandex-disk-latest.x86_64.rpm && \
    pip install requests && \
    # Clean up
    yum clean all && \
    rm -rf \
    /usr/share/man \
    /tmp/* \
    /var/cache/yum

# Copy init scripts
COPY rootfs /

RUN chmod +x /usr/sbin/sync.sh
