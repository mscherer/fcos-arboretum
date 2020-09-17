FROM fedora:32
MAINTAINER Michael Scherer <misc@redhat.com>
COPY main.py .
RUN dnf install python3-requests && dnf clean all
EXPOSE 8080
USER nobody
CMD ["python3", "./main.py"]
