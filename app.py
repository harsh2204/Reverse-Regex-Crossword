# TODO: 
# [x] Send relevant data from back-end to front-end js.
# [x] Get script files to load localy, either using the initialization parameters or running an internal server serving those files.
#       Have to implement either a resource handler or copy from https://github.com/rentouch/cefpython_old/blob/master/cefpython/cef3/linux/binaries_32bit/wxpython-response.py.
#       ^(Keep in mind that this is not compatible on all OS'es)
#  OR   Run a fast server locally, before starting the app to load the js files.
#  OR   Make internet connection a requirement for the app.
# 
# [x] Use that data to construct a N^M grid of puzzle
# [x] Add ability to change letters
# [x] Add letters look at camera always
# [ ] Connect frontend and backend

from cefpython3 import cefpython as cef
import platform
import ctypes
from string import ascii_uppercase
from pprint import pprint
from src.grid import Puzzle
from src import regex
import numpy as np
import json

puzzle = []
patterns = []

def main():
    cef.Initialize()
    window_info = cef.WindowInfo()
    parent_handle = 0
    # This call has effect only on Mac and Linux.
    # All rect coordinates are applied including X and Y parameters.
    window_info.SetAsChild(parent_handle, [0, 0, 1720, 1440])

    browser = cef.CreateBrowserSync(url=cef.GetDataUrl(open('cube.html', 'r').read()),
                                    window_info=window_info,
                                    window_title="Javascript Bindings",
                                    settings={
                                        'universal_access_from_file_urls_allowed':  True,
                                        'file_access_from_file_urls_allowed':       True
                                    })
                                    
    if platform.system() == "Windows":
        window_handle = browser.GetOuterWindowHandle()
        insert_after_handle = 0
        # X and Y parameters are ignored by setting the SWP_NOMOVE flag
        SWP_NOMOVE = 0x0002
        # noinspection PyUnresolvedReferences
        ctypes.windll.user32.SetWindowPos(window_handle, insert_after_handle,
                                          0, 0, 1720, 1440, SWP_NOMOVE)

    browser.SetClientHandler(LoadHandler())
    
    bindings = cef.JavascriptBindings()
    bindings.SetFunction("get_puzzle", get_puzzle)
    bindings.SetFunction("load_patterns", load_patterns)
    browser.SetJavascriptBindings(bindings)

    cef.MessageLoop()
    del browser
    cef.Shutdown()

def load_patterns(data, i, callback):
    global puzzle, patterns
    callback.Call(regex.get_patterns(data, patterns), i)
    # callback.Call(patterns)

def get_puzzle(string, callback):
    global puzzle, patterns
    # puzzle = Puzzle('assume,foodee,nation')
    puzzle = Puzzle(string)
    vectors = puzzle.vectors
    print(vectors)
    patterns = regex.generate_patterns(vectors)
    pprint(patterns)
    callback.Call(vectors.tolist(), patterns)
    


class LoadHandler(object):
    def OnLoadEnd(self, browser, **_):
        # browser.ExecuteFunction("fetch_puzzle")
        pass


if __name__ == '__main__':
    main()
