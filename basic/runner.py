import basic.gui as gui
from basic.constants import debug, COLORS, LOGGER, create_log_time
from basic.updater import check_version


def main():
    try:
        debug(f"[+] Started", COLORS.CYAN, "MAIN")
        gui.self_init()
        debug("Initialize completed", COLORS.CYAN, "MAIN")
        root = gui.MainWindow()
        debug("Mainwindow Generated", COLORS.CYAN, "MAIN")
        account = gui.AccountView(root)
        debug("AccountWindow Generated", COLORS.CYAN, "MAIN")
        if check_version():
            account.need_update = True
        ms_account = gui.MicrosoftBind(root)
        debug("MS Generated", COLORS.CYAN, "MAIN")
        main_view = gui.MainAppView(root)
        debug("MainFrame Generated", COLORS.CYAN, "MAIN")
        root.change_view("account")
        debug("Main process successfully launched", COLORS.SUCCESS, "MAIN")
        root.mainloop()
    except Exception as e:
        exc_cont = f"{create_log_time()}"
        LOGGER.critical(str(e), exc_cont + " [MAIN_START]")
        debug(str(e), COLORS.ERROR, "MAIN_START")