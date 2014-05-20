#!/usr/bin/env python
import pyrax
import pyrax.exceptions

import time

logfile = "cloudfiles.log"

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_setting("region", "IAD")
pyrax.set_credential_file("rack_auth")
cf = pyrax.cloudfiles

FILTER_CONTAINERS = ['NeedTranscode', 'RawArchive', 'test']


def log(msg):
    with open(logfile, "a") as of:
        of.write(msg + '\n')


class cf_indexer(object):
    def __init__(self):
        self.videos = {}

    def populate_videos(self):
        for name in cf.list_containers():
            if name not in FILTER_CONTAINERS:
                cont = cf.get_container(name)
                self.videos[name] = {}
                for f in cont.get_object_names():
                    n, r = f.split('/', 1)
                    r = r.split('.')[0]
                    if n in self.videos[name]:
                        self.videos[name][n]['sizes'].append(r)
                    else:
                        self.videos[name][n] = {'sizes': [r]}

    def get_url(self, cont, name, size):
        if cont in self.videos:
            if name in self.videos[cont]:
                if size in self.videos[cont][name]['sizes']:
                    o = cf.get_object(cont, name + '/' + size + '.MP4')
                    u = o.get_temp_url(30)
                    return u

    def get_file(self, cont, name, size):
        if cont in self.videos:
            if name in self.videos[cont]:
                if size in self.videos[cont][name]['sizes']:
                    o = cf.get_object(cont, name + '/' + size + '.MP4')
                    g = o.get()
                    return g


if __name__ == '__main__':

    idxr = cf_indexer()
    s = - time.time()
    idxr.populate_videos()
    s += time.time()
    print "Populate to %fs" % s

    print idxr.videos
    s = - time.time()
    idxr.get_file('moretests', 'Jam1', 'mobile')
    s += time.time()
    print "Mobile to %fs" % s
    s = - time.time()
    idxr.get_file('moretests', 'Jam1', '720p')
    s += time.time()
    print "720p to %fs" % s
    s = - time.time()
    idxr.get_file('moretests', 'Jam1', '1080p')
    s += time.time()
    print "1080p to %fs" % s
