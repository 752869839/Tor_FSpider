# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from twisted.internet import threads
from tor_spider.settings import s_host,s_port

class WeedFilesStore(object):
    """
    实现weedfs上传图片
    """
    FILER_IP = s_host
    FILER_PORT = s_port

    def __init__(self, uri):
        from Seaweedfs.filer import WeedFiler
        assert uri.startswith('weed://')
        p = urlparse(uri)
        self.wf = WeedFiler(host=p.hostname, port=p.port)
        self.prefix = p.path

    def stat_file(self, path, info):
        return {}

    def persist_file(self, path, buf, info, meta=None, headers=None):
        path = self.prefix + '/' + path
        return threads.deferToThread(
            self.wf.put,
            buf.getvalue(),
            path,
        )
