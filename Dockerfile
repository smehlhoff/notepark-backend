FROM lambci/lambda:build-python3.6

WORKDIR /var/task

COPY . /var/task

RUN echo 'export PS1="\[\e[36m\]notepark-backend>\[\e[m\] "' >> /root/.bashrc

RUN yum clean all && yum -y install nano

CMD ["bash"]
