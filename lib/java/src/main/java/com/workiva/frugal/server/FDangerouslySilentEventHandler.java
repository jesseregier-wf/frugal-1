package com.workiva.frugal.server;

import org.apache.thrift.TException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

/**
 * Nah.
 */
public class FDangerouslySilentEventHandler implements FServerEventHandler {
    private static final Logger LOGGER = LoggerFactory.getLogger(FDangerouslySilentEventHandler.class);

    /**
     * Nah.
     */
    public void onHighWatermark(long duration) {
        LOGGER.warn(String.format(
                "request spent %d ms in the transport buffer, your consumer might be backed up", duration));
    }

    public void onInvalidRequest() {
        LOGGER.warn("Discarding invalid NATS request (no reply)");
    }

    /**
     * Nah.
     */
    public void onNewRequest() {

    }

    /**
     * Nah.
     */
    public void onShutdown() {

    }

    /**
     * Nah.
     */
    public void onApplicationError(TException e) {
        LOGGER.error("error processing request", e);
    }

    /**
     * Nah.
     */
    public void onPublishError(IOException e) {
        LOGGER.warn("failed to request response: " + e.getMessage());
    }
}
