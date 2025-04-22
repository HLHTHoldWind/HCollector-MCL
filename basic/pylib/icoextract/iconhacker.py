import winreg
from ctypes import Array, byref, c_char, memset, sizeof
from ctypes import c_int, c_void_p, POINTER
from ctypes.wintypes import *
from enum import Enum
import ctypes
import sys
import os
import numpy as np
from PIL import Image
import PIL
from typing import Tuple
import io
import basic.pylib.icoextract as icoextract
import tkinter
import tkinter.filedialog as filedialog


HKEY_CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
IMAGE_TYPE = [".png", ".jpg", ".jpge", ".bmp", ".gif", ".ico"]


class IconHacker:

    def __init__(self, basic_path, basic_folder, _os=os):
        self.basic_path = basic_path
        self.basic_folder = basic_folder
        self._os = os

    def get_file_icon(self, path, try_img=False):
        if self._os.path.isfile(path):
            img = self._get_icon(path, try_img)

        else:
            img = Image.open(self.basic_folder)

        ratio = 256 / img.width if img.width > img.height else 256 / img.height

        return img.resize((int(round(ratio * img.width)), int(round(ratio * img.height))))

    def get_file_icon_type(self, typename):
        img = self._get_icon_type(typename)

        ratio = 256 / img.width if img.width > img.height else 256 / img.height

        return img.resize((int(round(ratio * img.width)), int(round(ratio * img.height))))

    def get_type_expression(self, path):
        if "." not in path:
            return "File"

        file_type = get_file_type(path)
        content = ""
        try:
            open_path = winreg.OpenKey(HKEY_CLASSES_ROOT, file_type)
            open_key = winreg.QueryValue(open_path, None)
        except (FileNotFoundError, OSError):
            content = f"{file_type.lstrip('.').upper()} File"
            return content
        if open_key == "":
            content = f"{file_type.lstrip('.').upper()} File"
            return content

        try:
            open_path = winreg.OpenKey(HKEY_CLASSES_ROOT, open_key)
            content = str(winreg.QueryValue(open_path, None))

        except:
            content = f"{file_type.lstrip('.').upper()} File"
            return content

        return content

    def _get_icon(self, path, try_img):
        if "." not in path:
            img = Image.open(self.basic_path)
            return img
        file_type = get_file_type(path)
        if (file_type in IMAGE_TYPE) and try_img:
            try:
                img = Image.open(path).convert("RGBA")
                return img
            except PIL.UnidentifiedImageError:
                img = Image.open(self.basic_path)
                return img

        try:
            open_path = winreg.OpenKey(HKEY_CLASSES_ROOT, file_type)
            open_key = winreg.QueryValue(open_path, None)
        except (FileNotFoundError, OSError):
            img = Image.open(self.basic_path)
            return img

        if open_key == "":
            img = Image.open(self.basic_path)
            return img

        try:
            icon_path = winreg.OpenKey(HKEY_CLASSES_ROOT, open_key)
            default_icon = winreg.OpenKey(icon_path, "DefaultIcon")
            icon_key = winreg.QueryValue(default_icon, None)

            img_path, img_index = icon_key.split(",")
            img_path = img_path.strip("\" ")
            img_index = int(img_index.strip("\" "))
            img = get_icon_img(img_path, img_index)

        except:

            try:
                icon_path = winreg.OpenKey(HKEY_CLASSES_ROOT, open_key)
                default_icon = winreg.OpenKey(icon_path, "shell")
                default_icon = winreg.OpenKey(default_icon, "open")
                default_icon = winreg.OpenKey(default_icon, "command")
                icon_key = winreg.QueryValue(default_icon, None)

                img_path = ""
                string_list = icon_key.split(" ")[0:-1]
                for i in string_list:
                    img_path += i + " "

                img_path = img_path.strip("\" ")

                img_index = 0
                img = get_icon_img(img_path, img_index)

            except:
                img = Image.open(self.basic_path)
                return img

        return img

    def _get_icon_type(self, typename):
        file_type = typename

        try:
            open_path = winreg.OpenKey(HKEY_CLASSES_ROOT, file_type)
            open_key = winreg.QueryValue(open_path, None)
        except (FileNotFoundError, OSError):
            img = Image.open(self.basic_path)
            return img

        if open_key == "":
            img = Image.open(self.basic_path)
            return img

        try:
            icon_path = winreg.OpenKey(HKEY_CLASSES_ROOT, open_key)
            default_icon = winreg.OpenKey(icon_path, "DefaultIcon")
            icon_key = winreg.QueryValue(default_icon, None)

            img_path, img_index = icon_key.split(",")
            img_path = img_path.strip("\" ")
            img_index = int(img_index.strip("\" "))
            img = get_icon_img(img_path, img_index)

        except:

            try:
                icon_path = winreg.OpenKey(HKEY_CLASSES_ROOT, open_key)
                default_icon = winreg.OpenKey(icon_path, "shell")
                default_icon = winreg.OpenKey(default_icon, "open")
                default_icon = winreg.OpenKey(default_icon, "command")
                icon_key = winreg.QueryValue(default_icon, None)

                img_path = ""
                string_list = icon_key.split(" ")[0:-1]
                for i in string_list:
                    img_path += i + " "

                img_path = img_path.strip("\" ")

                img_index = 0
                img = get_icon_img(img_path, img_index)

            except:
                img = Image.open(self.basic_path)
                return img

        return img


def get_file_type(file_name: str):
    return "." + file_name.split(".")[-1].lower()


def get_icon_img(path, pointer):
    icon = icoextract.IconExtractor(path)
    length = icon.get_length(pointer)

    img = Image.open(io.BytesIO(icon.get_iconb(pointer, length, biggest=True))).convert("RGBA")

    return img


def test():
    root = tkinter.Tk()
    root.withdraw()
    basic_file = "C:\\Users\\Hold Wind\\PycharmProjects\\HGit\\client\\assets\\bitmaps\\file.png"
    basic_folder = "C:\\Users\\Hold Wind\\PycharmProjects\\HGit\\client\\assets\\bitmaps\\Folder.png"
    hacker = IconHacker(basic_file, basic_folder)

    path = filedialog.askopenfilename()
    img = hacker.get_file_icon(path)
    img.show()


if __name__ == '__main__':
    test()
