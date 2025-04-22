import basic.gui as gui
from basic.constants import debug, COLORS
# import pywinstyles


def main():
    debug(f"[+] Started", COLORS.CYAN, "MAIN")
    gui.self_init()
    debug("Initialize completed", COLORS.CYAN, "MAIN")
    root = gui.MainWindow()
    debug("Mainwindow Generated", COLORS.CYAN, "MAIN")
    account = gui.AccountView(root)
    debug("Mainwindow Generated", COLORS.CYAN, "MAIN")
    ms_account = gui.MicrosoftBind(root)
    debug("MS Generated", COLORS.CYAN, "MAIN")
    main_view = gui.MainAppView(root)
    debug("MainFrame Generated", COLORS.CYAN, "MAIN")
    # pywinstyles.apply_style(root, "acrylic")
    # pywinstyles.set_opacity(root, value=0.5)
    # pywinstyles.set_opacity(account, value=0.5)
    root.change_view("account")
    debug("Change to Login frame", COLORS.CYAN, "MAIN")
    debug("Main process successfully launched", COLORS.SUCCESS, "MAIN")
    root.mainloop()


if __name__ == "__main__":
    main()
