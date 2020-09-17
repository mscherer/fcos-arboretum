FROM fedora:32
MAINTAINER Michael Scherer <misc@redhat.com>
COPY main.py .
USER nobody
EXPOSE 8080
RUN dnf install python3-requests && dnf clean all
CMD ["python3", "./main.py"]
