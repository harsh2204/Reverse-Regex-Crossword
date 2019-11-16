# TODO: Send relevant data from back-end to front-end js.
# Get script files to load localy, either using the initialization parameters or running an internal server serving those files.
# Use that data to construct a N^M grid of puzzle
# Add ability to change letters
# Add letters look at camera always

from cefpython3 import cefpython as cef



def main():
    cef.Initialize()
    browser = cef.CreateBrowserSync(url=cef.GetDataUrl(open('cube.html', 'r').read()),
                                    window_title="Javascript Bindings")
    # browser.SetClientHandler(LoadHandler())
    # bindings = cef.JavascriptBindings()
    # bindings.SetFunction("py_function", py_function)
    # bindings.SetFunction("py_callback", py_callback)
    # browser.SetJavascriptBindings(bindings)
    cef.MessageLoop()
    del browser
    cef.Shutdown()


# def py_function(value, js_callback):
#     print("Value sent from Javascript: "+value)
#     js_callback.Call("I am a Python string #2", py_callback)


# def py_callback(value):
#     print("Value sent from Javascript: "+value)


# class LoadHandler(object):
#     def OnLoadEnd(self, browser, **_):
#         browser.ExecuteFunction("js_function", "I am a Python string #1")


if __name__ == '__main__':
    main()
