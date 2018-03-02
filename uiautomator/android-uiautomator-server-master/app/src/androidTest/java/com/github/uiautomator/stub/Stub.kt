/*
 * The MIT License (MIT)
 * Copyright (c) 2015 xiaocong@gmail.com
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
 * OR OTHER DEALINGS IN THE SOFTWARE.
 */

package com.github.uiautomator.stub

import android.support.test.InstrumentationRegistry
import android.support.test.filters.SdkSuppress
import android.support.test.runner.AndroidJUnit4
import android.support.test.uiautomator.UiDevice
import android.test.FlakyTest
import android.test.suitebuilder.annotation.LargeTest
import com.fasterxml.jackson.databind.ObjectMapper
import com.googlecode.jsonrpc4j.JsonRpcServer
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import kotlin.properties.Delegates

/**
 * Use JUnit test to start the uiautomator jsonrpc server.
 * @author xiaocong@gmail.com
 */
RunWith(AndroidJUnit4::class)
SdkSuppress(minSdkVersion = 18)
public class Stub {
    val PORT = 9008
    val server: AutomatorHttpServer by Delegates.lazy { AutomatorHttpServer(PORT) }

    Before
    public fun setUp() {
        server.route("/jsonrpc/0", JsonRpcServer(ObjectMapper(), AutomatorServiceImpl(), javaClass<AutomatorService>()))
        server.start()
        UiDevice.getInstance(InstrumentationRegistry.getInstrumentation()).wakeUp()
    }

    After
    public fun tearDown() {
        server.stop()
    }

    Test
    LargeTest
    FlakyTest(tolerance = 3)
    throws(InterruptedException::class)
    public fun testUIAutomatorStub() {
        while (server.isAlive())
            Thread.sleep(100)
    }

}