import time
import ctypes
import locale
import logging
import os
import configparser
import json
import platform
import re
import psutil
from basic import NCE

MAIN_VERSION = 124

WORK_PATH = RUN_PATH = os.getcwd()
USER_PATH = os.path.expanduser('~')
CONFIG = config_ini = configparser.ConfigParser()
"Server constants"
SERVER_HOST = "qwq.hlhtstudios.com"
ARCHIVE_HOST = "http://archives.hlhtstudios.com:3399"
SERVER_PORT = 105 * 50 + 3714
ACCOUNT_PORT = 7812
SERVER_G_PORT = 13714
BUFFER_SIZE = 8192
SEPARATOR = "<SEPARATOR>"
TOTAL_RAM = psutil.virtual_memory().total

CLIENT_ID = "4d436560-a8c2-46b7-80ba-a1de93445e40"
REDIRECT_URL = "http://127.0.0.1/"

"Other constants"

user_ini = configparser.ConfigParser()
CONFIG_PATH = f"{USER_PATH}\\AppData\\Local\\HLHT\\HCollector\\config\\config.ini"
DATA_PATH = f"{USER_PATH}\\AppData\\Local\\HLHT\\HCollector\\sta"
SYS_PATH = f"{USER_PATH}\\AppData\\Local\\HLHT\\HCollector\\system"
BASIC_PATH = f"{USER_PATH}\\AppData\\Local\\HLHT\\HCollector"
USER_CONFIG = f"{DATA_PATH}\\user.sta"
USER_CONFIG_MS = f"{DATA_PATH}\\user_ms.sta"
TEMP_PATH = f"{USER_PATH}\\AppData\\Local\\Temp"
UN_AVAILABLE_CHAR = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
GENERAL_AUTH = "f5b4851d5acc5ab1b11f9646c3802a7b1cc85be8551d4f3ee4bbec2218e89dcd"
SALT = NCE.encryption_key("HLHT Studios", "3714")
ACRYLIC = False

log_name = time.time()
os.makedirs("logs", exist_ok=True)
log_file_path = f'{RUN_PATH}\\logs\\log_{str(log_name).replace(".", "_")}.log'
LOGGER = logging.getLogger("[HCollector]")
LOGGER.propagate = False
LOGGER.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_file_path, mode='w')
fh.setLevel(logging.DEBUG)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(name)s [%(levelname)s]: %(message)s ')
fh.setFormatter(formatter)

# Add the handler to the logger
LOGGER.addHandler(fh)

SERVER_LIST = {"HCollection": "qwq.hlhtstudios.com:37140",
               "Crossline": "qwq.hlhtstudios.com:19132"}


C_START = int("4E00", base=16)
C_END = int("9FFF", base=16)
B_START = int("3105", base=16)
B_END = int("3129", base=16)
J1_START = int("3000", base=16)
J1_END = int("30FF", base=16)
J2_START = int("FF00", base=16)
J2_END = int("FFEF", base=16)
P_START = int("FF00", base=16)
P_END = int("FFEF", base=16)
R_START = int("0400", base=16)
R_END = int("04FF", base=16)

C_LIST = []
J_LIST = []
P_LIST = []
R_LIST = []
for char in range(B_START, B_END + 1):
    C_LIST.append(chr(char))

for char in range(C_START, C_END + 1):
    C_LIST.append(chr(char))

for char in range(J1_START, J1_END + 1):
    J_LIST.append(chr(char))

for char in range(J2_START, J2_END + 1):
    J_LIST.append(chr(char))

for char in range(R_START, R_END + 1):
    R_LIST.append(chr(char))


def create_log_time():
    timestamp = time.localtime(time.time())
    time_y = str(timestamp.tm_year)
    time_M = str(timestamp.tm_mon)
    time_d = str(timestamp.tm_mday)
    time_h = str(timestamp.tm_hour).rjust(2, '0')
    time_m = str(timestamp.tm_min).rjust(2, '0')
    time_s = str(timestamp.tm_sec).rjust(2, '0')
    date_text = f"{time_y}/{time_M}/{time_d}"
    time_text = f"{time_h}:{time_m}:{time_s}"
    return f"[{date_text} {time_text}]"


class Color:

    def __init__(self, color, name, code):
        self.color = color
        self.name = name
        self.color_code = code


class COLORS:
    CYAN = Color('[96m', "INFO", "#15c0cb")
    PINK = Color('[95m', "INFO", "#e4007f")
    BLUE = Color('[94m', "INFO", "#00a0e9")
    GREEN = INFO = SUCCESS = Color('[92m', "INFO", "#4add43")
    YELLOW = WARNING = Color('[93m', "WARNING", "#ffff00")
    YELLOW2 = WARN = Color('[93m', "WARN", "#ee9f01")
    RED = ERROR = Color('[91m', "ERROR", "#cf4e44")
    LIGHT_GRAY = Color('[37m', "COMMAND", "#c8c3bc")
    NONE = Color('[0m', "INFO", "#ffffff")
    BOLD = Color('[1m', "INFO", "#fffffe")
    UNDERLINE = Color('[4m', "INFO", "#fffffd")
    LIGHT_BLUE = Color('[4m', "INFO", "#a0c3fb")
    LIGHT_GREEN = Color('[4m', "INFO", "#41ff41")
    LIGHT_YELLOW = Color('[4m', "INFO", "#ffdf94")
    colors = [CYAN, PINK, BLUE, GREEN, YELLOW, RED, LIGHT_GRAY,
              NONE, BOLD, UNDERLINE, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, YELLOW2]


# other classes
class User:

    def __init__(self, email, uid, name, password, avatar):
        self.email = email
        self.uid = uid
        self.name = name
        self.password = password
        self.avatar = avatar


class MS_User:

    def __init__(self, name, uuid, token, r_token):
        self.name = name
        self.uuid = uuid
        self.token = token
        self.r_token = r_token
        self.state = False


if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.GetUserDefaultUILanguage()
    default_lang = locale.windows_locale[kernel32.GetUserDefaultUILanguage()]

else:
    default_lang = locale.getdefaultlocale()[0]

language_lib = []

for file in os.listdir(f"{WORK_PATH}\\languages"):
    if file.endswith(".json"):
        language_lib.append(os.path.basename(file).replace(".json", "").lower())

if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.GetUserDefaultUILanguage()
    default_lang = locale.windows_locale[kernel32.GetUserDefaultUILanguage()]

else:
    default_lang = locale.getdefaultlocale()[0]

LANG_DICT = {}

for lang_file in os.listdir(f"{WORK_PATH}\\languages"):
    if lang_file.endswith(".json"):
        with open(f"{WORK_PATH}\\languages\\{lang_file}", 'rb') as file:
            # print(file.read())
            content = json.load(file)
            lang_code = lang_file.lower().replace(".json", "")
            LANG_DICT[content["default.fullname"]] = f"{lang_code}"

TEMP_PATH = f"{USER_PATH}\\AppData\\Local\\Temp"
LOCAL_PATH = f"{USER_PATH}\\AppData\\Local\\HLHT\\KANKI"
DEFAULT_URL = "translate.google.com"

LANGUAGE_CODES = {"english": "en", "japanese": "ja", "chinese": "zh-cn",
                  "schinese": "zh-cn", "tchinese": "zh-tw", "latin": "la",
                  "italian": "it", "french": "fr", "korean": "ko", "esperanto": "eo",
                  "russian": "ru", "turkish": "tr"}


def load_lang():
    while True:
        try:

            CONFIG.read(CONFIG_PATH)

            if os.path.exists("languages\\" + CONFIG["CONFIG"]["lang"].lower() + ".json"):
                with open("languages\\" + CONFIG["CONFIG"]["lang"].lower() + ".json", "rb") as _file:
                    _LANG = json.load(_file)
            else:
                with open("languages\\en_us.json", "rb") as _file:
                    _LANG = json.load(_file)
            return _LANG

        except KeyError as e:
            init_config()
            continue


def get_windows_version():
    platform_info = platform.platform()
    if "Windows" not in platform_info:
        return 0

    if "Windows-10" in platform_info:
        version_match = re.search(r"Windows-10-(\d+\.\d+\.\d+)-", platform_info)
        if version_match:
            build_number = int(version_match.group(1).split(".")[-1])
            if build_number >= 22000:
                return 11
            else:
                return 10
    else:
        version_match = re.search(r"Windows-(\d+)\.(\d+)\.(\d+)", platform_info)
        if version_match:
            major, minor, build = map(int, version_match.groups())
            if major == 10 and build >= 22000:
                return 11
            elif major == 10:
                return 10

    return 0


ENABLE_WIN11_EFFECT = True if get_windows_version() >= 11 else False


def init_config():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH, exist_ok=True)
    if not os.path.exists(LOCAL_PATH):
        os.makedirs(LOCAL_PATH, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        if TOTAL_RAM / (1024 ** 3) <= 8:
            ram = 4096
        elif TOTAL_RAM / (1024 ** 3) <= 16:
            ram = 12288
        else:
            ram = 16384
        with open(CONFIG_PATH, "w") as file:
            config_ini.read(CONFIG_PATH)
            config_ini["CONFIG"] = {
                "path": "this pc",
                "lang": default_lang,
                "local_view": "grid",
                "net_view": "grid",
                "current_view": "local",
                "game_path": f"{BASIC_PATH}\\games",
                "ram": f"{ram}",
            }
            config_ini.write(file)
    CONFIG.read(CONFIG_PATH)


def debug(text, style=COLORS.NONE, host="TEST"):
    timestamp = time.localtime(time.time())
    time_y = str(timestamp.tm_year)
    time_M = str(timestamp.tm_mon)
    time_d = str(timestamp.tm_mday)
    time_h = str(timestamp.tm_hour).rjust(2, '0')
    time_m = str(timestamp.tm_min).rjust(2, '0')
    time_s = str(timestamp.tm_sec).rjust(2, '0')
    date_text = f"{time_y}/{time_M}/{time_d}"
    time_text = f"{time_h}:{time_m}:{time_s}"
    print(f"{style.color}[{date_text} {time_text}] [{host}|{style.name}] {text}{COLORS.NONE.color}")
    if style == COLORS.ERROR:
        LOGGER.error(f"[{date_text} {time_text}] [{host}|{style.name}] {text}{COLORS.NONE.color}")
    elif style == COLORS.WARN:
        LOGGER.warning(f"[{date_text} {time_text}] [{host}|{style.name}] {text}{COLORS.NONE.color}")
    elif style == COLORS.INFO:
        LOGGER.info(f"[{date_text} {time_text}] [{host}|{style.name}] {text}{COLORS.NONE.color}")
    elif style == COLORS.SUCCESS:
        LOGGER.info(f"[{date_text} {time_text}] [{host}|{style.name}] {text}{COLORS.NONE.color}")
    else:
        LOGGER.debug(f"[{date_text} {time_text}] [{host}|{style.name}] {text}{COLORS.NONE.color}")


def test_config():
    try:
        config_ini.read(CONFIG_PATH)
        test = [config_ini["CONFIG"]["path"],
                config_ini["CONFIG"]["local_view"],
                config_ini["CONFIG"]["current_view"],
                config_ini["CONFIG"]["game_path"],
                config_ini["CONFIG"]["ram"],
                config_ini["CONFIG"]["net_view"]]

        if not os.path.exists(config_ini["CONFIG"]["game_path"]):
            os.makedirs(config_ini["CONFIG"]["game_path"], exist_ok=True)

        if int(config_ini["CONFIG"]["ram"]) > TOTAL_RAM / (1024 ** 2):
            if TOTAL_RAM / (1024 ** 3) <= 8:
                ram = 4096
            elif TOTAL_RAM / (1024 ** 3) <= 16:
                ram = 12288
            else:
                ram = 16384
            config_ini["CONFIG"]["ram"] = str(ram)
            with open(CONFIG_PATH, "w") as _cf:
                config_ini.write(_cf)
    except (KeyError, FileNotFoundError):
        init_config()

LANG = load_lang()

test_config()
