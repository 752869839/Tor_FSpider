# -*- coding: utf-8 -*-
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
from scrapy.core.downloader.handlers.http11 import (
    HTTP11DownloadHandler,
    ScrapyAgent)
from scrapy.core.downloader.webclient import _parse
from twisted.internet import interfaces
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols import tls
from twisted.web.client import Agent, SchemeNotSupported
from twisted.web.iweb import IAgentEndpointFactory, IAgent, IPolicyForHTTPS
from txtorcon.endpoints import TorClientEndpoint
from zope.interface import implementer

_Agent = Agent


@implementer(interfaces.IStreamClientEndpoint)
class TLSWrapClientEndpoint(object):
    """An endpoint which automatically starts TLS.
    :param contextFactory: A `ContextFactory`__ instance.
    :param wrappedEndpoint: The endpoint to wrap.
    __ http://twistedmatrix.com/documents/current/api/twisted.internet.protocol.ClientFactory.html
    """

    _wrapper = tls.TLSMemoryBIOFactory

    def __init__(self, context_factory, wrapped_endpoint):
        self.context_factory = context_factory
        self.wrapped_endpoint = wrapped_endpoint

    def connect(self, fac):
        """Connect to the wrapped endpoint, then start TLS.
        The TLS negotiation is done by way of wrapping the provided factory
        with `TLSMemoryBIOFactory`__ during connection.
        :returns: A ``Deferred`` which fires with the same ``Protocol`` as
            ``wrappedEndpoint.connect(fac)`` fires with. If that ``Deferred``
            errbacks, so will the returned deferred.
        __ http://twistedmatrix.com/documents/current/api/twisted.protocols.tls.html
        """
        fac = self._wrapper(self.context_factory, True, fac)
        return self.wrapped_endpoint.connect(fac).addCallback(
            self._unwrap_protocol)

    @staticmethod
    def _unwrap_protocol(proto):
        return proto.wrappedProtocol


@implementer(IAgentEndpointFactory, IAgent)
class Agent(object):
    def __init__(self, reactor, contextFactory=ScrapyClientContextFactory(),
                 connectTimeout=None, bindAddress=None, pool=None):
        if not IPolicyForHTTPS.providedBy(contextFactory):
            raise NotImplementedError(
                'contextFactory must implement IPolicyForHTTPS')
        self._policyForHTTPS = contextFactory
        self._wrappedAgent = _Agent.usingEndpointFactory(
            reactor, self, pool=pool)

    def request(self, *a, **kw):
        return self._wrappedAgent.request(*a, **kw)

    def endpointForURI(self, uri):
        return self._getEndpoint(uri.scheme, uri.host, uri.port)


class SOCKSAgent(Agent):
    endpointFactory = TorClientEndpoint
    _tlsWrapper = TLSWrapClientEndpoint

    def __init__(self, *a, **kw):
        self.proxyEndpoint = kw.pop('proxyEndpoint')
        self.endpointArgs = kw.pop('endpointArgs', {})
        super(SOCKSAgent, self).__init__(*a, **kw)

    def _getEndpoint(self, scheme, host, port):
        if scheme not in (b'http', b'https'):
            raise SchemeNotSupported('unsupported scheme', scheme)
        endpoint = self.endpointFactory(
            host, port, self.proxyEndpoint, **self.endpointArgs)
        if scheme == b'https':
            tlsPolicy = self._policyForHTTPS.creatorForNetloc(host, port)
            endpoint = self._tlsWrapper(tlsPolicy, endpoint)
        return endpoint


class ScrapySocks5Agent(ScrapyAgent):

    def _get_agent(self, request, timeout):
        bindAddress = request.meta.get('bindaddress') or self._bindAddress
        proxy = request.meta.get('proxy')
        if proxy:
            _, _, proxyHost, proxyPort, proxyParams = _parse(proxy)
            _, _, host, port, proxyParams = _parse(request.url)
            proxyEndpoint = TCP4ClientEndpoint(reactor, proxyHost, proxyPort,
                                               timeout=timeout,
                                               bindAddress=bindAddress)
            agent = SOCKSAgent(reactor, proxyEndpoint=proxyEndpoint)
            return agent
        return self._Agent(reactor, contextFactory=self._contextFactory,
                           connectTimeout=timeout, bindAddress=bindAddress,
                           pool=self._pool)


class Socks5DownloadHandler(HTTP11DownloadHandler):

    def download_request(self, request, spider):
        """Return a deferred for the HTTP download"""
        agent = ScrapySocks5Agent(contextFactory=self._contextFactory,
                                  pool=self._pool)
        return agent.download_request(request)
