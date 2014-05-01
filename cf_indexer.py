#!/usr/bin/env python
import pyrax
import pyrax.exceptions

import time


pyrax.set_setting("identity_type", "rackspace")
pyrax.set_setting("region", "IAD")
pyrax.set_credential_file("rack_auth")
cf = pyrax.cloudfiles

FILTER_CONTAINERS = ['NeedTranscode', 'RawArchive', 'test']


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
                        self.videos[name][n].append(r)
                    else:
                        self.videos[name][n] = [r]

    def get_file(self, cont, name, size):
        if cont in self.videos:
            if name in self.videos[cont]:
                if size in self.videos[cont][name]:
                    o = cf.get_object(cont, name + '/' + size + '.mp4')
                    print o
                    g = o.get()
                    print (len(g) / 1024)



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
