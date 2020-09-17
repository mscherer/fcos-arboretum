FROM fedora:32
COPY main.py .
MAINTAINER Michael Scherer <misc@redhat.com>
CMD ["./main.py"]
