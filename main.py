import requests

from http.server import BaseHTTPRequestHandler, HTTPServer

streams = ['stable', 'next', 'testing']

artefacts = ['kernel', 'initramfs', 'rootfs']

# TODO make it dynamic
supported_arch = ['x86_64']

hostName = "localhost"
serverPort = 8080

# url 
#  /stable/
#    arch/
#     .treeinfo => quasi stable
#     kernel
#     initrd => https://builds.coreos.fedoraproject.org/prod/streams/stable/builds/32.20200824.3.0/x86_64/fedora-coreos-32.20200824.3.0-live-initramfs.x86_64.img
#     rootfs


def get_artefacts(stream):
    url = "https://builds.coreos.fedoraproject.org/streams/%s.json" % stream
    r = requests.get(url).json()
    data = {}
    for a in r['architectures']:
        data[a] = {}
        for b in artefacts:
            data[a][b] = r['architectures'][a]['artifacts']['metal']['formats']['pxe'][b]['location']
    return data


def generate_treeinfo(arch, version):
    return """
[general]
arch = {arch}
family = Red Hat CoreOS
platforms = {arch}
version = {version}
[images-{arch}]
initrd = initramfs
kernel = kernel
rootfs = rootfs
""".format(arch=arch, version=version)


class MyServer(BaseHTTPRequestHandler):

    def return_404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found\n", "utf-8"))

    def return_302(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()
       

    def return_200(self, response):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))
         

    def check_path(self):
        # 1st item is empty, since the url start by /
        p = self.path.split('/')[1:]
        if len(p) != 3:
            return False
        if p[0] not in streams:
            return False
        if p[1] not in supported_arch:
            return False
        if p[2] not in artefacts and p[2] != '.treeinfo':
            return False
        return True

    def return_index(self):
        self.return_200("Redirect server for virt-install and FCOS\n")

    def do_GET(self):
        if self.path == '/':
            self.return_index()
        elif not self.check_path():
            self.return_404()
        else:
            s, a, i = self.path.split('/')[1:]
            if i == '.treeinfo':
                self.do_treeinfo(s, a)
            else:
                self.redirect_artefact(s, a, i)

    def do_treeinfo(self, stream, arch):
        self.return_200(generate_treeinfo(stream, arch))

    def redirect_artefact(self, stream, arch, artifact):
        data = get_artefacts(stream)
        self.return_302(data[arch][artifact]) 
        

if __name__ == "__main__":

    # TODO fix that        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
