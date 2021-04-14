# -*- coding: utf-8 -*-
import logging
import requests
from urllib.parse import urljoin
from tor_spider.settings import s_host,s_port

LOGGER = logging.getLogger("python-weed")


class WeedFiler(object):
    """ weed filer service.
    """

    def __init__(self, host=s_host, port=s_port, protocol='http'):
        """ construct WeedFiler

        Arguments:
        - `host`: defaults to '127.0.0.1'
        - `port`: defaults to 27100
        """
        self.host = host
        self.port = port
        self.protocol = protocol
        self.uri = '%s:%d' % (host, port)
        self.url = '%s://' % self.protocol + self.uri


    def get(self, remote_path):
        """ put a file @fp to @remote_path on weedfs

        returns @remote_path if succeeds else None
        Arguments:
        - `self`:
        - `remote_path`:
        - `echo`: if True, print response
        """
        url = urljoin(self.url, remote_path)
        result = None
        try:
            rsp = requests.get(url)
            if rsp.ok:
                result = rsp.text
            else:
                LOGGER.error('GET status code: %s' % rsp.status_code, extra=dict(url=url))
        except Exception as e:
            LOGGER.error('Error GET %s' % e, extra=dict(url=url))

        return result


    def put(self, fp, remote_path):
        """ put a file @fp to @remote_path on weedfs

        returns @remote_path if succeeds else None
        Arguments:
        - `self`:
        - `remote_path`:
        - `echo`: if True, print response
        """
        url = urljoin(self.url, remote_path)
        _fp = open(fp, 'rb') if isinstance(fp, str) else fp
        try:
            rsp = requests.post(url, files={'file': _fp})
            if rsp.ok:
                return rsp.text
            else:
                LOGGER.error('POST status code: %s' % rsp.status_code, extra=dict(url=url))
        except Exception as e:
            LOGGER.error('Error POST %s' % e, extra=dict(url=url))

        # close fp if parameter fp is a str
        if isinstance(fp, str):
            try:
                _fp.close()
            except Exception as e:
                LOGGER.warning('Could not close fp: %s. e: %s' % (_fp, e))

        return None


    def delete(self, remote_path):
        ''' remove a @remote_path by http DELETE '''
        url = urljoin(self.url, remote_path)
        try:
            rsp = requests.delete(url)
            if not rsp.ok:
                LOGGER.error('Error delete file code: %s' % rsp.status_code, extra=dict(remote_path=remote_path))
            return rsp.ok
        except Exception as e:
            LOGGER.error('Error delete file %s' % e, extra=dict(remote_path=remote_path))
            return False


    def list(self, dir, pretty=False):
        ''' list sub folders and files of @dir. show a better look if you turn on @pretty

        returns a dict of "sub-folders and files'
        '''
        d = dir if dir.endswith('/') else (dir + '/')
        url = urljoin(self.url, d)
        headers = {'Accept': 'application/json'}
        try:
            rsp = requests.get(url, headers=headers)
            if not rsp.ok:
                LOGGER.error('Error listing code: %s' % rsp.status_code, extra=dict(url=url))
            return rsp.json()
        except Exception as e:
            LOGGER.error('Error listing %s' % e, extra=dict(url=url))
        return None
