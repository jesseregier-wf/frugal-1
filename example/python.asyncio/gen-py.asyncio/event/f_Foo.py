#
# Autogenerated by Frugal Compiler (1.19.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



import asyncio
from datetime import timedelta
import inspect

from frugal.aio.processor import FBaseProcessor
from frugal.aio.processor import FProcessorFunction
from frugal.aio.registry import FClientRegistry
from frugal.middleware import Method
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
import base
from event.Foo import *
from event.ttypes import *


class Iface(base.f_BaseFoo.Iface):
    """
    This is a thrift service. Frugal will generate bindings that include 
    a frugal Context for each service call.
    """

    async def ping(self, ctx):
        """
        Ping the server.
        
        Args:
            ctx: FContext
        """
        pass

    async def blah(self, ctx, num, Str, event):
        """
        Blah the server.
        
        Args:
            ctx: FContext
            num: int (signed 32 bits)
            Str: string
            event: Event
        """
        pass

    async def oneWay(self, ctx, id, req):
        """
        oneway methods don't receive a response from the server.
        
        Args:
            ctx: FContext
            id: int (signed 64 bits)
            req: dict of <int (signed 32 bits), string>
        """
        pass


class Client(base.f_BaseFoo.Client, Iface):

    def __init__(self, transport, protocol_factory, middleware=None):
        """
        Create a new Client with a transport and protocol factory.

        Args:
            transport: FTransport
            protocol_factory: FProtocolFactory
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        super(Client, self).__init__(transport, protocol_factory,
                                     middleware=middleware)
        self._methods.update({
            'ping': Method(self._ping, middleware),
            'blah': Method(self._blah, middleware),
            'oneWay': Method(self._oneWay, middleware),
        })

    async def ping(self, ctx):
        """
        Ping the server.
        
        Args:
            ctx: FContext
        """
        return await self._methods['ping']([ctx])

    async def _ping(self, ctx):
        timeout = ctx.get_timeout() / 1000.0
        future = asyncio.Future()
        timed_future = asyncio.wait_for(future, timeout)
        await self._transport.register(ctx, self._recv_ping(ctx, future))
        try:
            await self._send_ping(ctx)
            result = await timed_future
        finally:
            await self._transport.unregister(ctx)
        return result

    async def _send_ping(self, ctx):
        oprot = self._oprot
        async with self._write_lock:
            oprot.write_request_headers(ctx)
            oprot.writeMessageBegin('ping', TMessageType.CALL, 0)
            args = ping_args()
            args.write(oprot)
            oprot.writeMessageEnd()
            await oprot.get_transport().flush()

    def _recv_ping(self, ctx, future):
        def ping_callback(transport):
            iprot = self._protocol_factory.get_protocol(transport)
            iprot.read_response_headers(ctx)
            _, mtype, _ = iprot.readMessageBegin()
            if mtype == TMessageType.EXCEPTION:
                x = TApplicationException()
                x.read(iprot)
                iprot.readMessageEnd()
                future.set_exception(x)
                raise x
            result = ping_result()
            result.read(iprot)
            iprot.readMessageEnd()
            future.set_result(None)
        return ping_callback

    async def blah(self, ctx, num, Str, event):
        """
        Blah the server.
        
        Args:
            ctx: FContext
            num: int (signed 32 bits)
            Str: string
            event: Event
        """
        return await self._methods['blah']([ctx, num, Str, event])

    async def _blah(self, ctx, num, Str, event):
        timeout = ctx.get_timeout() / 1000.0
        future = asyncio.Future()
        timed_future = asyncio.wait_for(future, timeout)
        await self._transport.register(ctx, self._recv_blah(ctx, future))
        try:
            await self._send_blah(ctx, num, Str, event)
            result = await timed_future
        finally:
            await self._transport.unregister(ctx)
        return result

    async def _send_blah(self, ctx, num, Str, event):
        oprot = self._oprot
        async with self._write_lock:
            oprot.write_request_headers(ctx)
            oprot.writeMessageBegin('blah', TMessageType.CALL, 0)
            args = blah_args()
            args.num = num
            args.Str = Str
            args.event = event
            args.write(oprot)
            oprot.writeMessageEnd()
            await oprot.get_transport().flush()

    def _recv_blah(self, ctx, future):
        def blah_callback(transport):
            iprot = self._protocol_factory.get_protocol(transport)
            iprot.read_response_headers(ctx)
            _, mtype, _ = iprot.readMessageBegin()
            if mtype == TMessageType.EXCEPTION:
                x = TApplicationException()
                x.read(iprot)
                iprot.readMessageEnd()
                future.set_exception(x)
                raise x
            result = blah_result()
            result.read(iprot)
            iprot.readMessageEnd()
            if result.awe is not None:
                future.set_exception(result.awe)
                return
            if result.api is not None:
                future.set_exception(result.api)
                return
            if result.success is not None:
                future.set_result(result.success)
                return
            x = TApplicationException(TApplicationException.MISSING_RESULT, "blah failed: unknown result")
            future.set_exception(x)
            raise x
        return blah_callback

    async def oneWay(self, ctx, id, req):
        """
        oneway methods don't receive a response from the server.
        
        Args:
            ctx: FContext
            id: int (signed 64 bits)
            req: dict of <int (signed 32 bits), string>
        """
        return await self._methods['oneWay']([ctx, id, req])

    async def _oneWay(self, ctx, id, req):
        await self._send_oneWay(ctx, id, req)

    async def _send_oneWay(self, ctx, id, req):
        oprot = self._oprot
        async with self._write_lock:
            oprot.write_request_headers(ctx)
            oprot.writeMessageBegin('oneWay', TMessageType.CALL, 0)
            args = oneWay_args()
            args.id = id
            args.req = req
            args.write(oprot)
            oprot.writeMessageEnd()
            await oprot.get_transport().flush()


class Processor(base.f_BaseFoo.Processor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__(handler, middleware=middleware)
        self.add_to_processor_map('ping', _ping(Method(handler.ping, middleware), self.get_write_lock()))
        self.add_to_processor_map('blah', _blah(Method(handler.blah, middleware), self.get_write_lock()))
        self.add_to_processor_map('oneWay', _oneWay(Method(handler.oneWay, middleware), self.get_write_lock()))


class _ping(FProcessorFunction):

    def __init__(self, handler, lock):
        self._handler = handler
        self._write_lock = lock

    async def process(self, ctx, iprot, oprot):
        args = ping_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = ping_result()
        ret = self._handler([ctx])
        if inspect.iscoroutine(ret):
            ret = await ret
        async with self._write_lock:
            oprot.write_response_headers(ctx)
            oprot.writeMessageBegin('ping', TMessageType.REPLY, 0)
            result.write(oprot)
            oprot.writeMessageEnd()
            oprot.get_transport().flush()


class _blah(FProcessorFunction):

    def __init__(self, handler, lock):
        self._handler = handler
        self._write_lock = lock

    async def process(self, ctx, iprot, oprot):
        args = blah_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = blah_result()
        try:
            ret = self._handler([ctx, args.num, args.Str, args.event])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except AwesomeException as awe:
            result.awe = awe
        except base.ttypes.api_exception as api:
            result.api = api
        async with self._write_lock:
            oprot.write_response_headers(ctx)
            oprot.writeMessageBegin('blah', TMessageType.REPLY, 0)
            result.write(oprot)
            oprot.writeMessageEnd()
            oprot.get_transport().flush()


class _oneWay(FProcessorFunction):

    def __init__(self, handler, lock):
        self._handler = handler
        self._write_lock = lock

    async def process(self, ctx, iprot, oprot):
        args = oneWay_args()
        args.read(iprot)
        iprot.readMessageEnd()
        ret = self._handler([ctx, args.id, args.req])
        if inspect.iscoroutine(ret):
            ret = await ret


