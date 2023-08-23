from ctypes import windll, byref, sizeof, c_int

def dark_title_bar(window):
    window.update()

    HWND = windll.user32.GetParent(window.winfo_id()) # the window we want to change

    # These attributes are for windows 11
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TITLE_COLOR = 36

    # color should be in hex order: 0x00bbggrr
    COLOR_1 = 0x00000000
    COLOR_2 = 0x00FFFFFF

    windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_CAPTION_COLOR, byref(c_int(COLOR_1)), sizeof(c_int))
    windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_TITLE_COLOR, byref(c_int(COLOR_2)), sizeof(c_int))