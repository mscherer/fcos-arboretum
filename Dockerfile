FROM fedora:32
MAINTAINER Michael Scherer <misc@redhat.com>
COPY main.py .
USER nobody
EXPOSE 8080
CMD ["python3", "./main.py"]
