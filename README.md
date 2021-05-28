# Reverse-Regex-Crossword

A 3D implemetation of [regex crossword](https://regexcrossword.com/) with a rule-based regex generator that uses a cef-python in the back-end with three.js for the front-end along with the generator writting in vanilla python.

![regex3d](https://github.com/harsh2204/Reverse-Regex-Crossword/raw/master/regex.png)

The current implementation of the app requires a http server running in the js directory, because cef-python can't server javascript files internally. The alternative to this would be to add an internet connect as a requirement for it, which I am against for now. <sub><sup>Maybe something/someone can change my mind</sup></sub>

The implementation still needs a little bit of work in generalizing the 3D parameterization of the n-dimension puzzle. I tried to write this app as general as possible from the ground up and I've reached the point where I just wanted to see it work. So now, I just have to backtrack my steps and add more general code to get this app to work with any dimension of puzzle.
