part of frugal;

/// A framed implementation of TTransport. Has stream for consuming
/// entire frames. Disallows direct reads.
class _TFramedTransport extends TTransport {
  static const int headerByteCount = 4;
  final Uint8List writeHeaderBytes = new Uint8List(headerByteCount);

  final TSocket socket;
  final List<int> _writeBuffer = [];
  final List<int> _readBuffer = [];
  final List<int> _readHeaderBytes = [];
  int _frameSize;

  StreamController<Uint8List> _frameStream = new StreamController();

  bool _isOpen;

  final Uint8List headerBytes = new Uint8List(headerByteCount);

  StreamSubscription _messageSub;

  _TFramedTransport(this.socket) {
    if (socket == null) {
      throw new ArgumentError.notNull("socket");
    }
  }

  void _reset({bool isOpen: false}) {
    _isOpen = isOpen;
    _writeBuffer.clear();
    _readBuffer.clear();
  }

  /// Stream for getting frame data.
  Stream<Uint8List> get onFrame => _frameStream.stream;

  @override
  bool get isOpen => _isOpen;

  @override
  Future open() async {
    _reset(isOpen: true);
    if (socket.isClosed) {
      await socket.open();
    }
    _messageSub = socket.onMessage.listen(messageHandler);
  }

  /// Closes the transport.
  /// Will also close the underlying TSocket.
  Future close() async {
    _reset(isOpen: false);
    if (socket.isOpen) {
      await socket.close();
    }
    if (_messageSub != null) {
      _messageSub.cancel();
    }
  }

  /// Direct reading is not allowed. To consume read data listen
  /// to onFrame.
  int read(Uint8List buffer, int offset, int length) {
    throw new TTransportError(TTransportErrorType.UNKNOWN,
        "frugal: cannot read directly from _TFramedSocket.");
  }

  /// Handler for messages received on the TSocket.
  void messageHandler(Uint8List list) {
    var offset = 0;
    if (_frameSize == null) {
      // Not enough bytes to get the frame length. Add these and move on.
      if ((_readHeaderBytes.length + list.length) < headerByteCount) {
        _readHeaderBytes.addAll(list);
        return;
      }

      // Get the frame size
      var headerBytesToGet = headerByteCount - _readHeaderBytes.length;
      _readHeaderBytes.addAll(list.getRange(0, headerBytesToGet));
      var frameBuffer = new Uint8List.fromList(_readHeaderBytes).buffer;
      _frameSize = frameBuffer.asByteData().getInt32(0);
      _readHeaderBytes.clear();
      offset += headerBytesToGet;
    }

    if (_frameSize < 0) {
      // TODO: Put this error on an error stream and bubble it up.
      throw new TTransportError(TTransportErrorType.UNKNOWN,
          "Read a negative frame size: $_frameSize");
    }

    // Grab up to the frame size in bytes
    var bytesToGet = min(_frameSize - _readBuffer.length, list.length - offset);
    _readBuffer.addAll(list.getRange(offset, offset + bytesToGet));

    // Have an entire frame. Fire it off and reset.
    if (_readBuffer.length == _frameSize) {
      _frameStream.add(new Uint8List.fromList(_readBuffer));
      _readBuffer.clear();
      _frameSize = null;
    }

    // More bytes to get. Run through the handler again.
    if ((bytesToGet + offset < list.length)) {
      messageHandler(new Uint8List.fromList(list.sublist(bytesToGet + offset)));
      return;
    }
  }

  @override
  void write(Uint8List buffer, int offset, int length) {
    if (buffer == null) {
      throw new ArgumentError.notNull("buffer");
    }

    if (offset + length > buffer.length) {
      throw new ArgumentError("The range exceeds the buffer length");
    }

    _writeBuffer.addAll(buffer.sublist(offset, offset + length));
  }

  @override
  Future flush() {
    int length = _writeBuffer.length;
    headerBytes.buffer.asByteData().setUint32(0, length);
    _writeBuffer.insertAll(0, headerBytes);
    var buff = new Uint8List.fromList(_writeBuffer);
    _writeBuffer.clear();
    return new Future.value(socket.send(buff));
  }
}
