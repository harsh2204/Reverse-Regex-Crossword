# TODO: 
# [x] Send relevant data from back-end to front-end js.
# [ ] Get script files to load localy, either using the initialization parameters or running an internal server serving those files.
#       Have to implement either a resource handler or copy from https://github.com/rentouch/cefpython_old/blob/master/cefpython/cef3/linux/binaries_32bit/wxpython-response.py.
#       ^(Keep in mind that this is not compatible on all OS'es)
#  OR   Run a fast server locally, before starting the app to load the js files.
#  OR   Make internet connection a requirement for the app.
# 
# [ ] Use that data to construct a N^M grid of puzzle
# [ ] Add ability to change letters
# [ ] Add letters look at camera always

from cefpython3 import cefpython as cef
from string import ascii_uppercase
import numpy as np
import json

def main():
    cef.Initialize()
    browser = cef.CreateBrowserSync(url=cef.GetDataUrl(open('cube.html', 'r').read()),
                                    window_title="Javascript Bindings",
                                    settings={
                                        'universal_access_from_file_urls_allowed':  True,
                                        'file_access_from_file_urls_allowed':       True
                                    })
                                    
    browser.SetClientHandler(LoadHandler())
    
    bindings = cef.JavascriptBindings()
    bindings.SetFunction("get_puzzle", get_puzzle)
    # bindings.SetFunction("py_callback", py_callback)
    browser.SetJavascriptBindings(bindings)

    cef.MessageLoop()
    del browser
    cef.Shutdown()


def get_puzzle():
    l = np.array(list(ascii_uppercase) + list(ascii_uppercase)[::-1])
    l = np.reshape(l[:27], (3,3,3))
    return l.tolist()
    


# def py_callback(value):
#     print("Value sent from Javascript: "+value)

class LoadHandler(object):
    def OnLoadEnd(self, browser, **_):
        browser.ExecuteFunction("load_puzzle", json.dumps(get_puzzle()))


if __name__ == '__main__':
    main()
