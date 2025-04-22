import basic.gui as gui
# import pywinstyles


def main():
    gui.self_init()
    root = gui.MainWindow()
    account = gui.AccountView(root)
    ms_account = gui.MicrosoftBind(root)
    main_view = gui.MainAppView(root)
    # pywinstyles.apply_style(root, "acrylic")
    # pywinstyles.set_opacity(root, value=0.5)
    # pywinstyles.set_opacity(account, value=0.5)
    root.change_view("account")
    root.mainloop()


if __name__ == "__main__":
    main()
