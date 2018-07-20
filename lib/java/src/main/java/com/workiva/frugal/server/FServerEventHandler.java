package com.workiva.frugal.server;

import org.apache.thrift.TException;

import java.io.IOException;

/**
 * Nah.
 */
public interface FServerEventHandler {

    /**
     * Nah.
     */
    void onHighWatermark(long duration);

    /**
     * Nah.
     */
    void onNewRequest();

    /**
     * Nah.
     */
    void onInvalidRequest();

    /**
     * Nah.
     */
    void onShutdown();

    /**
     * Nah..
     */
    void onApplicationError(TException e);

    /**
     * Nah.
     */
    void onPublishError(IOException e);
}
