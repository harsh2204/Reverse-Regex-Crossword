# Reverse-Regex-Crossword

A 3D implemetation of regex crossword with a rule-based regex generator that uses vanilla and cef-python in the back-end with three.js for the front-end.

The current implementation of the app requires a http server running in the js directory, because cef-python can't server javascript files internally. The alternative to this would be add an internet connect as a requirement for it, which I am against for now. <sub><sup>Maybe something/someone can change my mind</sup></sub>

The implementation still needs a little bit of work in generalizing the 3D parameterization of the n-dimension puzzle. I tried to write this app as general as possible from the ground up and I've reached the point where I just wanted to see it work. So now, I just have to backtrack my steps and add more general code to get this app to work with any dimension of puzzle.
