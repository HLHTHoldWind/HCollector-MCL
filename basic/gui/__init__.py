"""

HCloud Beta

11/10/2023 rebuild version

"""

# import system requirement
import os
import random
import sys
import shutil
import ctypes
import threading
from threading import Thread, Lock
import time
import configparser
import urllib

# monitor constants
winapi = ctypes.windll.user32
trueWidth = winapi.GetSystemMetrics(0)

# import windows requirement
import winreg
import win32api
import win32clipboard
from ctypes import windll

# import tcl requirement
from tkinter.filedialog import *
from tkinter.simpledialog import *
from ttkbootstrap import *
from ttkbootstrap.tooltip import *
import tkinter.ttk as ttk
import tkinter as tk
from cefpython3 import cefpython
import pywinstyles

# qt requirement
# from PyQt6.QtCore import QUrl
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWidgets import QMainWindow, QApplication

# import technical requirement
import hashlib
import send2trash
import keyboard
import mouse
import numpy as np
import socket
import zipfile
import copy
import webbrowser
import minecraft_launcher_lib
from pynput import mouse as mouse_l
from PIL import Image, ImageTk, ImageSequence
from httpcore import SyncHTTPProxy

# import addition
import basic.git_requests.requests as git_re
import basic.NCE as NCE
import basic.pylib.icoextract as icoextract
import basic.pylib.language as language
import basic.pylib.widget as widget
import basic.launcher as launcher
from basic.gui.browser import MainFrame, BrowserFrame, NavigationBar
from basic.constants import *

# value constants
"Windows constants"
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ZOOM = round((winapi.GetSystemMetrics(0) / trueWidth) + (0.1 * ((winapi.GetSystemMetrics(0) / trueWidth) / 2)), 1)
darwin = sys.platform == 'darwin'
REFRESH_RATE = 120 if getattr(win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1),
                       'DisplayFrequency') > 120 else getattr(win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1),
                       'DisplayFrequency')  # sync

LOCK = threading.Lock()
Image_cache = []
is_mouse_pressed = False

BACKGROUND_C = "#ffffff"
FOREGROUND_C = "#000000"
BACKGROUND_D = "#000000"
FOREGROUND_D = "#ffffff"

LANG = load_lang()

try:

    proxies = urllib.request.getproxies()

    h_address = proxies["http"]

    head = h_address.split("//")[0].rstrip(":")
    a_p = h_address.split("//")[1]
    address = a_p.split(":")[0]
    port = a_p.split(":")[1]

    http_proxy = SyncHTTPProxy((head.encode(), address.encode(), int(port), b''))
    proxies = {'http': http_proxy, 'https': http_proxy}

except:
    pass


class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ScrollText(Text):

    def __init__(self, master):
        self.outframe = Frame(master)
        Text.__init__(self, master=self.outframe, wrap=WORD, background="#1b1b1b",
                      inactiveselectbackground="#909090",
                      foreground="#ffffff",
                      selectbackground="#909090", selectforeground="#303030", insertbackground="#ffffff",
                      highlightcolor="#ffffff", font=("consolas", 12))
        self.vbar = Scrollbar(self.outframe, command=self.cyview, orient=VERTICAL)
        self.hbar = Scrollbar(self.outframe, command=self.cxview, orient=HORIZONTAL)
        self['yscrollcommand'] = self.redirect_yscroll_event
        self['xscrollcommand'] = self.hbar.set
        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.cyview
        self.hbar['command'] = self.cxview
        text_meths = vars(Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.outframe, m))

        for i in COLORS.colors:
            self.tag_config(i.color_code, foreground=i.color_code)

    def cyview(self, *event):
        self.yview(*event)

    def cxview(self, *event):
        self.xview(*event)

    def redirect_mousewheel_event(self, event):
        self.event_generate('<MouseWheel>',
                            x=0, y=event.y, delta=event.delta)
        return "break"

    def redirect_yscroll_event(self, *args, **kwargs):
        self.vbar.set(*args)
        return 'break'


def check_content_color(content: str) -> Color:
    for i in COLORS.colors:
        if content.startswith(i.color):
            return i
        elif i.name in content:
            return i

    return COLORS.NONE


class OutputFrame(LabelFrame):

    def __init__(self, master, name):
        super().__init__(master=master, text=name)
        self._master = master
        self.name = name

        self.console = ScrollText(master=self)
        self.console["state"] = "disabled"

        self.bind("<Configure>", self.resize_all)

    def addline(self, text: str):
        color = check_content_color(text)
        content = text.replace(color.color, "")
        content = content.replace(COLORS.NONE.color, "")
        self.console["state"] = "normal"
        self.console.insert("end", content, color.color_code)
        self.console["state"] = "disabled"

    def resize_all(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()

        self.console.place(x=0, y=0, width=width, height=height)


class AvatarCropperFrame(Frame):
    def __init__(self, master, on_crop_done=None, **kwargs):
        global Image_cache
        super().__init__(master, **kwargs)
        pywinstyles.set_opacity(self, 1.0)

        self.zoom = zoom
        self.on_crop_done = on_crop_done
        self.image = Image.new("RGB", (512, 512), "white")
        self.tk_image = ImageTk.PhotoImage(self.image)
        Image_cache.append(self.tk_image)

        canvas_height = self.tk_image.height()
        canvas_width = self.tk_image.width()
        total_height = canvas_height + self.zoom(25)

        self.config(width=canvas_width, height=total_height)

        self.canvas = Canvas(self, width=canvas_width, height=canvas_height, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        self.start_x = self.zoom(0)
        self.start_y = self.zoom(0)
        self.crop_size = min(canvas_width, canvas_height)
        self.rect = None

        self.dragging = False
        self.resizing = False
        self.original_w = 0
        self.original_h = 0
        self.original_img = Image.new("RGB", (512, 512), "white")
        self.handle_radius = self.zoom(6)
        self.handles = []

        self._draw_overlay()
        self._draw_crop_rect()
        self._create_handles()
        self.update_handles()

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Buttons
        self.btn_cancel = Button(self, text=LANG["control.cancel"], command=self.close, takefocus=False)
        self.btn_ok = Button(self, text=LANG["control.ok"], command=self.crop_avatar, takefocus=False)

        self.master.master._master.textable[self.btn_cancel] = "control.cancel"
        self.master.master._master.textable[self.btn_ok] = "control.ok"
        btn_y = canvas_height + self.zoom(10)
        btn_spacing = self.zoom(10)
        btn_width = self.zoom(80)
        self.btn_cancel.place(x=btn_spacing, y=btn_y, width=btn_width)
        self.btn_ok.place(x=canvas_width - btn_width - btn_spacing, y=btn_y, width=btn_width)

    def close(self, event=None):
        if ENABLE_WIN11_EFFECT:
            pywinstyles.apply_style(self.master.master._master, "acrylic")
        widget.withdraw(self.master, direction="s", fps=REFRESH_RATE)
        self.master.place_forget()

    def open(self, image: Image.Image, event=None):
        global Image_cache
        self.original_img = copy.deepcopy(image)
        self.original_w, self.original_h = self.original_img.size
        self.image = resize_image(image, max_width=zoom(580),
                                  max_height=zoom(350))
        self.tk_image = ImageTk.PhotoImage(self.image)
        Image_cache.append(self.tk_image)

        canvas_height = self.tk_image.height()
        canvas_width = self.tk_image.width()
        total_height = canvas_height + self.zoom(25)

        # Resize the frame and canvas
        self.config(width=canvas_width, height=total_height)
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        # Reset crop box
        self.crop_size = min(canvas_width, canvas_height) - self.zoom(20)
        self.start_x = (canvas_width - self.crop_size) // 2
        self.start_y = (canvas_height - self.crop_size) // 2

        # Redraw
        self._draw_crop_rect()
        self._draw_overlay()
        self.update_handles()

        # Reposition buttons
        btn_y = canvas_height + self.zoom(10)
        btn_spacing = self.zoom(10)
        btn_width = self.zoom(80)

        self.btn_ok.place(x=canvas_width - btn_width - btn_spacing, y=btn_y, width=btn_width)
        self.btn_cancel.place(x=btn_spacing, y=btn_y, width=btn_width)
        self.place(x=(zoom(600)-canvas_width)//2, y=zoom(10), width=canvas_width, height=zoom(380))
        self.master.place(x=0, y=zoom(400), width=zoom(600), height=0)
        widget.move_to(self.master, x=0, y=0, width=zoom(600), height=zoom(400), fps=REFRESH_RATE)

    def _draw_crop_rect(self):
        if self.rect:
            self.canvas.delete(self.rect)
        x1 = self.start_x
        y1 = self.start_y
        x2 = x1 + self.crop_size
        y2 = y1 + self.crop_size
        self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="#4CAF50", width=2)

    def _draw_overlay(self):
        self.canvas.delete("overlay")
        x1, y1 = self.start_x, self.start_y
        x2, y2 = x1 + self.crop_size, y1 + self.crop_size
        w, h = self.tk_image.width(), self.tk_image.height()
        color = "#000000"

        self.canvas.create_rectangle(0, 0, w, y1, fill=color, stipple="gray25", tags="overlay")
        self.canvas.create_rectangle(0, y1, x1, y2, fill=color, stipple="gray25", tags="overlay")
        self.canvas.create_rectangle(x2, y1, w, y2, fill=color, stipple="gray25", tags="overlay")
        self.canvas.create_rectangle(0, y2, w, h, fill=color, stipple="gray25", tags="overlay")

    def _create_handles(self):
        for _ in range(4):
            handle = Label(self, text="", style="secondary.Inverse.TLabel")
            handle.configure(width=1)
            handle.place(width=self.handle_radius * 2, height=self.handle_radius * 2)
            handle.bind("<Button-1>", self.on_handle_press)
            handle.bind("<B1-Motion>", self.on_handle_drag)
            handle.bind("<ButtonRelease-1>", self.on_release)
            self.handles.append(handle)

    def update_handles(self):
        x1, y1 = self.start_x, self.start_y
        x2, y2 = x1 + self.crop_size, y1 + self.crop_size
        positions = [
            (x1, y1),
            (x2, y1),
            (x1, y2),
            (x2, y2),
        ]
        for i, (x, y) in enumerate(positions):
            self.handles[i].place(x=x - self.handle_radius, y=y - self.handle_radius)

    def on_press(self, event):
        x, y = event.x, event.y
        rx1, ry1, rx2, ry2 = self.canvas.coords(self.rect)
        if rx1 <= x <= rx2 and ry1 <= y <= ry2:
            self.dragging = True
            self.drag_offset_x = x - rx1
            self.drag_offset_y = y - ry1

    def on_drag(self, event):
        if self.dragging:
            x = event.x - self.drag_offset_x
            y = event.y - self.drag_offset_y
            x = max(0, min(self.tk_image.width() - self.crop_size, x))
            y = max(0, min(self.tk_image.height() - self.crop_size, y))
            self.start_x = x
            self.start_y = y
            self._draw_crop_rect()
            self._draw_overlay()
            self.update_handles()

    def on_handle_press(self, event):
        widget = event.widget
        self.resizing = True
        self.active_handle = widget

    def on_handle_drag(self, event):
        if not self.resizing:
            return

        handle_index = self.handles.index(self.active_handle)

        mx = self.canvas.canvasx(event.x_root - self.winfo_rootx())
        my = self.canvas.canvasy(event.y_root - self.winfo_rooty())

        x1, y1 = self.start_x, self.start_y
        x2, y2 = x1 + self.crop_size, y1 + self.crop_size

        min_size = self.zoom(40)
        max_width = self.tk_image.width()
        max_height = self.tk_image.height()

        if handle_index == 0:  # NW
            new_size = min(x2 - mx, y2 - my)
            new_size = max(min_size, new_size)
            if x2 - new_size >= 0 and y2 - new_size >= 0:
                self.start_x = x2 - new_size
                self.start_y = y2 - new_size
                self.crop_size = new_size

        elif handle_index == 1:  # NE
            new_size = min(mx - x1, y2 - my)
            new_size = max(min_size, new_size)
            if x1 + new_size <= max_width and y2 - new_size >= 0:
                self.start_y = y2 - new_size
                self.crop_size = new_size

        elif handle_index == 2:  # SW
            new_size = min(x2 - mx, my - y1)
            new_size = max(min_size, new_size)
            if x2 - new_size >= 0 and y1 + new_size <= max_height:
                self.start_x = x2 - new_size
                self.crop_size = new_size

        elif handle_index == 3:  # SE
            new_size = min(mx - x1, my - y1)
            new_size = max(min_size, new_size)
            if x1 + new_size <= max_width and y1 + new_size <= max_height:
                self.crop_size = new_size

        self._draw_crop_rect()
        self._draw_overlay()
        self.update_handles()

    def on_release(self, event):
        self.dragging = False
        self.resizing = False

    def crop_avatar(self):
        # Apply zoom factor to the coordinates and crop size
        x1 = int(self.start_x)
        y1 = int(self.start_y)
        x2 = x1 + int(self.crop_size)
        y2 = y1 + int(self.crop_size)

        scale = self.original_w / self.image.width

        mapped_x1 = int(x1 * scale)
        mapped_y1 = int(y1 * scale)
        mapped_x2 = int(x2 * scale)
        mapped_y2 = int(y2 * scale)

        img = self.original_img.crop((mapped_x1, mapped_y1, mapped_x2, mapped_y2))

        if self.on_crop_done:
            self.on_crop_done(img)

        self.close()
        return self.original_img.crop((mapped_x1, mapped_y1, mapped_x2, mapped_y2))


def resize_image(image, max_width, max_height):
    # Resize the image to fit within max_width and max_height, preserving aspect ratio
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    ratio = min(width_ratio, height_ratio)
    new_width = int(image.width * ratio)
    new_height = int(image.height * ratio)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


# window classes
class MainWindow(Window):

    def __init__(self):
        global BACKGROUND_C, FOREGROUND_C, BACKGROUND_D, FOREGROUND_D
        Window.__init__(self, themename="windows_dark")
        self.withdraw()
        self.drawn = MainViewClass(self)
        self.views = {}
        self.textable = {}
        self.drawn.place(x=0, y=0, width=0, height=0)
        self.Style = Style("windows_dark")
        self.account = User("", 0, "", "", "")
        self.ms_account = MS_User("", "", "", "")
        self.title_now = ""
        BACKGROUND_C = self.Style.colors.get("link")
        FOREGROUND_C = self.Style.colors.get_foreground("link")

        BACKGROUND_D = self.Style.colors.get("dark")
        FOREGROUND_D = self.Style.colors.get_foreground("dark")

    def change_view(self, view: str):
        # self.withdraw()
        self.drawn.withdraw()
        time.sleep(0.5)
        self.views[view].draw()
        self.drawn = self.views[view]

    def destroy_view(self, view: str):
        self.views[view].withdraw(after="d")
        del self.views[view]

    def add_view(self, name, _widget):
        self.views[name] = _widget

    def back_main(self):
        print(self.views.keys())
        if "main_view" in self.views.keys():
            self.change_view("main_view")

    def appear(self):
        self.withdraw()
        self.focus_set()
        _width = self.winfo_width()
        _height = self.winfo_height()
        middle(self, _width, 0)
        self.configure(width=_width, height=0)
        winX = _width
        winY = _height
        maxX = winapi.GetSystemMetrics(0)
        maxY = winapi.GetSystemMetrics(1)
        x = maxX // 2 - winX // 2
        y = maxY // 2 - winY // 2
        self.deiconify()
        widget.move_to(self, x, y, _width, _height, fps=REFRESH_RATE, is_windows=True)

    def disappear(self):
        self.focus_set()
        _width = self.winfo_width()
        _height = self.winfo_height()
        winX = _width
        winY = zoom(0)
        maxX = winapi.GetSystemMetrics(0)
        maxY = winapi.GetSystemMetrics(1)
        x = maxX // 2 - winX // 2
        y = maxY // 2 - winY // 2
        widget.move_to(self, x, maxY + 1, _width, zoom(0), fps=REFRESH_RATE, is_windows=True)
        time.sleep(0.5)
        self.geometry(f"{_width}x{_height}")
        self.withdraw()

        # middle(self, _width, _height)

    def redraw(self, view, viewType, *args):
        self.views[view].withdraw(after="d")
        del self.views[view]
        viewType(self, *args)

    def _close(self):
        self.focus_set()
        _width = self.winfo_width()
        _height = self.winfo_height()
        winX = _width
        winY = zoom(0)
        maxX = winapi.GetSystemMetrics(0)
        maxY = winapi.GetSystemMetrics(1)
        x = maxX // 2 - winX // 2
        y = maxY // 2 - winY // 2
        thread = widget.move_to(self, x, maxY + 1, _width, zoom(0), fps=REFRESH_RATE, is_windows=True)
        thread.join()
        self.quit()
        os._exit(114514)
        self.destroy()
        # thread.join()

    def close(self):
        Thread(target=self._close).start()


class MainViewClass(Frame):

    def __init__(self, main: MainWindow, **kw):
        Frame.__init__(self, master=main, **kw)

    def draw(self):
        self.pack()

    def withdraw(self, after="f"):
        func = self.place_forget if after == "f" else self.destroy
        widget.withdraw(self, fps=REFRESH_RATE, after_funtions=[func])


class InfoWindow(Toplevel):

    def __init__(self, master, title="Info", message="", alert=True, icon=None, bitmap=None,
                 buttonType=("Cancel : danger", "OK : success"), buttonCommands=None):
        super().__init__(master)
        self.transient(master)
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.delete)
        windowInit(self, 300, 150, False, title=title, icon=icon)
        middle(self, zoom(300), zoom(150))
        if buttonCommands is None:
            self.buttonCommands = (self.destroy, self.destroy)
        else:
            self.buttonCommands = buttonCommands
        self.title(title)
        self.iconbitmap(icon)
        self.button_type = buttonType
        self.master = master
        self.alert = alert
        self.buttons = []
        self.buttons2 = []
        messageLabel = ttk.Label(self, text=message)
        picLabel = ttk.Label(self, image=bitmap)
        picLabel.place(x=zoom(10), y=zoom(30), width=zoom(60), height=zoom(60))
        messageHeight = messageLabel.winfo_height()
        y = (zoom(150) - zoom(messageHeight)) / 2
        messageLabel.place(x=zoom(75), y=y - zoom(20))
        self.createButton()

    def close(self, event=None):
        self.destroy()

    def createButton(self):
        buttonFrame = Frame(self)
        times = 0
        self.buttons = []
        self.buttons2 = []
        for i in self.button_type:
            string = i.split(" : ")[0]
            _style = i.split(" : ")[1]
            command = self.buttonCommands[times]
            self.buttons.append(Button(buttonFrame, text=string, style=_style))
            self.buttons[-1].place(x=zoom(times * 60), y=0, width=zoom(60), height=zoom(30))
            self.buttons[-1].configure(command=lambda b=self.buttons[-1]: self.press_button(b))
            if string == "OK":
                button = self.buttons[-1]

                def invoke(event=None):
                    button.invoke()

                self.buttons[-1].bind_all("<Return>", invoke)
            self.buttons2.append(command)
            times += 1
        frameWidth = zoom(60 * len(self.button_type))
        frameHeight = zoom(30)
        x = max(zoom(0), (zoom(300) - frameWidth) - zoom(10))
        buttonFrame.place(x=x + zoom(5), y=zoom(115), width=frameWidth, height=frameHeight)
        # buttonFrame.bind("<ButtonRelease>", self.press_button)

    def delete(self):
        try:
            self.buttons2[-1]()
        except Exception:
            pass
        self.destroy()

    def show(self):
        self.withdraw()
        self.deiconify()
        if self.alert:
            self.bell()
        self.grab_set()
        # self.mainloop()

    def press_button(self, event=None):
        if self.buttons2[self.buttons.index(event)] is not None:
            self.buttons2[self.buttons.index(event)]()
        self.destroy()


# function widget classes
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    def __init__(self, master, *args, **kw):
        Frame.__init__(self, master, *args, **kw)

        self.style_config = Style()

        self.style_config.configure('vsf.secondary.Round.TScrollbar', width=30)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        self.vscrollbar = vscrollbar = Scrollbar(self, orient=VERTICAL, style='vsf.secondary.round.TScrollbar')
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = canvas = Canvas(self, bd=0, highlightthickness=0,
                                      yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)
        canvas.bind("<Unmap>", self.toggle_wheel_off)
        canvas.bind("<Map>", self.toggle_wheel_on)

    def toggle_wheel_on(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def toggle_wheel_off(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if self.winfo_viewable():
            delta = (event.delta / 120) if is_windows() else event.delta
            self.canvas.yview_scroll(int(-1 * delta), "units")


# class WebViewer(QMainWindow):
#     def __init__(self):
#         super(QMainWindow, self).__init__()
#         self.browser = QWebEngineView()
#         self.setCentralWidget(self.browser)
#         self.showMaximized()
#
#     def show(self):
#         app = QApplication(sys.argv)
#         QApplication.setApplicationName(LANG["account.microsoft.title"])


class AccountFrame(Frame):

    def __init__(self, master, size: tuple, img_path, username: str, mail_add: str, style_name, **kw):
        """ Size should be 4 : 1 """
        global Image_cache
        Frame.__init__(self, master=master, **kw)
        self.size = size

        width, height = size[0:2]
        font_ratio = height / ZOOM / 100

        size = height - zoom(10)
        color = BACKGROUND_D
        im = Image.open(img_path).convert("RGBA").resize((1024, 1024))
        # im.show()

        im2 = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\avatar_frame.png")

        data = np.array(im2)  # "data" is a height x width x 4 numpy array  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = hex_to_rgb(color)  # Transpose back needed

        # im2 = Image.fromarray(data)

        pixels = im.load()
        pixels2 = im2.load()

        _w, _h = im2.size
        for _x in range(_w):
            for _y in range(_h):
                if pixels2[_x, _y][-1] == 255:
                    pixels[_x, _y] = (0, 0, 0, 0)

        im = im.resize((im2.width, im2.width))

        # im.show()

        self.img = Image.new('RGBA', (im2.width, im2.width))
        self.img.paste(im, (0, 0))
        # img.paste(im2, (0, 0), im2)
        # print(im2.getpixel((500, 500)))
        img = self.img.resize((size, size))
        pic = ImageTk.PhotoImage(img)
        Image_cache.append(pic)

        color = FOREGROUND_D
        color2 = BACKGROUND_D

        self.username = username
        self.mail_add = mail_add

        self.avatar = Label(self, borderwidth=0, image=pic)

        self.avatar.place(x=width - height + zoom(5), y=zoom(5), width=size, height=size)

        self.name_label = Label(self, text=username, anchor='e',
                                font=("Arial", max(round(30 * font_ratio), 1)))
        self.name_label.place(x=zoom(5), y=zoom(5),
                              width=round(width * 0.75) - round(zoom(25) * font_ratio),
                              height=round(height * 0.67) - zoom(5))
        self.mail_label = Label(self, text=mail_add, anchor='e',
                                font=("Arial", max(round(14 * font_ratio), 1)))
        self.mail_label.place(x=zoom(5), y=round(height * 0.67) - round(zoom(10) * font_ratio),
                              width=round(width * 0.75) - round(zoom(25) * font_ratio),
                              height=round(height * 0.33) - zoom(5))

        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event=None):
        global Image_cache
        self.size = size = (self.winfo_width(), self.winfo_height())

        width, height = size[0:2]
        font_ratio = height / ZOOM / 100

        size = height - zoom(10)

        img = self.img.resize((size, size))
        pic = ImageTk.PhotoImage(img)
        Image_cache.append(pic)

        self.avatar.configure(image=pic)

        self.avatar.place(x=width - height + zoom(5), y=zoom(5), width=size, height=size)

        self.name_label.configure(text=self.username, anchor='e',
                                font=("Arial", max(round(30 * font_ratio), 1)))
        self.name_label.place(x=zoom(5), y=zoom(5),
                              width=round(width * 0.75) - round(zoom(25) * font_ratio),
                              height=round(height * 0.67) - zoom(5))
        self.mail_label.configure(text=self.mail_add, anchor='e',
                                font=("Arial", max(round(14 * font_ratio), 1)))
        self.mail_label.place(x=zoom(5), y=round(height * 0.67) - round(zoom(10) * font_ratio),
                              width=round(width * 0.75) - round(zoom(25) * font_ratio),
                              height=round(height * 0.33) - zoom(5))

    def _update(self, img_path, username: str, mail_add: str):
        global Image_cache
        size = self.size
        width, height = size[0:2]
        font_ratio = height / ZOOM / 100

        size = height - zoom(10)
        color = BACKGROUND_D
        im = Image.open(img_path).convert("RGBA").resize((1024, 1024))
        # im.show()

        im2 = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\avatar_frame.png").resize((1024, 1024))

        data = np.array(im2)  # "data" is a height x width x 4 numpy array  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = hex_to_rgb(color)  # Transpose back needed

        # im2 = Image.fromarray(data)

        pixels = im.load()
        pixels2 = im2.load()

        _w, _h = im2.size
        for _x in range(_w):
            for _y in range(_h):
                if pixels2[_x, _y][-1] == 255:
                    pixels[_x, _y] = (0, 0, 0, 0)

        im = im.resize((im2.width, im2.width))

        self.img = im
        img = self.img.resize((size, size))
        pic = ImageTk.PhotoImage(img)
        Image_cache.append(pic)

        self.username = username
        self.mail_add = mail_add

        self.avatar.configure(image=pic)
        self.name_label.configure(text=username)
        self.mail_label.configure(text=mail_add)


def set_transparent_widgets(parent: tk.Widget, value):
    widget_list = parent.winfo_children()
    pywinstyles.set_opacity(parent, value=value)
    for _widget in widget_list:
        if "label" not in _widget.winfo_name():
            pywinstyles.set_opacity(_widget, value=value)
        else:
            pywinstyles.set_opacity(_widget, value=1)


# MainView
class MainAppView(MainViewClass):

    def __init__(self, master: MainWindow):
        global Image_cache
        MainViewClass.__init__(self, master)
        self.stat = "launch"
        self.is_alive = False
        self.is_pause = False
        self.is_download = False
        self.is_setting = False
        self.inset_pro = False
        self.is_account = False
        self.is_preference = False
        self.background_p = None
        self.now_download = ""
        self.speed_timer = 0
        self.speed_time = 0
        self.speed_size = 0
        self.speed = 0
        self._master = master
        self._master.add_view("main_view", self)
        self.minecraft = None
        self.ms_account = self._master.ms_account
        Thread(target=self._sign_in_ms_thread).start()

        self.server_list = ["HCollection", "Crossline"]
        self.server_version = ["1.20.1", "1.21.3"]
        self.server_select = self.server_list[0]
        self.server_backgrounds = []
        self.server_backgrounds_org = []
        self.launcher = launcher.Launcher(self.server_list)

        self.Style = Style()
        self.Style.configure("bold.primary.TButton", font=("Arial", "15", "bold"))
        self.Style.configure("side.dark.TButton", relief="flat", font=("Arial", 20, "bold"),
                             anchor="w", compound="left", justify="left")

        self.background = Canvas(self)
        self.progressbar = Frame(self, bootstyle="light")
        self.topbar = Frame(self)
        self.sidebar = Frame(self)
        self.server_frame = Frame(self.sidebar)
        self.set_side_frame = Frame(self.sidebar)
        self.prefen_frame = Frame(self.topbar)
        self.acc_set_frame = Frame(self.topbar)
        self.title_label = Label(self.topbar, font=("Arial", 25, "bold"))
        ms_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\microsoft_logo.png").resize((32, 32))
        sync_set_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\setting_sync.png").resize((40, 40))
        set_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\setting.png").resize((40, 40))
        acc_mig_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\account_migrate.png").resize((40, 40))
        ms_img_tk = ImageTk.PhotoImage(ms_img)
        sync_set_tk = ImageTk.PhotoImage(sync_set_img)
        set_tk = ImageTk.PhotoImage(set_img)
        acc_mig_tk = ImageTk.PhotoImage(acc_mig_img)
        Image_cache.append(ms_img_tk)
        Image_cache.append(sync_set_tk)
        Image_cache.append(set_tk)
        Image_cache.append(acc_mig_tk)
        Image_cache.append(ms_img)
        Image_cache.append(sync_set_img)
        Image_cache.append(set_img)
        Image_cache.append(acc_mig_img)
        self.ms_btn = Button(self.topbar, image=ms_img_tk, command=self.get_ms_info, takefocus=False)
        self.sync_set_btn = Button(self.sidebar, image=sync_set_tk, command=self.migrate_setting, takefocus=False)
        self.set_btn = Button(self.sidebar, image=set_tk, command=self.switch_setting, takefocus=False)
        self.acc_mig_btn = Button(self.sidebar, image=acc_mig_tk, command=self.migrate_account, takefocus=False)
        self.background.configure(background="#1b1b1b", bd=0, highlightthickness=0)
        _account = self._master.account
        self.account_frame = Frame(self)

        self.server_btns = []
        server_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\local_icon.png").resize((45, 45))
        server_img_tk = ImageTk.PhotoImage(server_img)
        Image_cache.append(server_img_tk)
        Image_cache.append(server_img)
        for server in self.server_list:
            self.server_btns.append(Button(self.server_frame, style="dark.TButton", text="  " + server,
                                           image=server_img_tk,
                                           command=self.change_server_lambda(self.server_list.index(server)),
                                           takefocus=False, compound="left"))

        self.migrate_frame = Frame(self)
        self.migrate_entry = Label(self.migrate_frame, font=("Arial", 10))
        self.migrate_label = Label(self.migrate_frame, text=LANG["main.interface.migrate_acc.title"],
                                   font=("Arial", 10))
        self.migrate_close = Button(self.migrate_frame, text=LANG["control.close"], command=self.close_migrate,
                                    takefocus=False)
        self.migrate_ok = Button(self.migrate_frame, text=LANG["control.ok"], command=self.start_migrate,
                                 takefocus=False)

        self._master.textable[self.migrate_label] = "main.interface.migrate_acc.title"
        self._master.textable[self.migrate_close] = "control.close"
        self._master.textable[self.migrate_ok] = "control.ok"

        self.console = OutputFrame(self, "Minecraft Console")

        self.launch_btn = Button(self, text=LANG[f"main.control.{self.stat}"].upper(),
                                 style="bold.primary.TButton", command=self.operation, takefocus=False)

        self._master.textable[self.launch_btn] = f"main.control.{self.stat}"
        self.progress = Progressbar(self.progressbar, style='Striped.Horizontal.TProgressbar')
        self.progress_status = Label(self.progressbar, style="primary.Inverse.TLabel")
        self.progress_title = Label(self.progressbar, style="primary.Inverse.TLabel")
        self.avatar_frame = Frame(self)
        self.avatar_selector = AvatarCropperFrame(self.avatar_frame, on_crop_done=self.update_avatar)

        acc_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\account.png").resize((45, 45))
        wre_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\wrench.png").resize((45, 45))
        exit_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\exit.png").resize((45, 45))
        dc_img = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\discord.png").resize((45, 45))

        acc_tk = ImageTk.PhotoImage(acc_img)
        wre_tk = ImageTk.PhotoImage(wre_img)
        exit_tk = ImageTk.PhotoImage(exit_img)
        dc_tk = ImageTk.PhotoImage(dc_img)

        Image_cache.append([acc_tk, wre_tk, exit_tk, dc_tk])

        self.account_set_btn = Button(self.set_side_frame,
                                      text="  "+LANG["setting.account"], image=acc_tk, takefocus=False, compound="left",
                                      command=self.switch_account_set)
        self.wre_set_btn = Button(self.set_side_frame,
                                  text="  "+LANG["setting.configure"], image=wre_tk, takefocus=False, compound="left",
                                  command=self.switch_preference)
        self.logout_btn = Button(self.set_side_frame,
                                 text="  "+LANG["account.signout"], image=exit_tk, takefocus=False,
                                 command=self.logout, compound="left")

        self.acc_re_ms_btn = Button(self.acc_set_frame, text=LANG["setting.account.relogin_ms"],
                                    command=self.re_login, takefocus=False)
        self.acc_change_avatar = Button(self.acc_set_frame,
                                        text=LANG["setting.account.change_avatar"], command=self.change_avatar,
                                        takefocus=False)

        self.lang_tip = Label(self.prefen_frame, text=LANG["setting.configure.language"], font=("Arial", 10))
        self.lang_selector = Combobox(self.prefen_frame, state="readonly", values=list(LANG_DICT.keys()))
        self.lang_selector.bind("<<ComboboxSelected>>", self.change_lang)
        self.lang_selector.current(list(LANG_DICT.keys()).index(LANG["default.fullname"]))

        self.game_path_tip = Label(self.prefen_frame, text=LANG["setting.configure.game_path"], font=("Arial", 10))
        self.game_path_entry = Entry(self.prefen_frame, state="disabled")
        self.game_path_btn = Button(self.prefen_frame, text=LANG["control.choose"], command=self.change_game_path,
                                    takefocus=False)

        self.discord_btn = Button(self.prefen_frame, text=LANG["setting.discord"], command=self.open_dc_web,
                                  takefocus=False, image=dc_tk, compound="left")

        self.ram_controller = Meter(self.prefen_frame,
                                    amounttotal=round(TOTAL_RAM / (1024**3)),
                                    amountused=int(CONFIG["CONFIG"]["ram"])//1024,
                                    bootstyle='success.TMeter', textright="G",
                                    subtext=LANG["setting.configure.ram"],
                                    stripethickness=0, interactive=True,
                                    textfont=("Arial", 20), subtextfont=("Arial", 10))

        self.ram_controller.bind_all("<ButtonRelease-1>", self.set_ram)

        game_path = CONFIG["CONFIG"]["game_path"]

        self.game_path_entry["state"] = "normal"
        self.game_path_entry.delete(0, "end")
        self.game_path_entry.insert(0, game_path)
        self.game_path_entry["state"] = "disabled"

        self._master.textable[self.account_set_btn] = "setting.account"
        self._master.textable[self.discord_btn] = "setting.discord"
        self._master.textable[self.wre_set_btn] = "setting.configure"
        self._master.textable[self.logout_btn] = "account.signout"
        self._master.textable[self.acc_re_ms_btn] = "setting.account.relogin_ms"
        self._master.textable[self.acc_change_avatar] = "setting.account.change_avatar"
        self._master.textable[self.lang_tip] = "setting.configure.language"
        self._master.textable[self.game_path_tip] = "setting.configure.game_path"
        self._master.textable[self.game_path_btn] = "control.choose"

        Thread(target=self.get_server_state).start()
        self.load_backgrounds()

    def draw(self):
        self.is_alive = True
        self.is_setting = False
        self.inset_pro = False
        self.is_account = False
        self.is_preference = False
        self._master.style.theme_use("launcher_dark")
        self._master.protocol("WM_DELETE_WINDOW", self.close)
        Thread(target=self._sign_in_ms_thread).start()
        if ENABLE_WIN11_EFFECT:
            pywinstyles.apply_style(self._master, "acrylic")
            pywinstyles.set_opacity(self.background, value=0.5)
            set_transparent_widgets(self.topbar, 0.8)
            set_transparent_widgets(self.sidebar, 0.6)
            set_transparent_widgets(self.progressbar, 0.8)
            set_transparent_widgets(self.launch_btn, 0.9)
            set_transparent_widgets(self.migrate_frame, 0.9)

        else:
            pywinstyles.set_opacity(self.background, value=0.5)
            set_transparent_widgets(self.topbar, 0.8)
            set_transparent_widgets(self.sidebar, 0.6)
            set_transparent_widgets(self.progressbar, 0.8)
            set_transparent_widgets(self.launch_btn, 0.8)
            set_transparent_widgets(self.migrate_frame, 0.9)

        _account = self._master.account
        self.account_frame = AccountFrame(self.topbar, (zoom(200), zoom(50)), _account.avatar, _account.name,
                                          _account.email, "dark")

        # set_transparent_widgets(self.account_frame, 1)

        self.Style = Style()
        self.Style.configure("bold.primary.TButton", font=("Arial", "15", "bold"))
        self.Style.configure("bold.danger.TButton", font=("Arial", "15", "bold"))
        self.Style.configure("bold.primary.Inverse.TLabel", font=("Arial", "9", "bold"))
        self.Style.configure("side.light.Link.TButton", relief="flat", font=("Arial", 15, "bold"),
                             anchor="w", compound="left", justify="left")
        self.Style.configure("rside.light.Link.TButton", relief="flat", font=("Arial", 15, "bold"),
                             anchor="e", compound="left", justify="left")
        self.Style.configure("bold.light.Link.TButton", font=("Arial", 15, "bold"), relief="flat")
        self.launch_btn.configure(style="bold.primary.TButton")
        self.ms_btn.configure(style="bold.light.Link.TButton")
        self.set_btn.configure(style="bold.light.Link.TButton")
        self.acc_re_ms_btn.configure(style="bold.light.Link.TButton")
        self.acc_change_avatar.configure(style="bold.light.Link.TButton")
        self.sync_set_btn.configure(style="bold.light.Link.TButton")
        self.acc_mig_btn.configure(style="bold.light.Link.TButton")
        self.progress_title.configure(style="bold.primary.Inverse.TLabel")
        self.progress_status.configure(style="bold.primary.Inverse.TLabel")
        self.migrate_close.configure(style="bold.light.Link.TButton")
        self.migrate_ok.configure(style="bold.light.Link.TButton")
        self.account_set_btn.configure(style="side.light.Link.TButton")
        self.wre_set_btn.configure(style="side.light.Link.TButton")
        self.logout_btn.configure(style="side.light.Link.TButton")
        self.discord_btn.configure(style="rside.light.Link.TButton")

        self.console.console.configure(wrap=WORD, background="#232323",
                                       inactiveselectbackground="#909090",
                                       foreground="#ffffff",
                                       selectbackground="#909090", selectforeground="#303030",
                                       insertbackground="#ffffff",
                                       highlightcolor="#ffffff", font=("consolas", 9))

        for btn in self.server_btns:
            btn.configure(style="side.light.Link.TButton")

        self.set_button()

        width, height = self._master.winfo_width(), self._master.winfo_height()
        self._master.title(LANG["software.name"])
        self._master.title_now = LANG["software.name"]
        self.set_background()
        self.place(x=width // 2, y=height // 2, width=0, height=0)
        _x, _y = get_middle_xy(self._master, zoom(600), zoom(400))
        self.background.place(x=0, y=0, width=zoom(600), height=zoom(400))
        self.title_label.place(x=zoom(10), y=0, width=zoom(340), height=zoom(50))
        self.topbar.place(x=0, y=0, width=zoom(600), height=zoom(50))
        self.account_frame.place(x=zoom(400), y=0, width=zoom(200), height=zoom(50))
        self.ms_btn.place(x=zoom(275), y=0, width=zoom(50), height=zoom(50))
        self.sidebar.place(x=0, y=zoom(50), width=zoom(200), height=zoom(350))
        self.server_frame.place(x=0, y=0, width=zoom(200), height=zoom(300))
        self.set_side_frame.place(x=0, y=0, width=zoom(0), height=zoom(300))
        self.sync_set_btn.place(x=zoom(50), y=zoom(300), width=zoom(50), height=zoom(50))
        self.set_btn.place(x=0, y=zoom(300), width=zoom(50), height=zoom(50))
        self.acc_mig_btn.place(x=zoom(100), y=zoom(300), width=zoom(50), height=zoom(50))
        self.launch_btn.place(x=zoom(600 - 200 - 25), y=zoom(400 - 50 - 25), width=zoom(200), height=zoom(50))
        self.progress_title.place(x=0, y=0, width=zoom(350), height=zoom(25))
        self.progress.place(x=0, y=zoom(25), width=zoom(350), height=zoom(25))
        self.progress_status.place(x=0, y=zoom(50), width=zoom(350), height=zoom(25))
        self.migrate_label.place(x=0, y=zoom(0), width=zoom(200), height=zoom(25))
        self.migrate_entry.place(x=0, y=zoom(25), width=zoom(200), height=zoom(25))
        self.migrate_ok.place(x=0, y=zoom(50), width=zoom(100), height=zoom(25))
        self.migrate_close.place(x=zoom(100), y=zoom(50), width=zoom(100), height=zoom(25))
        self.migrate_frame.place(x=zoom(125), y=zoom(375), width=zoom(0), height=zoom(0))
        self.account_set_btn.place(x=0, y=0, width=zoom(200), height=zoom(50))
        self.wre_set_btn.place(x=0, y=zoom(50), width=zoom(200), height=zoom(50))
        self.logout_btn.place(x=0, y=zoom(250), width=zoom(200), height=zoom(50))

        self.acc_re_ms_btn.place(x=0, y=zoom(50), width=zoom(400), height=zoom(50))
        self.acc_change_avatar.place(x=0, y=0, width=zoom(400), height=zoom(50))
        self.acc_set_frame.place_forget()
        self.prefen_frame.place_forget()

        self.lang_tip.place(x=0, y=0, width=zoom(250), height=zoom(25))
        self.lang_selector.place(x=zoom(250), y=0, width=zoom(150), height=zoom(25))
        self.game_path_tip.place(x=0, y=zoom(25), width=zoom(300), height=zoom(25))
        self.game_path_entry.place(x=0, y=zoom(50), width=zoom(300), height=zoom(25))
        self.game_path_btn.place(x=zoom(300), y=zoom(50), width=zoom(100), height=zoom(25))
        self.discord_btn.place(x=zoom(0), y=zoom(300), width=zoom(400), height=zoom(50))
        self.ram_controller.place(x=zoom(100), y=zoom(100), width=zoom(200), height=zoom(200))
        self.ram_controller._draw_base_image()
        self.ram_controller._draw_meter()

        b_y = 0
        for btn in self.server_btns:
            btn.place(x=0, y=b_y, width=zoom(200), height=zoom(50))
            b_y += zoom(50)

        widget.move_to(self._master, x=_x, y=_y, width=zoom(600), height=zoom(400), fps=REFRESH_RATE, is_windows=True)
        widget.move_to(self, x=0, y=0, width=zoom(600), height=zoom(400), fps=REFRESH_RATE)
        Thread(target=self.start_animation).start()
        self.avatar_frame.place(x=0, y=zoom(400), width=zoom(600), height=0)
        debug("Main Frame Drawn", COLORS.CYAN, "GUI")

    def open_setting(self):
        self.is_setting = True
        self.inset_pro = True
        if not self.is_account and not self.is_preference:
            self.is_account = True
        light = 0.9
        widget.move_to(self.server_frame, x=0, y=0, width=zoom(0), height=zoom(300), fps=REFRESH_RATE)
        if not self.is_download:
            widget.fade_out(self.launch_btn, light=light, fps=REFRESH_RATE)
        time.sleep(0.5)
        widget.move_to(self.set_side_frame, x=0, y=0, width=zoom(200), height=zoom(300), fps=REFRESH_RATE)
        widget.move_to(self.topbar, x=0, y=0, width=zoom(600), height=zoom(400), fps=REFRESH_RATE)
        time.sleep(0.5)
        if self.is_account:
            self.open_account_set()
        else:
            self.open_preference()
        time.sleep(0.5)

    def close_setting(self):
        self.is_setting = False
        self.inset_pro = True
        light = 0.9
        if self.is_account:
            self.close_account_set()
            time.sleep(0.5)
        elif self.is_preference:
            self.close_preference()
        self.inset_pro = True
        widget.move_to(self.set_side_frame, x=0, y=0, width=zoom(0), height=zoom(300), fps=REFRESH_RATE)
        widget.move_to(self.topbar, x=0, y=0, width=zoom(600), height=zoom(50), fps=REFRESH_RATE)
        time.sleep(0.5)
        widget.move_to(self.server_frame, x=0, y=0, width=zoom(200), height=zoom(300), fps=REFRESH_RATE)
        if not self.is_download:
            widget.fade_in(self.launch_btn, light=light, fps=REFRESH_RATE)
        time.sleep(0.5)
        self.inset_pro = False

    def open_account_set(self):
        self.inset_pro = True
        self.is_account = True
        if self.is_preference:
            self.close_preference()
            self.is_preference = False
        widget.move_to(self.account_frame, x=zoom(400), y=zoom(50), width=zoom(200), height=zoom(50),
                       fps=REFRESH_RATE, delay=0.25)
        time.sleep(0.25)
        widget.move_to(self.account_frame, x=zoom(200), y=zoom(50), width=zoom(360), height=zoom(90),
                       fps=REFRESH_RATE)
        time.sleep(0.25)
        self.acc_set_frame.place(x=zoom(200), y=zoom(140), width=zoom(400), height=zoom(350))
        widget.fade_in(self.acc_re_ms_btn, fps=REFRESH_RATE)
        widget.fade_in(self.acc_change_avatar, fps=REFRESH_RATE)
        self.inset_pro = False

    def close_account_set(self):
        self.inset_pro = True
        widget.fade_out(self.acc_re_ms_btn, fps=REFRESH_RATE)
        widget.fade_out(self.acc_change_avatar, fps=REFRESH_RATE)
        widget.move_to(self.account_frame, x=zoom(400), y=zoom(50), width=zoom(200), height=zoom(50),
                       fps=REFRESH_RATE)
        time.sleep(0.5)
        self.acc_set_frame.place_forget()
        widget.move_to(self.account_frame, x=zoom(400), y=0, width=zoom(200), height=zoom(50),
                       fps=REFRESH_RATE, delay=0.25)
        self.inset_pro = False

    def switch_account_set(self):
        if self.inset_pro:
            return 0
        if not self.is_account:
            Thread(target=self.open_account_set).start()

    def switch_preference(self):
        if self.inset_pro:
            return 0
        if not self.is_preference:
            Thread(target=self.open_preference).start()

    def open_preference(self):
        self.is_preference = True
        self.inset_pro = True

        if self.is_account:
            self.close_account_set()
            self.is_account = False
        # elif self.is_preference:
        #     self.close_preference()

        time.sleep(0.5)
        self.prefen_frame.place(x=zoom(200), y=zoom(50), width=zoom(400), height=zoom(350))
        widget.fade_in(self.prefen_frame, fps=REFRESH_RATE)
        self.inset_pro = False

    def close_preference(self):
        self.inset_pro = True
        widget.fade_out(self.prefen_frame, fps=REFRESH_RATE)
        time.sleep(0.5)
        self.prefen_frame.place_forget()
        self.inset_pro = False

    def switch_setting(self):
        if self.inset_pro:
            return 0
        if self.is_setting:
            Thread(target=self.change_title).start()
            Thread(target=self.close_setting).start()
        else:
            Thread(target=widget.label_print, args=(self.title_label, "Setting", 0.5)).start()
            Thread(target=self.open_setting).start()

    def change_game_path(self):
        path = askdirectory()
        if os.path.isdir(path):
            CONFIG["CONFIG"]["game_path"] = path
            with open(CONFIG_PATH, "w") as cf:
                CONFIG.write(cf)
            self.game_path_entry["state"] = "normal"
            self.game_path_entry.delete("all")
            self.game_path_entry.insert(0, path)
            self.game_path_entry["state"] = "disabled"

    def open_dc_web(self):
        webbrowser.open("https://discord.gg/tjvkRMkthD")

    def set_ram(self, event=None):
        value = str(self.ram_controller["amountused"])
        CONFIG["CONFIG"]["ram"] = value * 1024
        with open(CONFIG_PATH, "w") as cf:
            CONFIG.write(cf)

    def migrate_account(self):
        time.sleep(0.05)
        self.migrate_entry.configure(text=self.ms_account.name)
        widget.move_to(self.migrate_frame, x=zoom(200), y=zoom(112), width=zoom(200), height=zoom(75), fps=REFRESH_RATE)

    def close_migrate(self):
        self.focus_set()
        widget.move_to(self.migrate_frame, x=zoom(125), y=zoom(375), width=zoom(0), height=zoom(0),
                       fps=REFRESH_RATE, after_functions=[self.migrate_frame.place_forget])

    def start_migrate(self):
        self.focus_set()
        Thread(target=self._migrate_account, args=(self.ms_account.name,)).start()

    def _migrate_account(self, old_name):
        name = self.ms_account.name
        old_id = self.ms_account.uuid
        _socket = self.connect_server()
        _socket.sendall(f"migrate_ms{SEPARATOR}{GENERAL_AUTH}".encode())
        _socket.recv(BUFFER_SIZE)
        mail_add = self._master.account.email
        password = self._master.account.password

        S = SEPARATOR
        message = f"{mail_add}{S}{covert_password(password)}{S}{name}{S}{old_id}{S}{old_name}"
        content = NCE.encryption_key(message, SALT)
        _socket.sendall(content.encode())

        state = _socket.recv(BUFFER_SIZE).decode()
        widget.move_to(self.migrate_frame, x=zoom(125), y=zoom(375), width=zoom(0), height=zoom(0),
                       fps=REFRESH_RATE, after_functions=[self.migrate_frame.place_forget])
        if state == "success_sign":
            return 0

        else:
            return 1

    def change_lang(self, event=None, langs=None):
        global LANG
        self.focus_set()
        if langs is None:
            langs = self.lang_selector.get()

        CONFIG["CONFIG"]["lang"] = LANG_DICT[langs]
        with open(CONFIG_PATH, "w") as cf:
            CONFIG.write(cf)

        LANG = load_lang()
        for i in self._master.textable.keys():
            i.configure(text=LANG[self._master.textable[i]])
        self._master.title_now = LANG["software.name"]

        self.account_set_btn.configure(text="  " + LANG["setting.account"])
        self.wre_set_btn.configure(text="  " + LANG["setting.configure"])
        self.logout_btn.configure(text="  " + LANG["account.signout"])
        self.launch_btn.configure(text=LANG["main.control.launch"].upper())
        self.ram_controller.subtext.configure(text=LANG["setting.configure.ram"])
        self.ram_controller.subtext.update()

        self._master.title(self._master.title_now)

    def re_login(self):
        self.is_alive = False
        self.account_frame.destroy()
        self._master.change_view("microsoft_bind")

    def logout(self, event=None):
        user_ini["USER"]["remember"] = "false"
        with open(USER_CONFIG, "w") as file:
            user_ini.write(file)

        del self._master.views["account"]

        def back():
            AccountView(self._master)
            self.account_frame.destroy()
            self.is_alive = False
            Thread(target=self._master.disappear).start()
            time.sleep(0.5)
            self._master.change_view("account")

        Thread(target=back).start()

    def change_avatar(self, event=None):
        supported_extensions = Image.registered_extensions()
        # Filter only readable formats and convert to file dialog patterns (e.g., "*.jpg")
        file_patterns = [
            f"*{ext}" for ext, fmt in supported_extensions.items()
            if fmt in Image.OPEN  # Ensures read support
        ]
        file_path = askopenfilename(
            title=LANG["account.upload_avatar"],
            filetypes=[(LANG["misc.supported_file"], tuple(file_patterns))]
        )
        if file_path:
            if ENABLE_WIN11_EFFECT:
                pywinstyles.apply_style(self._master, "dark")
            img = Image.open(file_path)
            self.avatar_selector.open(img)

    def update_avatar(self, img: Image.Image):
        img.save(f"{DATA_PATH}\\temp_avatar.png")
        _socket = self.connect_server()
        start_time = time.time()
        _socket.sendall(f"upload_avatar{SEPARATOR}{GENERAL_AUTH}".encode())
        _socket.recv(BUFFER_SIZE)
        mail_add = self._master.account.email
        password = self._master.account.password

        content = NCE.encryption_key(f"{mail_add}{SEPARATOR}{covert_password(password)}", SALT)
        _socket.sendall(content.encode())

        state = _socket.recv(BUFFER_SIZE).decode()
        if state == "next":
            with open(f"{DATA_PATH}\\temp_avatar.png", "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in
                    # busy networks
                    _socket.sendall(bytes_read)

            _socket.close()

            Thread(target=self._get_avatar).start()

        else:
            end = time.time()

            if end - start_time < 0.75:
                time.sleep(0.75 - (end - start_time))

    def _get_avatar(self):
        time.sleep(1)
        self.socket = self.connect_server()
        self.socket.sendall(f"get_avatar{SEPARATOR}{GENERAL_AUTH}".encode())
        self.socket.recv(BUFFER_SIZE)
        self.socket.sendall(NCE.encryption_key(self._master.account.email, SALT).encode())

        with open(f"{DATA_PATH}\\avatar.png", "wb") as file:
            while True:
                bytes_read = self.socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                file.write(bytes_read)

        avatar = f"{DATA_PATH}\\avatar.png"
        self.socket.close()
        self._master.account = User(self._master.account.email,
                                    self._master.account.uid,
                                    self._master.account.name,
                                    self._master.account.password,
                                    avatar)

        self.account_frame._update(avatar, self._master.account.name, self._master.account.email)

    def set_download_status(self, status):
        self.progress_status.configure(text=status)

    def set_download_progress(self, progress):
        self.progress["value"] = progress

    def set_download_max(self, max):
        self.progress["maximum"] = int(max)
        self.progress_title.configure(text=LANG["main.interface.downloading"])

    def load_backgrounds(self):
        global Image_cache
        for name in self.server_list:
            self.server_backgrounds.append([])
            self.server_backgrounds_org.append([])
            index = self.server_list.index(name)
            for _file in os.listdir(f"{RUN_PATH}\\assets\\backgrounds\\{name}"):
                img = widget.get_image_fill(Image.open(f"{RUN_PATH}\\assets\\backgrounds\\{name}\\{_file}"),
                                            (zoom(600), zoom(400)))
                # img.show()
                img_t = ImageTk.PhotoImage(img)
                self.server_backgrounds_org[index].append(img)
                self.server_backgrounds[index].append(img_t)
                Image_cache.append(img)
                Image_cache.append(img_t)

    def change_server_lambda(self, server_id: int):
        def change_server():
            self.server_select = self.server_list[server_id]
            self.update_server_select()

        return change_server

    def update_server_select(self):
        Thread(target=self.get_server_state).start()
        if self.server_select == "Crossline":
            self.stat = "notopen"
            self.launch_btn.configure(text=LANG[f"main.control.notopen"].upper())
        Thread(target=self.set_background_anmiate).start()
        Thread(target=self.change_title).start()

    def get_server_update(self):
        if self.check_update():
            self.stat = "update"
        if self.server_select == "Crossline":
            self.stat = "notopen"
        self.launch_btn.configure(text=LANG[f"main.control.{self.stat}"].upper())

    def get_server_state(self):
        nogame = False
        debug(f"Getting Server Status", COLORS.CYAN, "GUI")
        if self.ms_account.token == "":
            self.stat = "logging_in"
        elif not self.launcher.available_versions[self.server_select].available:
            self.stat = "download"
            nogame = True
        elif not os.path.exists(f"{RUN_PATH}\\java\\jdk-21"):
            self.stat = "download_j"
            nogame = True
        else:
            self.stat = "launch"
        if self.server_select == "Crossline":
            self.stat = "notopen"
        else:
            if not nogame:
                Thread(target=self.get_server_update).start()

        try:
            self.launch_btn.configure(text=LANG[f"main.control.{self.stat}"].upper())
        except RuntimeError:
            pass

    def check_update(self):
        urllib.request.urlretrieve(f"{ARCHIVE_HOST}/minecraft/hversion.txt",
                                   f"{DATA_PATH}\\temp.txt")
        with open(f"{DATA_PATH}\\temp.txt", "r") as f:
            version = int(f.readline().strip())

        if self.launcher.available_versions[self.server_select].version != version:
            return True
        else:
            return False

    def operation(self):
        self.focus_set()
        if self.stat == "download":
            Thread(target=self.download, args=(self.HC_downloader,)).start()
        if self.stat == "download_j":
            Thread(target=self.download, args=(self.JAVA_downloader,)).start()
        if self.stat == "update":
            Thread(target=self.download, args=(self.HC_updater,)).start()
        if self.stat == "launch":
            Thread(target=self.launch).start()
        if self.stat == "stop":
            if self.minecraft is not None:
                self.minecraft.kill()
        if self.stat == "close":
            Thread(target=self.close_console).start()

    def _download_listener(self, blocknum, bs, size):
        if self.speed_time == 0:
            self.speed_time = time.time()

        def division(x, y):
            if 0 not in (x, y):
                return x / y
            else:
                return 0

        self.speed_size += bs
        self.speed_timer += 1

        if self.speed_timer > 100:
            duration = time.time() - self.speed_time
            self.speed_time = 0
            self.speed = round(self.speed_size / (1024 * 1024 * duration) * 8, 2) if duration > 0 else 0
            self.speed_size = 0
            self.speed_timer = 0

        now_value = min(size, round(blocknum * bs))
        self.progress["value"] = now_value
        self.progress["maximum"] = size
        self.progress_title.configure(text=f"{LANG['main.interface.downloading']} {self.now_download}")
        self.progress_status.configure(text=f"{division(now_value, size) * 100:.2f}% {self.speed} Mbps")

    def _download_listener_t(self, blocknum, bs, size):
        if self.speed_time == 0:
            self.speed_time = time.time()

        def division(x, y):
            if 0 not in (x, y):
                return x / y
            else:
                return 0

        self.speed_size += bs
        self.speed_timer += 1

        if self.speed_timer > 500:
            duration = time.time() - self.speed_time
            self.speed_time = 0
            self.speed = round(self.speed_size / (1024 * 1024 * duration) * 8, 2) if duration > 0 else 0
            self.speed_size = 0
            self.speed_timer = 0

        self.progress["value"] += bs
        self.progress_title.configure(text=f"{LANG['main.interface.downloading']} {self.now_download}")
        self.progress_status.configure(
            text=f"{division(self.progress['value'], self.progress['maximum']) * 100:.2f}% {self.speed} Mbps")

    def HC_updater(self):
        URL = f"{ARCHIVE_HOST}/minecraft"
        self.progress["value"] = 0
        self.progress_title.configure(text=f"{LANG['main.download.start']}")
        size = url_size_getter(f"{URL}/optimization.zip") + url_size_getter(
            f"{URL}/shader.zip") + url_size_getter(f"{URL}/basic.zip") + url_size_getter(f"{URL}/addon.zip")
        self.progress["maximum"] = size
        basic_t = Thread(target=downloader, args=(f"{URL}/basic.zip",
                                                  f"{TEMP_PATH}\\basic.zip", self._download_listener_t))
        addon_t = Thread(target=downloader, args=(f"{URL}/addon.zip",
                                                  f"{TEMP_PATH}\\addon.zip", self._download_listener_t))
        opt_t = Thread(target=downloader, args=(f"{URL}/optimization.zip",
                                                f"{TEMP_PATH}\\optimization.zip", self._download_listener_t))
        shader_t = Thread(target=downloader, args=(f"{URL}/shader.zip",
                                                   f"{TEMP_PATH}\\shader.zip", self._download_listener_t))
        # self.now_download = "hdisc"
        # urllib.request.urlretrieve(f"{URL}/hdisc.zip", f"{TEMP_PATH}\\hdisc.zip", reporthook=self._download_listener)
        basic_t.start()
        addon_t.start()
        opt_t.start()
        shader_t.start()
        self.now_download = LANG["main.download.mod"]
        basic_t.join()
        addon_t.join()
        opt_t.join()
        shader_t.join()
        os.makedirs(f"{DATA_PATH}\\mods", exist_ok=True)
        path_h = f"{config_ini['CONFIG']['game_path']}\\versions\\HCollection"
        for mod in os.listdir(f"{DATA_PATH}\\mods"):
            if mod.endswith(".jar"):
                if os.path.exists(f"{path_h}\\mods\\{mod}"):
                    os.remove(f"{path_h}\\mods\\{mod}")

        self.extractor(f"{TEMP_PATH}\\basic.zip", f"{path_h}\\mods", mod=True)
        self.extractor(f"{TEMP_PATH}\\addon.zip", f"{path_h}\\mods", mod=True)
        self.extractor(f"{TEMP_PATH}\\optimization.zip", f"{path_h}\\mods", mod=True)
        self.extractor(f"{TEMP_PATH}\\shader.zip", f"{path_h}\\mods", mod=True)
        urllib.request.urlretrieve(f"{URL}/hversion.txt", f"{path_h}\\version.txt", reporthook=self._download_listener)

    def JAVA_downloader(self):
        URL = f"{ARCHIVE_HOST}/minecraft"
        if not os.path.exists(f"{RUN_PATH}\\java\\jdk-21"):
            self.now_download = "Java 21"
            urllib.request.urlretrieve(f"{URL}/jdk-21.zip", f"{TEMP_PATH}\\jdk-21.zip",
                                       reporthook=self._download_listener)
            os.makedirs(f"{RUN_PATH}\\java\\jdk-21", exist_ok=True)
            self.extractor(f"{TEMP_PATH}\\jdk-21.zip", f"{RUN_PATH}\\java\\jdk-21")

    def HC_downloader(self):
        URL = f"{ARCHIVE_HOST}/minecraft"
        if not os.path.exists(f"{RUN_PATH}\\java"):
            self.JAVA_downloader()

        # game content
        self.progress["value"] = 0
        self.progress_title.configure(text=f"{LANG['main.download.start']}")
        size = url_size_getter(f"{URL}/assets.zip") + url_size_getter(f"{URL}/libraries.zip") + url_size_getter(
            f"{URL}/HCollection.zip") + url_size_getter(f"{URL}/optimization.zip") + url_size_getter(
            f"{URL}/shader.zip") + url_size_getter(f"{URL}/basic.zip") + url_size_getter(f"{URL}/addon.zip")
        self.progress["maximum"] = size
        assets_t = Thread(target=downloader, args=(f"{URL}/assets.zip",
                                                   f"{TEMP_PATH}\\assets.zip", self._download_listener_t))
        lib_t = Thread(target=downloader, args=(f"{URL}/libraries.zip",
                                                f"{TEMP_PATH}\\libraries.zip", self._download_listener_t))
        main_t = Thread(target=downloader, args=(f"{URL}/HCollection.zip",
                                                 f"{TEMP_PATH}\\HCollection.zip", self._download_listener_t))
        basic_t = Thread(target=downloader, args=(f"{URL}/basic.zip",
                                                  f"{TEMP_PATH}\\basic.zip", self._download_listener_t))
        addon_t = Thread(target=downloader, args=(f"{URL}/addon.zip",
                                                  f"{TEMP_PATH}\\addon.zip", self._download_listener_t))
        opt_t = Thread(target=downloader, args=(f"{URL}/optimization.zip",
                                                f"{TEMP_PATH}\\optimization.zip", self._download_listener_t))
        shader_t = Thread(target=downloader, args=(f"{URL}/shader.zip",
                                                   f"{TEMP_PATH}\\shader.zip", self._download_listener_t))
        assets_t.start()
        lib_t.start()
        main_t.start()
        basic_t.start()
        addon_t.start()
        opt_t.start()
        shader_t.start()
        self.now_download = LANG["main.download.game_content"]
        assets_t.join()
        lib_t.join()
        main_t.join()
        basic_t.join()
        addon_t.join()
        opt_t.join()
        shader_t.join()

        # extract part
        os.makedirs(f"{config_ini['CONFIG']['game_path']}\\versions\\HCollection", exist_ok=True)
        os.makedirs(f"{config_ini['CONFIG']['game_path']}\\versions\\HCollection\\config", exist_ok=True)
        os.makedirs(f"{config_ini['CONFIG']['game_path']}\\versions\\HCollection\\mods", exist_ok=True)
        os.makedirs(f"{DATA_PATH}\\mods", exist_ok=True)

        path = f"{config_ini['CONFIG']['game_path']}"
        path_h = f"{config_ini['CONFIG']['game_path']}\\versions\\HCollection"

        self.extractor(f"{TEMP_PATH}\\assets.zip", f"{path}\\assets")
        self.extractor(f"{TEMP_PATH}\\libraries.zip", f"{path}\\libraries")
        self.extractor(f"{TEMP_PATH}\\HCollection.zip", path_h)

        self.extractor(f"{TEMP_PATH}\\basic.zip", f"{path_h}\\mods", mod=True)
        self.extractor(f"{TEMP_PATH}\\addon.zip", f"{path_h}\\mods", mod=True)
        self.extractor(f"{TEMP_PATH}\\optimization.zip", f"{path_h}\\mods", mod=True)
        self.extractor(f"{TEMP_PATH}\\shader.zip", f"{path_h}\\mods", mod=True)

        self.now_download = "config"
        urllib.request.urlretrieve(f"{URL}/createfood.json5", f"{path_h}\\config\\createfood.json5",
                                   reporthook=self._download_listener)
        self.now_download = "version"
        urllib.request.urlretrieve(f"{URL}/hversion.txt", f"{path_h}\\version.txt", reporthook=self._download_listener)
        # self.extractor(f"{TEMP_PATH}\\hdisc.zip", f"{path_h}\\mods", mod=True)

    def update_console(self, function_frame: OutputFrame):
        self.launch_btn.configure(style="bold.danger.TButton")
        self.console.console.destroy()
        self.console.console = ScrollText(master=self.console)
        self.console.console["state"] = "disabled"
        self.console.console.configure(wrap=WORD, background="#232323",
                                       inactiveselectbackground="#909090",
                                       foreground="#ffffff",
                                       selectbackground="#909090", selectforeground="#303030",
                                       insertbackground="#ffffff",
                                       highlightcolor="#ffffff", font=("consolas", 9))
        path = config_ini['CONFIG']['game_path'] + f"\\versions\\{self.server_select}\\logs"
        old_logs = get_logs(path)
        os.makedirs(path, exist_ok=True)
        open(f"{path}\\latest.log", "w").close()
        pywinstyles.set_opacity(self.console, value=1)
        self.stat = "stop"
        self.console.console.delete("1.0", "end")
        self.set_button()
        self.console.place(x=zoom(600 - 200 - 25), y=zoom(400 - 50 - 25), width=zoom(200), height=zoom(50))
        widget.move_to(self.console, x=0, y=0, width=zoom(600), height=zoom(400), fps=REFRESH_RATE)
        contents = []
        if self.minecraft is None:
            print('minecraft ended')
            return 0
        self.console.console.delete("1.0", "end")
        rest = []
        while self.minecraft.poll() is None:
            try:
                update_list, updated = self.check_con_update(contents)
                if updated:

                    index = 0
                    updated_list = []
                    for i in update_list:
                        updated_list.append(i)
                        if not self.minecraft.poll() is None:
                            break
                        if index > len(contents) - 1:
                            function_frame.addline(i)
                        elif contents[index] != i:
                            function_frame.addline(i)
                        index += 1
                        function_frame.console.cyview("end")

                    contents = updated_list
                    rest = []
                    if updated_list != update_list:
                        rest = update_list[len(updated_list):]

                    function_frame.console.cyview("end")
            except:
                pass
            time.sleep(0.05)

        new_logs = get_logs(path)
        debug('Minecraft ended', COLORS.ERROR, "LAUNCHER")
        self.launch_btn.configure(style="bold.primary.TButton")
        self.stat = "stopping"
        self.set_button()
        condition = True
        if new_logs != old_logs:
            condition = False

        name = f"{path}\\latest.log"
        with open(name) as l_f:
            log_content = l_f.read()
        if "Unreported exception thrown" in log_content:
            condition = False
        if condition:
            widget.move_to(self.console, x=zoom(600 - 200 - 25), y=zoom(400 - 50 - 25),
                           width=zoom(200), height=zoom(50), fps=REFRESH_RATE)
            time.sleep(0.5)
            widget.fade_out(self.console, 1, fps=REFRESH_RATE)
            time.sleep(1)
            self.console.place_forget()
            self.stat = "launch"
            self.minecraft = None
            self.set_button()
        else:
            with open(name) as l_f:
                log_content = l_f.readlines()
            rest = []
            start_add = False
            for line in log_content:
                if "Unreported exception thrown" in line:
                    start_add = True
                if start_add:
                    rest.append(line)
                    # print(line)
                    # print(contents)
            for i in rest:
                contents.append(i)
                function_frame.addline(i)
                function_frame.console.cyview("end")

            function_frame.console.cyview("end")
            self.stat = "close"
            self.minecraft = None
            self.set_button()

    def close_console(self):
        widget.move_to(self.console, x=zoom(600 - 200 - 25), y=zoom(400 - 50 - 25),
                       width=zoom(200), height=zoom(50), fps=REFRESH_RATE)
        time.sleep(0.5)
        widget.fade_out(self.console, 1, fps=REFRESH_RATE)
        time.sleep(1)
        self.console.place_forget()
        self.stat = "launch"
        self.minecraft = None
        self.set_button()

    def check_con_update(self, base_list: list):
        new_list = []
        name = config_ini['CONFIG']['game_path'] + f"\\versions\\{self.server_select}\\logs\\latest.log"
        # print(name)
        if not os.path.exists(name):
            return base_list, False
        new_list.insert(0, base_list)
        updated = False
        with open(name) as file:
            contents = file.readlines()

        if base_list != contents:
            new_list = contents
            updated = True

        return new_list, updated

    def extractor(self, src, dst, mod=False):
        def division(x, y):
            if 0 not in (x, y):
                return x / y
            else:
                return 0

        with zipfile.ZipFile(src, "r") as zip_ref:
            self.progress["value"] = 0
            self.progress["maximum"] = len(zip_ref.namelist())
            for z_file in zip_ref.namelist():
                zip_ref.extract(member=z_file, path=dst)
                self.progress["value"] += 1
                if mod:
                    shutil.copy(f"{dst}\\{z_file}", f"{DATA_PATH}\\mods")
                self.progress_title.configure(
                    text=f"{LANG['main.download.extract']} {os.path.basename(src)} ({self.progress['value']} / {self.progress['maximum']})")
                self.progress_status.configure(
                    text=f"{division(self.progress['value'], self.progress['maximum']) * 100:.2f}%")

    def download(self, function):
        self.is_download = True
        self.launch_btn.configure(text="")
        self.progressbar.place(x=zoom(600 - 25 - 200), y=zoom(400 - 25 - 50), width=zoom(200), height=zoom(50))
        widget.move_to(self.launch_btn, x=zoom(600 - 350 - 25), y=zoom(400 - 75 - 25),
                       width=zoom(350), height=zoom(75), fps=REFRESH_RATE)
        widget.move_to(self.progressbar, x=zoom(600 - 350 - 25), y=zoom(400 - 75 - 25),
                       width=zoom(350), height=zoom(75), fps=REFRESH_RATE)
        widget.fade_out(self.launch_btn, light=0.8, fps=REFRESH_RATE)

        function()
        self.launch_btn.place(x=zoom(600 - 25), y=zoom(400 - 50 - 25), width=zoom(0), height=zoom(50))
        widget.move_to(self.progressbar, x=zoom(600 - 25), y=zoom(400 - 75 - 25), width=0, height=zoom(75),
                       fps=REFRESH_RATE, after_functions=[self.progressbar.place_forget])
        time.sleep(0.5)
        pywinstyles.set_opacity(self.launch_btn, value=0.8)
        widget.move_to(self.launch_btn, x=zoom(600 - 25 - 200), y=zoom(400 - 25 - 50), width=zoom(200), height=zoom(50),
                       fps=REFRESH_RATE)

        time.sleep(1)
        self.progressbar.place_forget()
        self.launcher.update_list()
        self.get_server_state()

        self.is_download = False

    def launch(self):
        text = "Try to launch Minecraft using userdata (Name: {0}) (UUID: {1}) (Token: {2})".format(
            self.ms_account.name, self.ms_account.uuid, self.ms_account.token
        )
        debug(text, COLORS.PINK, "LAUNCHER")
        if "" in [self.ms_account.name, self.ms_account.uuid, self.ms_account.token]:
            # self.get_ms_info()
            debug("Login to Microsoft Account First!", COLORS.ERROR, "LAUNCHER")
        else:
            self.minecraft = self.launcher.launch(self.server_select, self.ms_account, 16 * 1024)
            Thread(target=self.update_console, args=(self.console,)).start()

    def migrate_setting(self):
        old_path = askdirectory(title=LANG["main.interface.migrate.title"])
        game_path = f"{config_ini['CONFIG']['game_path']}\\versions\\{self.server_select}"
        config_path = f"{old_path}\\config"
        if os.path.exists(config_path):
            for path, dirs, files in os.walk(config_path):
                for file_name in files:
                    if file_name != "createfood.json5":
                        new_path = f"{game_path}\\config{path.replace(config_path, '')}"
                        os.makedirs(new_path, exist_ok=True)
                        if os.path.exists(f"{new_path}\\{file_name}"):
                            os.remove(f"{new_path}\\{file_name}")
                        shutil.copy(f"{path}\\{file_name}", f"{new_path}")

        if os.path.exists(f"{old_path}\\options.txt"):
            shutil.copy(f"{old_path}\\options.txt", f"{game_path}")

    def get_ms_info(self):
        self.focus_set()
        if "" in [self.ms_account.name, self.ms_account.uuid, self.ms_account.token]:
            self.account_frame.destroy()
            self.is_alive = False
            self._master.change_view("microsoft_bind")

    def change_title(self, event=None):
        widget.label_print(self.title_label, self.server_select, during=0.5)

    def start_animation(self, event=None):
        time.sleep(0.5)
        self.change_title()
        self.set_button()
        self.is_pause = True
        Thread(target=self.background_loop).start()
        time.sleep(3)
        self.is_pause = False

    def close(self, event=None):
        self.is_alive = False
        self.account_frame.destroy()
        self._master.close()

    def set_button(self, event=None):
        if self.server_select == "Crossline":
            self.stat = "notopen"
        if self.stat == "close":
            self.launch_btn.configure(text=LANG["control.close"].upper())
        else:
            self.launch_btn.configure(text=LANG[f"main.control.{self.stat}"].upper())

    def background_loop(self):
        light = 0.5
        while self.is_alive:
            while True:
                img = random.choice(self.server_backgrounds[self.server_list.index(self.server_select)])
                if self.background_p == img:
                    continue
                self.background_p = img
                break
            if self.is_pause:
                light = light
                self.is_pause = False
            else:
                light = 0.5
            step = round(light / REFRESH_RATE, 4)
            period = 1 / REFRESH_RATE
            for f in range(REFRESH_RATE):
                if (not self.is_alive) or self.is_pause:
                    break
                timer = time.time()
                pywinstyles.set_opacity(self.background, value=light)
                light -= step
                light = max(light, 0)
                spend = time.time() - timer
                if spend < period:
                    time.sleep(period - spend)

            if self.is_pause:
                continue

            self.background.delete("all")
            self.background.create_image(0, 0, image=img, anchor="nw")

            step = round(0.5 / REFRESH_RATE, 4)
            period = 1 / REFRESH_RATE
            for f in range(REFRESH_RATE):
                if (not self.is_alive) or self.is_pause:
                    break
                timer = time.time()
                pywinstyles.set_opacity(self.background, value=light)
                light += step
                light = min(0.5, light)
                spend = time.time() - timer
                if spend < period:
                    time.sleep(period - spend)
            if self.is_pause:
                continue
            for i in range(50):
                if (not self.is_alive) or self.is_pause:
                    break
                time.sleep(0.1)

    def set_background_anmiate(self):
        self.is_pause = True

    def set_background(self):
        img = random.choice(self.server_backgrounds[self.server_list.index(self.server_select)])
        self.background_p = img
        self.background.delete("all")
        self.background.create_image(0, 0, image=img, anchor="nw")

    def connect_server(self):
        global Image_cache
        server = socket.socket()
        try:
            server.connect((SERVER_HOST, ACCOUNT_PORT))
        except Exception:
            error = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\Cross Mark.png")
            error_img = ImageTk.PhotoImage(error.resize((zoom(60), zoom(60))), master=self)
            Image_cache.append(error)
            Image_cache.append(error_img)
            # self.titleLabel.place(x=zoom(35), y=0, width=zoom(200), height=zoom(400))
            self._master.deiconify()
            msg = InfoWindow(self, title=LANG["server.connect.error"], message=LANG["server.connect.error_text"],
                             icon=f"{RUN_PATH}\\assets\\icon\\ico.ico",
                             bitmap=error_img, alert=True, buttonType=LANG["control.quit"],
                             buttonCommands=os._exit)
            msg.show()
            self.mainloop()
        return server

    def _sign_in_ms_thread(self):
        _socket = self.connect_server()
        start_time = time.time()
        _socket.sendall(f"get_ms{SEPARATOR}{GENERAL_AUTH}".encode())
        _socket.recv(BUFFER_SIZE)
        mail_add = self._master.account.email
        password = self._master.account.password

        content = NCE.encryption_key(f"{mail_add}{SEPARATOR}{covert_password(password)}", SALT)
        _socket.sendall(content.encode())

        state = _socket.recv(BUFFER_SIZE).decode()
        if state == "success_sign":
            _socket.sendall("copy".encode())
            content = _socket.recv(BUFFER_SIZE).decode()
            if content == "no_msaccount":
                return 1
            data = NCE.decryption_key(content, SALT)
            name, uid, token, r_token = data.split(SEPARATOR)

            end = time.time()

            if end - start_time < 0.75:
                time.sleep(0.75 - (end - start_time))

            self.ms_account.name = name
            self.ms_account.uuid = uid
            # self.ms_account.token = token
            self.ms_account.r_token = r_token
            new_login_data = minecraft_launcher_lib.microsoft_account.complete_refresh(
                client_id=CLIENT_ID, refresh_token=r_token, client_secret=None, redirect_uri=None)
            self.upload_ms_info(name,
                                uid,
                                new_login_data['access_token'],
                                new_login_data['refresh_token'])
            self.ms_account.token = new_login_data['access_token']
            self.ms_account.r_token = new_login_data['refresh_token']
            debug("Successfully Logged into Microsoft Account", COLORS.SUCCESS, "BACKGROUND")
            self.get_server_state()
        else:
            end = time.time()

            if end - start_time < 0.75:
                time.sleep(0.75 - (end - start_time))

    def upload_ms_info(self, name, uid, token, r_token):
        _socket = self.connect_server()
        _socket.sendall(f"modify_ms{SEPARATOR}{GENERAL_AUTH}".encode())
        _socket.recv(BUFFER_SIZE)
        mail_add = self._master.account.email
        password = self._master.account.password

        S = SEPARATOR

        message = f"{mail_add}{S}{covert_password(password)}{S}{name}{S}{uid}{S}{token}{S}{r_token}"

        content = NCE.encryption_key(message, SALT)
        _socket.sendall(content.encode())

        state = _socket.recv(BUFFER_SIZE).decode()
        if state == "success_sign":
            return 0

        else:
            return 1


# Microsoft bind
class MicrosoftBind(MainViewClass):

    def __init__(self, master: MainWindow):
        assert cefpython.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
        sys.excepthook = cefpython.ExceptHook
        settings = {}
        cefpython.Initialize(settings=settings, switches={'disable-gpu-compositing': None})
        cefpython.DpiAware.EnableHighDpiSupport()
        self._master = master
        self._master.add_view("microsoft_bind", self)
        MainViewClass.__init__(self, master)

        self.webPanel = MainFrame(self)

    def draw(self):
        width, height = self._master.winfo_width(), self._master.winfo_height()
        self._master.title(LANG["account.microsoft.title"])
        self._master.protocol("WM_DELETE_WINDOW", self.back_main)
        if ENABLE_WIN11_EFFECT:
            pywinstyles.apply_style(self._master, "dark")
        else:
            pywinstyles.apply_style(self._master, "dark")
        self.webPanel.place(x=zoom(0), y=zoom(0), width=zoom(800), height=zoom(600))
        self.place(x=zoom(400), y=zoom(300), width=0, height=0)
        _x, _y = get_middle_xy(self._master, zoom(800), zoom(600))
        widget.move_to(self._master, x=_x, y=_y, width=zoom(800), height=zoom(600), fps=REFRESH_RATE, is_windows=True)
        widget.move_to(self, x=0, y=0, width=zoom(800), height=zoom(600), fps=REFRESH_RATE)
        # darkWindow(self._master)
        # self.webPanel.show()
        self.login_to_microsoft()
        debug("MS Frame Drawn", COLORS.CYAN, "GUI")
        # self._master.appear()

    def back_main(self):
        self.webPanel.browser_frame.browser = None
        self._master.back_main()

    def redraw(self, event=None):
        self._master.redraw("microsoft_bind", viewType=MicrosoftBind)

    def login_to_microsoft(self):
        Thread(target=self._login_to_microsoft).start()

    def _login_to_microsoft(self):
        # Thread(target=launcher.login, args=(self.webPanel,)).start()
        time.sleep(1)
        data = launcher.login(self.webPanel)
        if data == 1:
            print("Unknown Error during login")
            error = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\Cross Mark.png")
            error_img = ImageTk.PhotoImage(error.resize((zoom(60), zoom(60))))
            Image_cache.append(error)
            Image_cache.append(error_img)
            msg = InfoWindow(self, title=LANG["control.error"], message=LANG["account.microsoft.signin_error"],
                             icon=f"{RUN_PATH}\\assets\\icon\\ico.ico",
                             bitmap=error_img, alert=True, buttonType=LANG["control.quit"],
                             buttonCommands=os._exit)
            msg.show()
        else:
            _content = f"{data['name']}\n{data['id']}\n{data['access_token']}\n{data['refresh_token']}"
            self.upload_ms_info(data['name'], data['id'], data['access_token'], data['refresh_token'])
            self._master.change_view("main_view")

    def connect_server(self):
        global Image_cache
        server = socket.socket()
        try:
            server.connect((SERVER_HOST, ACCOUNT_PORT))
        except Exception:
            error = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\Cross Mark.png")
            error_img = ImageTk.PhotoImage(error.resize((zoom(60), zoom(60))), master=self)
            Image_cache.append(error)
            Image_cache.append(error_img)
            # self.titleLabel.place(x=zoom(35), y=0, width=zoom(200), height=zoom(400))
            self._master.deiconify()
            msg = InfoWindow(self, title=LANG["server.connect.error"], message=LANG["server.connect.error_text"],
                             icon=f"{RUN_PATH}\\assets\\icon\\ico.ico",
                             bitmap=error_img, alert=True, buttonType=LANG["control.quit"],
                             buttonCommands=os._exit)
            msg.show()
            self.mainloop()
        return server

    def upload_ms_info(self, name, uid, token, r_token):
        _socket = self.connect_server()
        _socket.sendall(f"modify_ms{SEPARATOR}{GENERAL_AUTH}".encode())
        _socket.recv(BUFFER_SIZE)
        mail_add = self._master.account.email
        password = self._master.account.password

        S = SEPARATOR

        message = f"{mail_add}{S}{covert_password(password)}{S}{name}{S}{uid}{S}{token}{S}{r_token}"

        content = NCE.encryption_key(message, SALT)
        _socket.sendall(content.encode())

        state = _socket.recv(BUFFER_SIZE).decode()
        if state == "success_sign":
            return 0

        else:
            return 1


# account classes
class AccountView(MainViewClass):

    def __init__(self, master: MainWindow):
        global Image_cache
        self.email = ""
        self.password = ""
        self.username = ""
        self.uid = ""
        self.avatar = f"{DATA_PATH}\\avatar.png"
        self.account = User("", "", "", "", "")
        self.run_main = False
        self.immediately_sign_in = False
        self._master = master
        self._master.add_view("account", self)
        Frame.__init__(self)

        self.icon = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\account_title.png").resize((zoom(170), zoom(221)))
        self.title_img = ImageTk.PhotoImage(self.icon, master=self)

        Image_cache.append(self.icon)
        Image_cache.append(self.title_img)

        self.titleLabel = Label(self, image=self.title_img)

        self.socket = self.connect_server()

        self.remember = BooleanVar(self)
        self.remember.set(False)

        if user_ini["USER"]["remember"] == "true":
            self.immediately_sign_in = True
            self.remember.set(True)

        if self.remember.get():
            self.mail_add = user_ini["USER"]["mail"]
            self.user_pass = user_ini["USER"]["password"]
        else:
            self.mail_add = ""
            self.user_pass = ""

        self.sign_in = SignInFrame(self)
        self.sign_up = SignUpFrame(self)
        self.verify = MailVerifyFrame(self)
        self.create_acc = PasswordWriteFrame(self)
        self.title_animate = LoadingFrame(self, loc=(zoom(65), zoom(65), zoom(170), zoom(170)))

    def draw(self):
        windowInit(self._master, 600, 400, False, LANG["account.title"],
                   f"{RUN_PATH}\\assets\\icon\\ico.ico")
        middle(self._master, zoom(600), zoom(400))
        self._master.style.theme_use("windows_dark")
        self._master.protocol("WM_DELETE_WINDOW", self.closeWIN)
        self._master.minsize(width=zoom(600), height=zoom(400))

        self.set_appwindow()
        darkWindow(self._master)
        self.place(x=0, y=0, width=zoom(600), height=zoom(400))

        self.titleLabel.place(x=zoom(65), y=zoom(65), width=zoom(170), height=zoom(221))
        self.sign_in.place(x=zoom(295), y=zoom(50), width=zoom(260), height=zoom(300))
        self.title_animate = LoadingFrame(self, loc=(zoom(65), zoom(65), zoom(170), zoom(170)))
        self.title_animate.run()

        self._master.appear()
        if self.immediately_sign_in:
            def _IS():
                time.sleep(1)
                self.sign_in.sign_in()

            Thread(target=_IS).start()

        debug("Account Frame Drawn", COLORS.CYAN, "GUI")

    def withdraw(self, after="f"):
        func = self.place_forget if after == "f" else self.destroy
        widget.withdraw(self, fps=REFRESH_RATE, after_funtions=[func], direction="s")

    def get_avatar(self):
        thread = Thread(target=self._get_avatar)
        return thread

    def _get_avatar(self):
        self.socket = self.connect_server()
        self.socket.sendall(f"get_avatar{SEPARATOR}{GENERAL_AUTH}".encode())
        self.socket.recv(BUFFER_SIZE)
        self.socket.sendall(NCE.encryption_key(self.email, SALT).encode())

        with open(f"{DATA_PATH}\\avatar.png", "wb") as file:
            while True:
                bytes_read = self.socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                file.write(bytes_read)

        self.avatar = f"{DATA_PATH}\\avatar.png"
        self.socket.close()
        self.make_user()

    def make_user(self):
        self.account = User(self.email, self.uid, self.username, self.password, self.avatar)
        self._master.account = User(self.email, self.uid, self.username, self.password, self.avatar)

    def connect_server(self):
        global Image_cache
        server = socket.socket()
        try:
            server.connect((SERVER_HOST, ACCOUNT_PORT))
        except Exception:
            error = Image.open(f"{RUN_PATH}\\assets\\bitmaps\\Cross Mark.png")
            error_img = ImageTk.PhotoImage(error.resize((zoom(60), zoom(60))), master=self)
            Image_cache.append(error)
            Image_cache.append(error_img)
            self.titleLabel.place(x=zoom(35), y=0, width=zoom(200), height=zoom(400))
            self._master.deiconify()
            msg = InfoWindow(self, title=LANG["server.connect.error"], message=LANG["server.connect.error_text"],
                             icon=f"{RUN_PATH}\\assets\\icon\\ico.ico",
                             bitmap=error_img, alert=True, buttonType=LANG["control.quit"],
                             buttonCommands=os._exit)
            msg.show()
            self.mainloop()
        return server

    def get_focus(self, event=None):
        self.focus_set()

    def set_appwindow(self):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(self.winfo_id())
        _style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        _style = _style & ~WS_EX_TOOLWINDOW
        _style = _style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, _style)
        self._master.wm_withdraw()
        self.after(10, lambda: self._master.wm_deiconify())

    def closeWIN(self):
        global user_ini
        self.title_animate.stop()
        user_ini["USER"]["mail"] = self.sign_in.mail_entry.get()
        user_ini["USER"]["password"] = self.sign_in.pass_entry.get()
        user_ini["USER"]["remember"] = "true" if self.remember.get() else "false"
        with open(USER_CONFIG, "w") as file:
            user_ini.write(file)
        self.focus_set()
        self._master.close()
        # time.sleep(3)

    def signed_in(self, event=None):
        debug("Signed in", COLORS.CYAN, "GUI-ACC")
        global user_ini
        # self._master.withdraw()
        user_ini["USER"]["mail"] = self.sign_in.mail_entry.get()
        user_ini["USER"]["password"] = self.sign_in.pass_entry.get()
        user_ini["USER"]["remember"] = "true" if self.remember.get() else "false"
        with open(USER_CONFIG, "w") as file:
            user_ini.write(file)
        Thread(target=self._get_avatar_and_continue).start()
        Thread(target=self.back_main).start()

    def back_main(self):
        while not self.run_main:
            time.sleep(0.1)

        self.title_animate.stop()

        print("avatar path", self._master.account.avatar)
        debug("Login closed", COLORS.CYAN, "GUI-ACC")
        self._master.back_main()

    def _get_avatar_and_continue(self):
        debug("Getting avatar", COLORS.CYAN, "GUI-ACC")
        self._get_avatar()  # fetch the image (blocking, but in background)
        self.run_main = True


    def switch_sign_in(self, event=None):
        self.socket.close()
        self.socket = self.connect_server()
        widget.withdraw(self.sign_up, delay=0.25, fps=REFRESH_RATE, direction="ns")
        widget.withdraw(self.verify, delay=0.25, fps=REFRESH_RATE, direction="ns")
        widget.withdraw(self.create_acc, delay=0.25, fps=REFRESH_RATE, direction="ns")
        widget.move_to(self.sign_in, x=zoom(295), y=zoom(50), width=zoom(260), height=zoom(300),
                       delay=0.25, fps=REFRESH_RATE, start_delay=0.25, parameters=["appear", "ns"])

    def switch_sign_up(self, event=None):
        widget.withdraw(self.sign_in, delay=0.25, fps=REFRESH_RATE, direction="ns")
        widget.move_to(self.sign_up, x=zoom(295), y=zoom(50), width=zoom(260), height=zoom(300),
                       delay=0.25, fps=REFRESH_RATE, start_delay=0.25, parameters=["appear", "ns"])

    def switch_verify(self, event=None):
        widget.withdraw(self.sign_up, delay=0.25, fps=REFRESH_RATE, direction="ns")
        self.verify.code_entry.delete("0", "end")
        widget.move_to(self.verify, x=zoom(295), y=zoom(50), width=zoom(260), height=zoom(300),
                       delay=0.25, fps=REFRESH_RATE, start_delay=0.25, parameters=["appear", "ns"])

    def switch_create_account(self, event=None):
        widget.withdraw(self.verify, delay=0.25, fps=REFRESH_RATE, direction="ns")
        self.create_acc.pass_entry.delete("0", "end")
        self.create_acc.check_entry.delete("0", "end")
        self.create_acc.name_entry.delete("0", "end")
        widget.move_to(self.create_acc, x=zoom(295), y=zoom(50), width=zoom(260), height=zoom(300),
                       delay=0.25, fps=REFRESH_RATE, start_delay=0.25, parameters=["appear", "ns"])


class SignInFrame(Frame):

    def __init__(self, master: AccountView):
        Frame.__init__(self, master=master)
        self._master = master

        self.Style = Style()
        self.Style.configure("TButton", font=("Arial", "10"))
        self.Style.configure("w.info.Link.TButton", font=("Arial", "10"),
                             anchor="w", relief="flat", focusthickness=0)
        self.Style.configure("e.info.Link.TButton", font=("Arial", "10"),
                             anchor="e", relief="flat", focusthickness=0)
        self.Style.configure("bold.secondary.TButton", font=("Arial", "15", "bold"))
        self.Style.configure("error.danger.TLabel", font=("Arial", "10", "bold"))
        self.Style.configure("secondary.TEntry", foreground="#cccccc")
        self.Style.configure("TLabel", font=("Arial", "10"))
        self.Style.configure("success.TCheckbutton", font=("Arial", "10"))

        self.mail_entry = Entry(self, style="secondary.TEntry", font=("Arial", "10"))
        self.mail_tip = Label(self, text=LANG["account.signin.mail_tip"])
        self.pass_entry = Entry(self, show="•", style="secondary.TEntry", font=("Arial", "10"))
        self.pass_tip = Label(self, text=LANG["account.signin.password_tip"])
        self.remember_btn = Checkbutton(self, text=LANG["account.signin.remember_me"], variable=self._master.remember,
                                        style="success.TCheckbutton")
        self.error_tip = Label(self, text=LANG["account.signin.content_error"], style="error.danger.TLabel")

        self.forget_btn = Button(self, text=LANG["account.forget_pass"],
                                 command=self.forgot_password, style="w.info.Link.TButton", takefocus=False)
        self.sign_up_btn = Button(self, text=LANG["account.signup"],
                                  command=self._master.switch_sign_up, style="e.info.Link.TButton", takefocus=False)
        self.sign_in_btn = Button(self, text=LANG["account.signin"].upper(),
                                  command=self.sign_in, style="bold.secondary.TButton", takefocus=False)

        self.mail_entry.insert("end", self._master.mail_add)
        self.pass_entry.insert("end", self._master.user_pass)

        self.mail_entry.bind("<Return>", self.switch_to_pass)
        self.pass_entry.bind("<Return>", self.sign_in)
        self.mail_entry.bind("<FocusIn>", self.remove_error_tip)
        self.pass_entry.bind("<FocusIn>", self.remove_error_tip)
        self.sign_in_btn.bind("<Enter>", self.btn_zoom_in)
        self.sign_in_btn.bind("<Leave>", self.btn_zoom_out)
        self.bind("<1>", self.get_focus)

        self.bind("<Configure>", self.refresh_all)

    def get_focus(self, event=None):
        self.focus_set()

    def remove_error_tip(self, event=None):
        self.error_tip.place_forget()

    def switch_to_pass(self, event=None):
        self.pass_entry.focus_set()

    def forgot_password(self, event=None):
        self.focus_set()

    def btn_zoom_in(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(200),
                     "width": width, "height": zoom(50)}
        widget.zoom(self.sign_in_btn, ratio=1.02, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def btn_zoom_out(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(200),
                     "width": width, "height": zoom(50)}
        widget.unzoom(self.sign_in_btn, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def sign_in(self, event=None):
        self.focus_set()
        mail_add = self.mail_entry.get()
        password = self.pass_entry.get()

        if (not mail_add) or (not password):
            return 1

        widget.withdraw(self._master.sign_in, delay=0.2, direction="ns", fps=REFRESH_RATE)
        widget.move_to(self._master.titleLabel, x=zoom(215), y=zoom(65), width=zoom(170), height=zoom(221),
                       delay=0.25, fps=REFRESH_RATE, start_delay=0.2)
        widget.move_to(self._master.title_animate, x=zoom(215), y=zoom(65), width=zoom(170), height=zoom(170),
                       delay=0.25, fps=REFRESH_RATE, start_delay=0.2)
        Thread(target=self._sign_in_thread, args=[mail_add, password]).start()

    def _sign_in_thread(self, mail_add, password):
        start_time = time.time()
        self._master.socket.sendall(f"sign_in{SEPARATOR}{GENERAL_AUTH}".encode())
        self._master.socket.recv(BUFFER_SIZE)

        content = NCE.encryption_key(f"{mail_add}{SEPARATOR}{covert_password(password)}", SALT)
        self._master.socket.sendall(content.encode())

        state = self._master.socket.recv(BUFFER_SIZE).decode()
        if state == "success_sign":
            self._master.socket.sendall("copy".encode())
            content = self._master.socket.recv(BUFFER_SIZE).decode()
            email, uid, username = NCE.decryption_key(content, SALT).split(SEPARATOR)

            end = time.time()

            if end - start_time < 0.75:
                time.sleep(0.75 - (end - start_time))

            self._master.email = email
            self._master.uid = uid
            self._master.username = username
            self._master.password = password
            self._master.signed_in()

        else:
            end = time.time()

            if end - start_time < 0.75:
                time.sleep(0.75 - (end - start_time))
            if state == "pass_error":
                self.pass_error()
            widget.move_to(self._master.titleLabel, x=zoom(65), y=zoom(65), width=zoom(170), height=zoom(221),
                           delay=0.25, fps=REFRESH_RATE)
            widget.move_to(self._master.title_animate, x=zoom(65), y=zoom(65), width=zoom(170), height=zoom(170),
                           delay=0.25, fps=REFRESH_RATE, after_functions=[self._master.switch_sign_in])

    def pass_error(self, event=None):
        width = self.winfo_width() - zoom(10)
        print("passerror")
        self.error_tip.place(x=zoom(5), y=zoom(130), width=width, height=zoom(50))

    def refresh_all(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.mail_tip.place(x=zoom(5), y=0, width=width, height=zoom(25))
        self.mail_entry.place(x=zoom(5), y=zoom(25), width=width, height=zoom(30))
        self.pass_tip.place(x=zoom(5), y=zoom(75), width=width, height=zoom(25))
        self.pass_entry.place(x=zoom(5), y=zoom(100), width=width, height=zoom(30))
        self.remember_btn.place(x=zoom(5), y=zoom(130), width=width, height=zoom(30))

        self.forget_btn.place(x=zoom(-3), y=zoom(175), width=width - zoom(75), height=zoom(25))
        self.sign_up_btn.place(x=width - zoom(65), y=zoom(175), width=zoom(75), height=zoom(25))

        self.sign_in_btn.place(x=zoom(5), y=zoom(200), width=width, height=zoom(50))


class SignUpFrame(Frame):

    def __init__(self, master: AccountView):
        Frame.__init__(self, master=master)
        self._master = master

        self.Style = Style()
        self.Style.configure("TButton", font=("Arial", "10"))
        self.Style.configure("w.info.Link.TButton", font=("Arial", "10"), anchor="w")
        self.Style.configure("e.info.Link.TButton", font=("Arial", "10"), anchor="e")
        self.Style.configure("TButton", font=("Arial", "15", "bold"))
        self.Style.configure("TEntry")
        self.Style.configure("TLabel", font=("Arial", "10"))
        self.Style.configure("error.danger.TLabel", font=("Arial", "10", "bold"))

        self.mail_entry = Entry(self, bootstyle="secondary", font=("Arial", "10"))
        self.mail_tip = Label(self, text=LANG["account.signup.mail_tip"])
        self.code_entry = Entry(self, bootstyle="secondary", font=("Arial", "10"))
        self.code_tip = Label(self, text=LANG["account.signup.invite_code"])

        self.error_tip = Label(self, text=LANG["account.signup.invalid_code"], style="error.danger.TLabel")

        self.sign_in_btn = Button(self, text=LANG["account.signin"],
                                  command=self.back, style="e.info.Link.TButton", takefocus=False)
        self.sign_up_btn = Button(self, text=LANG["account.signup.mail_verify"].upper(),
                                  command=self.verify_mail, bootstyle="secondary", takefocus=False)

        self.mail_entry.bind("<Return>", self.verify_mail)
        self.bind("<1>", self.get_focus)
        self.mail_entry.bind("<FocusIn>", self.remove_error)
        self.code_entry.bind("<FocusIn>", self.remove_error)
        self.sign_up_btn.bind("<Enter>", self.btn_zoom_in)
        self.sign_up_btn.bind("<Leave>", self.btn_zoom_out)

        self.bind("<Configure>", self.refresh_all)

    def back(self, event=None):
        self._master.socket.sendall(NCE.encryption_key("exit", SALT).encode())
        self._master.switch_sign_in()

    def get_focus(self, event=None):
        self.focus_set()

    def remove_error(self, event=None):
        self.error_tip.place_forget()

    def btn_zoom_in(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(200),
                     "width": width, "height": zoom(50)}
        widget.zoom(self.sign_up_btn, ratio=1.02, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def btn_zoom_out(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(200),
                     "width": width, "height": zoom(50)}
        widget.unzoom(self.sign_up_btn, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def mail_exists(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.error_tip.configure(text=LANG["account.signup.account_exists"])
        self.error_tip.place(x=zoom(5), y=zoom(130), width=width, height=zoom(25))

    def code_error(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.error_tip.configure(text=LANG["account.signup.invalid_code"])
        self.error_tip.place(x=zoom(5), y=zoom(130), width=width, height=zoom(25))

    def verify_mail(self, event=None):
        self.focus_set()
        self._master.socket.sendall(f"sign_up{SEPARATOR}{GENERAL_AUTH}".encode())
        self._master.socket.recv(BUFFER_SIZE)
        self._master.socket.sendall(NCE.encryption_key(f"{self.mail_entry.get()}{SEPARATOR}{self.code_entry.get()}",
                                                       SALT).encode())
        state = self._master.socket.recv(BUFFER_SIZE).decode()
        if state != "pass":
            if state == "mail_exists":
                self.mail_exists()
                return 1
            else:
                self.code_error()
                return 1
        self._master.switch_verify()

    def refresh_all(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.mail_tip.place(x=zoom(5), y=0, width=width, height=zoom(25))
        self.mail_entry.place(x=zoom(5), y=zoom(25), width=width, height=zoom(30))

        self.code_tip.place(x=zoom(5), y=zoom(75), width=width, height=zoom(25))
        self.code_entry.place(x=zoom(5), y=zoom(100), width=width, height=zoom(30))

        self.sign_in_btn.place(x=width - zoom(65), y=zoom(175), width=zoom(75), height=zoom(25))

        self.sign_up_btn.place(x=zoom(5), y=zoom(200), width=width, height=zoom(50))


class MailVerifyFrame(Frame):

    def __init__(self, master: AccountView):
        Frame.__init__(self, master=master)
        self._master = master

        self.Style = Style()
        self.Style.configure("TButton", font=("Arial", "10"))
        self.Style.configure("w.info.Link.TButton", font=("Arial", "10"), anchor="w")
        self.Style.configure("e.info.Link.TButton", font=("Arial", "10"), anchor="e")
        self.Style.configure("TButton", font=("Arial", "15", "bold"))
        self.Style.configure("TEntry")
        self.Style.configure("TLabel", font=("Arial", "10"))

        self.code_entry = Entry(self, bootstyle="secondary", font=("Arial", "10"))
        self.code_tip = Label(self, text=LANG["account.signup.mail_verify.verify_code"])

        self.prev = Button(self, text=f'<{LANG["control.previous"]}',
                           command=self.back, style="w.info.Link.TButton", takefocus=False)

        self.sign_up_btn = Button(self, text=LANG["account.signup.mail_verify.verify"].upper(),
                                  command=self.verify_mail, bootstyle="secondary", takefocus=False)

        self.code_entry.bind("<Return>", self.verify_mail)
        self.sign_up_btn.bind("<Enter>", self.btn_zoom_in)
        self.sign_up_btn.bind("<Leave>", self.btn_zoom_out)
        self.bind("<1>", self.get_focus)

        self.bind("<Configure>", self.refresh_all)

    def back(self, event=None):
        self._master.socket.sendall(NCE.encryption_key("exit", SALT).encode())
        self._master.switch_sign_in()

    def get_focus(self, event=None):
        self.focus_set()
        self._master.socket.sendall(f"sign_up{SEPARATOR}{GENERAL_AUTH}".encode())

    def btn_zoom_in(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(200),
                     "width": width, "height": zoom(50)}
        widget.zoom(self.sign_up_btn, ratio=1.02, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def btn_zoom_out(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(200),
                     "width": width, "height": zoom(50)}
        widget.unzoom(self.sign_up_btn, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def verify_mail(self, event=None):
        self.focus_set()
        verify_code = self.code_entry.get().upper()
        while True:
            self._master.socket.sendall(NCE.encryption_key(verify_code, SALT).encode())
            answer = self._master.socket.recv(BUFFER_SIZE).decode()
            if answer == "correct":
                break

        self._master.switch_create_account()

    def refresh_all(self, event=None):
        width = self.winfo_width() - zoom(10)

        self.code_tip.place(x=zoom(5), y=zoom(75), width=width, height=zoom(25))
        self.code_entry.place(x=zoom(5), y=zoom(100), width=width, height=zoom(30))

        self.sign_up_btn.place(x=zoom(5), y=zoom(200), width=width, height=zoom(50))
        self.prev.place(x=zoom(-3), y=zoom(175), width=width - zoom(75), height=zoom(25))


class PasswordWriteFrame(Frame):

    def __init__(self, master: AccountView):
        global Image_cache
        Frame.__init__(self, master=master)
        self._master = master

        self.Style = Style()
        self.Style.configure("TButton", font=("Arial", "10"))
        self.Style.configure("w.info.Link.TButton", font=("Arial", "10"), anchor="w")
        self.Style.configure("e.info.Link.TButton", font=("Arial", "10"), anchor="e")
        self.Style.configure("TButton", font=("Arial", "15", "bold"))
        self.Style.configure("TEntry", font=("Arial", "15"))
        self.Style.configure("TLabel", font=("Arial", "10"))
        self.Style.configure("danger.TLabel", font=("Arial", "10", "bold"))

        self.name_entry = Entry(self, bootstyle="secondary")
        self.name_tip = Label(self, text=LANG["account.signup.account_name"])
        self.pass_entry = Entry(self, bootstyle="secondary", show="•")
        self.pass_tip = Label(self, text=LANG["account.signup.password"])
        self.check_entry = Entry(self, bootstyle="secondary", show="•")
        self.check_tip = Label(self, text=LANG["account.signup.check_password"])
        self.unavailable_tip = Label(self, text=LANG["account.signup.unavailable_name"], style="danger.TLabel")

        self.prev = Button(self, text=f'<{LANG["control.previous"]}',
                           command=self.back, style="w.info.Link.TButton")

        self.create_btn = Button(self, text=LANG["account.signup.create_account"].upper(),
                                 command=self.create_account, bootstyle="secondary")

        self.bind("<1>", self.get_focus)
        self.check_entry.bind("<FocusIn>", self.forget_tip)
        self.pass_entry.bind("<FocusIn>", self.forget_tip)
        self.name_entry.bind("<FocusIn>", self.forget_tip)
        self.create_btn.bind("<Enter>", self.btn_zoom_in)
        self.create_btn.bind("<Leave>", self.btn_zoom_out)

        self.bind("<Configure>", self.refresh_all)

        success_pic = Image.open(f"{RUN_PATH}\\assets\\icon\\success.png").resize((zoom(60), zoom(60)))
        self.success_pic = ImageTk.PhotoImage(success_pic, master=self)
        Image_cache.append(success_pic)
        Image_cache.append(self.success_pic)

    def back(self, event=None):
        self._master.socket.sendall(NCE.encryption_key("exit", SALT).encode())
        self._master.switch_sign_in()

    def get_focus(self, event=None):
        self.focus_set()

    def btn_zoom_in(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(250),
                     "width": width, "height": zoom(50)}
        widget.zoom(self.create_btn, ratio=1.02, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def btn_zoom_out(self, event=None):
        width = self.winfo_width() - zoom(10)
        originals = {"x": zoom(5), "y": zoom(250),
                     "width": width, "height": zoom(50)}
        widget.unzoom(self.create_btn, originals=originals, delay=0.05, fps=REFRESH_RATE)

    def forget_tip(self, event=None):
        self.unavailable_tip.place_forget()

    def unavailable(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.unavailable_tip.configure(text=LANG["account.signup.unavailable_name"])
        self.unavailable_tip.place(x=zoom(5), y=zoom(200), width=width, height=zoom(25))

    def different(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.unavailable_tip.configure(text=LANG["account.signup.not_same_password"])
        self.unavailable_tip.place(x=zoom(5), y=zoom(200), width=width, height=zoom(25))

    def too_long(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.unavailable_tip.configure(text=LANG["account.signup.too_long_content"])
        self.unavailable_tip.place(x=zoom(5), y=zoom(200), width=width, height=zoom(25))

    def registration_failed(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.unavailable_tip.configure(text=LANG["account.signup.registration_failed"])
        self.unavailable_tip.place(x=zoom(5), y=zoom(200), width=width, height=zoom(25))

    def create_account(self, event=None):
        self.focus_set()
        acc_name = self.name_entry.get()
        password = self.pass_entry.get()
        checked = self.check_entry.get()
        if (not acc_name) or (not password) or (not checked):
            return 1
        for i in UN_AVAILABLE_CHAR:
            if i in acc_name:
                self.unavailable()
                return 1

        if password != checked:
            self.different()
            return 1

        if len(password) >= 24 or len(acc_name) >= 24:
            self.too_long()
            return 1

        try:
            acc_name.encode()

        except ValueError:
            self.unavailable()
            return 1

        password_hash = covert_password(password)

        message = NCE.encryption_key(f"{acc_name}{SEPARATOR}{password_hash}", SALT)
        self._master.socket.sendall(message.encode())
        response = self._master.socket.recv(BUFFER_SIZE).decode()
        if response == "success":
            msg = InfoWindow(self, title=LANG["account.signup.registration_succeed"],
                             message=LANG["account.signup.registration_succeed_text"],
                             icon=f"{RUN_PATH}\\assets\\icon\\ico.ico",
                             bitmap=self.success_pic, alert=True,
                             buttonType=[f'{LANG["control.quit"]} : success'],
                             buttonCommands=[self._master.switch_sign_in])
            msg.show()
        elif response == "name_exists":
            self.unavailable()
        else:
            self.registration_failed()

    def refresh_all(self, event=None):
        width = self.winfo_width() - zoom(10)
        self.name_tip.place(x=zoom(5), y=0, width=width, height=zoom(25))
        self.name_entry.place(x=zoom(5), y=zoom(25), width=width, height=zoom(30))

        self.pass_tip.place(x=zoom(5), y=zoom(75), width=width, height=zoom(25))
        self.pass_entry.place(x=zoom(5), y=zoom(100), width=width, height=zoom(30))

        self.check_tip.place(x=zoom(5), y=zoom(150), width=width, height=zoom(25))
        self.check_entry.place(x=zoom(5), y=zoom(175), width=width, height=zoom(30))

        self.create_btn.place(x=zoom(5), y=zoom(250), width=width, height=zoom(50))
        self.prev.place(x=zoom(-3), y=zoom(225), width=width - zoom(65), height=zoom(25))


class LoadingFrame(Frame):

    def __init__(self, master, image=f"{RUN_PATH}\\assets\\bitmaps\\HCloud-loading.gif", loc=(0, 0, 100, 100)):
        global Image_cache
        Frame.__init__(self, master=master)
        self.animate = StoppableThread()
        self.stopped = False

        self.label = Label(self)

        self.x, self.y, self.width, self.height = loc

        self.im = Image.open(image)
        self._iter = ImageSequence.Iterator(self.im)
        self.img = []
        Image_cache.append(self.im)
        Image_cache.append(self._iter)
        Thread(target=self.refresh_all).start()

    def refresh_all(self, event=None):
        global Image_cache
        width = self.width
        height = self.height

        self.img = []
        for i in self._iter:
            try:
                img = ImageTk.PhotoImage(i.resize((width, height)))
                self.img.append(img)
                Image_cache.append(img)
            except RuntimeError:
                pass
        Image_cache.append(self.img)

    def stop(self):
        self.stopped = True

    def run(self, event=None):
        self.animate = Thread(target=self._run)
        self.animate.start()

    def _run(self):
        self.label.place(x=0, y=0, width=self.width, height=self.height)
        self.place(x=self.x, y=self.y, width=self.width, height=self.height)
        times = 1
        firstStart = time.time()
        width = self.winfo_width()
        height = self.winfo_height()
        while not self.stopped:
            for x in self.img:
                if self.stopped:
                    break
                start = time.time()
                # canvas.create_rectangle(0, 0, int(400 * zoom), int(300 * zoom), fill='white', outline='white')
                if self.stopped:
                    break
                try:
                    self.label.configure(image=x)
                except:
                    pass
                if self.stopped:
                    break
                end = time.time()
                passed = round(end - start, 3)
                totalTime = end - firstStart
                if passed <= 0.042 and times >= totalTime / 0.042:
                    time.sleep(0.042 - passed)
                times += 1


class ServerSelection(Toplevel):

    def __init__(self, master, server_variable: StringVar):
        Toplevel.__init__(self, master=master)
        self.withdraw()
        self._master = master

        windowInit(self, 450, 300, False, LANG["software.name"],
                   f"{RUN_PATH}\\assets\\icon\\ico.ico")
        middle(self, zoom(450), zoom(300))
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.minsize(width=zoom(450), height=zoom(300))
        darkWindow(self)

        self.Style = Style()
        self.Style.configure("solid.secondary.TButton", font=("Arial", "10"))
        self.Style.configure("name.light.Link.TButton", font=("Arial", "10", "bold"),
                             anchor="center", relief="flat", focusthickness=0)
        self.Style.configure("ip.light.Link.TButton", font=("Arial", "10", "bold"),
                             anchor="w", relief="flat", focusthickness=0)
        self.Style.configure("secondary.TEntry", foreground="#cccccc")
        self.Style.configure("TLabel", font=("Arial", "10"))

        self.communities = Frame(self)
        self.personal = Frame(self)
        self.direct = Entry(self, style="secondary.TEntry", font=("Arial", "10"))
        self.direct_btn = Button(self, style="solid.secondary.TButton", text=LANG["control.ok"])

    def closeWin(self, event=None):
        self.grab_release()
        self.destroy()

    def show(self, event=None):
        self.config(width=zoom(450), height=zoom(300))
        middle(self, zoom(450), zoom(300))
        self.deiconify()
        self.focus_set()
        self.grab_set()


# functional functions
def get_server_name(address):
    _socket = socket.socket()
    _socket.connect((SERVER_HOST, SERVER_G_PORT))
    content = f"{GENERAL_AUTH}{SEPARATOR}get_server_details{SEPARATOR}{address}"
    _socket.sendall(content.encode())
    details = _socket.recv(BUFFER_SIZE).decode()
    name = details[0]
    return name


def get_logs(path):
    files = os.listdir(path)
    logs = []
    for _file in files:
        if _file.endswith(".log.gz"):
            logs.append(_file)

    return logs


def get_online_servers():
    _socket = socket.socket()
    _socket.connect((SERVER_HOST, SERVER_G_PORT))
    content = f"{GENERAL_AUTH}{SEPARATOR}get_online_servers{SEPARATOR}none"
    _socket.sendall(content.encode())
    contents = b""
    _socket.recv(BUFFER_SIZE)

    while True:
        data = _socket.recv(BUFFER_SIZE)
        if not data:
            break
        contents += data

    contents = contents.decode()
    servers = contents.split(SEPARATOR)

    return servers


def safeMakeDirs(dirs):
    with LOCK:
        if not os.path.exists(dirs):
            os.makedirs(dirs)


def get_file_type(file_name: str):
    return "." + file_name.split(".")[-1]


def initSize(size, split=False):
    final = 0
    unit = "bytes"
    if size < 1024:
        final = f"{size}bytes" if not split else f"{size}"
        unit = "bytes"
    elif 1024 <= size < 1024 * 1024:
        final = f"{round(size / 1024, 2)}KB" if not split else f"{round(size / 1024, 2)}"
        unit = "KB"
    elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
        final = f"{round(size / 1024 / 1024, 2)}MB" if not split else f"{round(size / 1024 / 1024, 2)}"
        unit = "MB"
    elif 1024 * 1024 * 1024 <= size < 1024 * 1024 * 1024 * 1024:
        final = f"{round(size / 1024 / 1024 / 1024, 2)}GB" if not split else f"{round(size / 1024 / 1024 / 1024, 2)}"
        unit = "GB"
    if not split:
        return final
    else:
        return final, unit


def covertSize(size, unit: str):
    unit = unit.lower()

    if unit == "kb":
        return size / 1024
    elif unit == "mb":
        return size / 1024 / 1024
    elif unit == "gb":
        return size / 1024 / 1024
    else:
        return size


def initTime(second):
    final = 0
    if second < 60:
        final = f"{round(second, 3)}s"
    elif 60 <= second < 60 * 60:
        final = f"{round(second / 60, 2)}min"
    elif 60 * 60 <= second < 60 * 60 * 60:
        final = f"{round(second / 60 / 60, 2)}hour"
    return final


def safeDeleteDirs(dirs):
    def delete():
        nonlocal dirs
        total_dir = []
        for path, dirs, files in os.walk(dirs):
            total_dir.append(f"{path}")
        total_dir.reverse()
        for i in total_dir:
            try:
                os.rmdir(i)
            except Exception:
                pass

    Thread(target=delete).start()


def windowInit(master, width, height, canResize: bool, title: str, icon: str):
    master.config(width=zoom(width), height=zoom(height))
    if not canResize:
        master.resizable(width=False, height=False)
    master.title(title)
    master.iconbitmap(icon)


def middle(master, width=None, height=None):
    winX = width
    winY = height
    maxX = winapi.GetSystemMetrics(0)
    maxY = winapi.GetSystemMetrics(1)
    if winX is None:
        winX = master.winfo_width()
        winY = master.winfo_height()
    x = maxX // 2 - winX // 2
    y = maxY // 2 - winY // 2
    master.geometry(f"+{int(x)}+{int(y)}")


def get_middle_xy(master, width=None, height=None):
    winX = width
    winY = height
    maxX = winapi.GetSystemMetrics(0)
    maxY = winapi.GetSystemMetrics(1)
    if winX is None:
        winX = master.winfo_width()
        winY = master.winfo_height()
    x = maxX // 2 - winX // 2
    y = maxY // 2 - winY // 2
    return x, y


def noFun(*event):
    return event


def darkWindow(win):
    win.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ctypes.windll.user32.GetParent
    hwnd = get_parent(win.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ctypes.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ctypes.byref(value),
                         ctypes.sizeof(value))


def is_windows():
    if os.name == "nt":
        return True
    return False


def deleteUntil(string, key, side='right'):
    """Delete string until key"""
    try:
        strings = list(string)
        now = ""
        if side == "right":
            while True:
                now = strings[-1]
                if now == key:
                    break
                else:
                    del strings[-1]
        if side == "left":
            while True:
                now = strings[0]
                if now == key:
                    break
                else:
                    del strings[0]
        final = ''
        for i in strings:
            final += i
    except Exception:
        final = string
    return final


def open_file(file_path):
    def start(file_path):
        path = os.path.dirname(file_path)
        os.chdir(path)
        os.system(f'"{file_path}"')

    Thread(target=start, args=[file_path]).start()


def downloader(url, file_path, hook=None):
    urllib.request.urlretrieve(url, file_path, reporthook=hook)


def url_size_getter(url):
    try:
        req = urllib.request.Request(url, method='HEAD')
        response = urllib.request.urlopen(req)
        file_size = response.headers.get("Content-Length")
        if file_size is not None:
            return int(file_size)
        else:
            return None
    except urllib.error.URLError as e:
        print(f"Error accessing URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def covert_password(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT.encode(), 371400).hex()


def zoom(data):
    return int(round(data * ZOOM, 0))


def get_color(master, style_name):
    bootstyle = (master.master.bootstyle, "button")
    ttkstyle = Bootstyle.ttkstyle_name(string="-".join(bootstyle))
    value = master.tk.call(
        "ttk::style", "lookup", ttkstyle, "-%s" % style_name, None, None
    )
    return value


def get_time_format():
    open_path = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\International")
    date_f = winreg.QueryValueEx(open_path, "sShortDate")[0]
    time_f = winreg.QueryValueEx(open_path, "sShortTime")[0]
    itime = winreg.QueryValueEx(open_path, "iTime")[0]

    return date_f, time_f, itime


def hex_to_rgb(color: str):
    """Convert hexadecimal color to rgb color value

    Parameters:

        color (str):
            A hexadecimal color value

    Returns:

        tuple[int, int, int]:
            An rgb color value.
    """
    if len(color) == 4:
        # 3 digit hexadecimal colors
        r = int(color[1], 16)
        g = int(color[2], 16)
        b = int(color[3], 16)
    else:
        # 6 digit hexadecimal colors
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:], 16)
    return r, g, b


def self_init():
    global config_ini, SERVER_HOST
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    if not os.path.exists(SYS_PATH):
        os.makedirs(SYS_PATH)
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.exists(USER_CONFIG):
        with open(USER_CONFIG, "w") as file:
            user_ini.read(USER_CONFIG)
            user_ini["USER"] = {
                "mail": "",
                "password": "",
                "remember": "true"
            }
            user_ini.write(file)
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as file:
            config_ini.read(CONFIG_PATH)
            config_ini["CONFIG"] = {
                "path": "this pc",
                "local_view": "grid",
                "net_view": "grid",
                "current_view": "local",
                "game_path": f"{BASIC_PATH}\\games"
            }
            config_ini.write(file)

    try:
        config_ini.read(CONFIG_PATH)
        test = [config_ini["CONFIG"]["path"],
                config_ini["CONFIG"]["local_view"],
                config_ini["CONFIG"]["current_view"],
                config_ini["CONFIG"]["game_path"],
                config_ini["CONFIG"]["net_view"]]
    except Exception:
        with open(CONFIG_PATH, "w") as file:
            config_ini.read(CONFIG_PATH)
            config_ini["CONFIG"] = {
                "path": "this pc",
                "local_view": "grid",
                "net_view": "grid",
                "current_view": "local",
                "game_path": f"{BASIC_PATH}\\games"
            }
            config_ini.write(file)

    try:
        user_ini.read(USER_CONFIG)
        test = [user_ini["USER"]["mail"],
                user_ini["USER"]["password"],
                user_ini["USER"]["remember"]]
        test2 = [user_ini["CONFIG"]["server"]]
    except Exception:
        with open(USER_CONFIG, "w") as file:
            user_ini.read(USER_CONFIG)
            user_ini["USER"] = {
                "mail": "",
                "password": "",
                "remember": "false"
            }
            user_ini["CONFIG"] = {
                "server": "archives.hlhtstudios.com"
            }
            user_ini.write(file)
    SERVER_HOST = user_ini["CONFIG"]["server"]


if __name__ == "__main__":
    self_init()
    root = MainWindow()
    account = AccountView(root)
    root.change_view("account")
    root.mainloop()
