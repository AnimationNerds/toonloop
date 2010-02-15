#!/usr/bin/env python
"""
Testing GST OpenGL in a GTK Window.
Uses a v4l2 video source.
"""
import os
import sys
if __name__ == "__main__":
    from twisted.internet import gtk2reactor
    gtk2reactor.install()
from twisted.internet import reactor
from twisted.internet import task
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *
import gst

class GlDrawingArea(gtk.DrawingArea, gtk.gtkgl.Widget):
    """
    GTK drawing area which uses OpenGL.
    """
    def __init__(self, verbose=True):
        gtk.DrawingArea.__init__(self)
        # Query the OpenGL extension version.
        if verbose:
            print "OpenGL extension version - %d.%d\n" % gtk.gdkgl.query_version()
        # Configure OpenGL framebuffer.
        # Try to get a double-buffered framebuffer configuration,
        # if not successful then try to get a single-buffered one.
        display_mode = (
            gtk.gdkgl.MODE_RGB |
            gtk.gdkgl.MODE_DEPTH |
            gtk.gdkgl.MODE_DOUBLE
            )
        try:
            glconfig = gtk.gdkgl.Config(mode=display_mode)
        except gtk.gdkgl.NoMatches:
            display_mode &= ~gtk.gdkgl.MODE_DOUBLE
            glconfig = gtk.gdkgl.Config(mode=display_mode)
        if verbose:
            print "is RGBA:", glconfig.is_rgba()
            print "is double-buffered:", glconfig.is_double_buffered()
            print "is stereo:", glconfig.is_stereo()
            print "has alpha:", glconfig.has_alpha()
            print "has depth buffer:", glconfig.has_depth_buffer()
            print "has stencil buffer:", glconfig.has_stencil_buffer()
            print "has accumulation buffer:", glconfig.has_accum_buffer()
        # Set OpenGL-capability to the drawing area
        self.set_gl_capability(glconfig)

class App(object):
    def __init__(self):
        # GTK window:
        self.window = gtk.Window()
        self.window.set_size_request(640, 480)
        self.window.set_title('Testing GST OpenGL')
        self.window.set_reallocate_redraws(True)
        self.window.connect('delete-event', self.on_delete_event)
        self.window.connect('destroy-event', self.on_delete_event)

        # GST pipeline:
        self.pipeline = gst.Pipeline('test_pipeline')
        elements = []
        #self.source = gst.element_factory_make('videotestsrc', 'source_1')
        source = gst.element_factory_make('v4l2src', 'source_1')
        elements.append(source)
        caps = gst.Caps("video/x-raw-yuv, width=320, height=240")
        filter = gst.element_factory_make("capsfilter", "filter")
        filter.set_property("caps", caps)
        elements.append(filter)
        color_fix = gst.element_factory_make('ffmpegcolorspace', 'color_fix')
        elements.append(color_fix)
        queue_element = gst.element_factory_make('queue', 'relax')
        elements.append(queue_element)
        upload = gst.element_factory_make('glupload', 'upload')
        elements.append(upload)
        sink = gst.element_factory_make('glimagesink', 'sink')
        elements.append(sink)
        self.pipeline.add(*elements)
        gst.element_link_many(*elements)

        # Drawing area:
        self.area = GlDrawingArea()
        self.area.set_size_request(640, 480)
        self.window.add(self.area)
        self.window.show_all()

        # When ready, register xid to sink and get a handle to the sink
        self._sink = None
        bus = self.pipeline.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('sync-message::element', self.on_sync_message)
        
        print 'starting the pipeline'
        self.pipeline.set_state(gst.STATE_PLAYING)

        self._draw_task = task.LoopingCall(self.draw)
        self._draw_task.start(1.0, False)

    def on_sync_message(self, bus, message):
        print 'on_sync_message'
        if message.structure is None:
            return
        if message.structure.get_name() == 'prepare-xwindow-id':
            print 'prepare-xwindow-id'
            # Sync with the X server before giving the X-id to the sink
            print 'threads_enter'
            gtk.gdk.threads_enter()
            print "area xid: ", self.area.window.xid
            print 'sync with display'
            gtk.gdk.display_get_default().sync()
            self._sink = message.src
            print 'set xid'
            message.src.set_xwindow_id(self.area.window.xid)
            message.src.set_property('force-aspect-ratio', True)
            print 'threads_leave'
            gtk.gdk.threads_leave()

    def draw(self):
        print 'draw, but sink is none'
        if self._sink is not None:
            #self._sink.expose() ?
            print 'draw'
            gldrawable = self.area.get_gl_drawable() # throws an error
            glcontext = self.area.get_gl_context()
            if gldrawable is None:
                return False
            if not gldrawable.gl_begin(glcontext):
                return False
            glViewport(0, 0, self.area.allocation.width, self.area.allocation.height)
            ratio = 4. / 3.
            w = ratio
            h = 1.
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-w, w, -h, h, -1.0, 1.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

    def on_delete_event(self, widget, event):
        print 'deleted'
        reactor.stop()

    def __del__(self):
        print '__del__'
        self.pipeline.set_state(gst.STATE_NULL)


if __name__ == '__main__':
    app = App()
    reactor.run()
