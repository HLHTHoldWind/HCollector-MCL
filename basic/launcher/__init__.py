import subprocess
import time
import certifi
import minecraft_launcher_lib
import os
from basic.constants import *
from basic.gui.browser import MainFrame


def login(widget: MainFrame):
    login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(CLIENT_ID,
                                                                                                     REDIRECT_URL)
    while True:
        try:
            widget.get_browser().LoadUrl(login_url)
            break
        except:
            continue

    print(certifi.where())
    while True:
        if "chrome-error://chromewebdata/" in widget.get_browser().GetUrl():
            break
        # print(widget.get_browser().GetUrl(), widget.browser_frame.url)
        time.sleep(0.1)
    # print(widget.browser_frame.url)
    try:
        auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(widget.browser_frame.url, state)
    except AssertionError:
        print("States do not match!")
        return 1
    except KeyError:
        print("Url not valid")
        return 1

    login_data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, None, REDIRECT_URL, auth_code,
                                                                         code_verifier)

    widget.get_browser().CloseBrowser(True)
    return login_data


class Version:

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.available = False


class Launcher:

    def __init__(self, versions):
        self.path = CONFIG["CONFIG"]["game_path"]

        self.available_versions = {}
        for version in versions:
            self.available_versions[version] = Version(version, 0)

        if os.path.exists(os.path.join(self.path, "versions")):
            for version in self.available_versions.keys():
                if os.path.exists(os.path.join(self.path, "versions",
                                               self.available_versions[version].name, "version.txt")):
                    self.available_versions[version].available = True
                    with open(os.path.join(self.path, "versions",
                                           self.available_versions[version].name, "version.txt")) as v_file:
                        v = int(v_file.read())

                    self.available_versions[version].version = v

    def update_list(self):
        if os.path.exists(os.path.join(self.path, "versions")):
            for version in self.available_versions.keys():
                if os.path.exists(os.path.join(self.path, "versions",
                                               self.available_versions[version].name, "version.txt")):
                    self.available_versions[version].available = True
                    with open(os.path.join(self.path, "versions",
                                           self.available_versions[version].name, "version.txt")) as v_file:
                        v = int(v_file.read())

                    self.available_versions[version].version = v

    def install(self, version, name, fabric=False, forge=False, fabric_v="0", callbacker={}):
        if fabric:
            minecraft_launcher_lib.fabric.install_fabric(version, self.path,
                                                         loader_version=fabric_v, callback=callbacker)
        elif forge:
            forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
            minecraft_launcher_lib.forge.install_forge_version(forge_version, self.path, callback=callbacker)
        else:
            minecraft_launcher_lib.install.install_minecraft_version(version, self.path, callback=callbacker)

        os.rename(os.path.join(self.path, "versions", version), os.path.join(self.path, "versions", name))
        path = str(os.path.join(self.path, "versions", name))

        os.rename(os.path.join(path, f"{version}.jar"), os.path.join(path, f"{name}.jar"))
        os.rename(os.path.join(path, f"{version}.json"), os.path.join(path, f"{name}.json"))
        with open(os.path.join(path, "version.txt"), "w") as v_file:
            v_file.write("0")

    def launch(self, name, ms_user: MS_User, ram: 8096):
        options = {
            "username": ms_user.name,
            "uuid": ms_user.uuid,
            "token": ms_user.token,
            "jvmArguments": ["-Xmx" + str(ram) + "M", "-Xms1024M"],
            "gameDirectory": f"{self.path}\\versions\\{name}",
            "executablePath": f"{RUN_PATH}\\java\\jdk-21\\bin\\javaw.exe",
            "server": SERVER_LIST[name].split(":")[0],
            "port": SERVER_LIST[name].split(":")[1],
            "quickPlayMultiplayer": SERVER_LIST[name]
        }
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(name, self.path, options)
        minecraft = subprocess.Popen(minecraft_command, cwd=f"{self.path}\\versions\\{name}")

        return minecraft
