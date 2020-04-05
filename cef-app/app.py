import webview


def load_css(window):
    window.load_css(open('css/style.css').read())


if __name__ == '__main__':
    window = webview.create_window('Load CSS Example', html=open('cube.html').read())
    webview.start(load_css, window, debug=True)
