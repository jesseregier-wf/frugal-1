#
# Autogenerated by Frugal Compiler (2.0.2)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



from datetime import timedelta
from threading import Lock

from frugal.exceptions import TApplicationExceptionType
from frugal.exceptions import TTransportExceptionType
from frugal.middleware import Method
from frugal.tornado.processor import FBaseProcessor
from frugal.tornado.processor import FProcessorFunction
from frugal.transport import TMemoryOutputBuffer
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from tornado import gen
from tornado.concurrent import Future

from .ttypes import *


class Iface(object):

    def basePing(self, ctx):
        """
        Args:
            ctx: FContext
        """
        pass


class Client(Iface):

    def __init__(self, provider, middleware=None):
        """
        Create a new Client with an FServiceProvider containing a transport
        and protocol factory.

        Args:
            provider: FServiceProvider
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        middleware = middleware or []
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        self._transport = provider.get_transport()
        self._protocol_factory = provider.get_protocol_factory()
        self._oprot = self._protocol_factory.get_protocol(self._transport)
        self._write_lock = Lock()
        middleware += provider.get_middleware()
        self._methods = {
            'basePing': Method(self._basePing, middleware),
        }

    def basePing(self, ctx):
        """
        Args:
            ctx: FContext
        """
        return self._methods['basePing']([ctx])

    @gen.coroutine
    def _basePing(self, ctx):
        buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('basePing', TMessageType.CALL, 0)
        args = basePing_args()
        args.write(oprot)
        oprot.writeMessageEnd()
        response_transport = yield self._transport.request(ctx, buffer.getvalue())

        iprot = self._protocol_factory.get_protocol(response_transport)
        iprot.read_response_headers(ctx)
        _, mtype, _ = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.REQUEST_TOO_LARGE, message=x.message)
            raise x
        result = basePing_result()
        result.read(iprot)
        iprot.readMessageEnd()

class Processor(FBaseProcessor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__()
        self.add_to_processor_map('basePing', _basePing(Method(handler.basePing, middleware), self.get_write_lock()))


class _basePing(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_basePing, self).__init__(handler, lock)

    @gen.coroutine
    def process(self, ctx, iprot, oprot):
        args = basePing_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = basePing_result()
        try:
            yield gen.maybe_future(self._handler([ctx]))
        except TApplicationException as ex:
            with (yield self._lock.acquire()):
                _write_application_exception(ctx, oprot, "basePing", exception=ex)
                return
        except Exception as e:
            with (yield self._lock.acquire()):
                e = _write_application_exception(ctx, oprot, "basePing", ex_code=TApplicationExceptionType.UNKNOWN, message=e.message)
            raise e
        with (yield self._lock.acquire()):
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('basePing', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                if e.type == TTransportExceptionType.RESPONSE_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "basePing", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.message)
                else:
                    raise e


def _write_application_exception(ctx, oprot, method, ex_code=None, message=None, exception=None):
    if exception is not None:
        x = exception
    else:
        x = TApplicationException(type=ex_code, message=message)
    oprot.write_response_headers(ctx)
    oprot.writeMessageBegin(method, TMessageType.EXCEPTION, 0)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.get_transport().flush()
    return x

class basePing_args(object):
    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('basePing_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class basePing_result(object):
    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('basePing_result')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

