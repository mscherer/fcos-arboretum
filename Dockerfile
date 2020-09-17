FROM fedora:32
USER webserver
RUN adduser webserver
EXPOSE 8080
COPY main.py .
MAINTAINER Michael Scherer <misc@redhat.com>
CMD ["./main.py"]
