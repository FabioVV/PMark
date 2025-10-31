# PMark

## A very simple static site generator.

This is a static site generator written in Python meant to be fast and used with minimal setup.
I use it to generate my stuff, but if you find it useful, feel free to contribute to the project and/or use it for your stuff too.

## Requirements
  - Python 3.11+

## Usage
  - To run, simply clone the project and inside the cloned folder type in the following:
  -  `python run.py` or `python3 run.py`.
  - Then in the browser you should be able to access localhost:8001, which is where the files will be served for visualization
  - There should be a `static` and `content` directories inside of the cloned folder. If they are not there, make them
  - Inside of the static folder you should keep all of your static files like scripts, images and CSS. Follow this simple folder structure for correct generation:
    - static/
      - img/
      - css/
      - js/
  - Inside of the content folder is where you are going to write you markdown, the directory structure you create here will be the same in the generated HTML content
  - If after running the program everything goes well, you should see a docs/ directory inside of you CWD, all of the generated HTML will be in there

## Testing
  - To test the app, simply run the run.py file like so: `python test.py` or `python3 test.py`

## Caveats
  - This app is still in active development
  - There are some small know problems, i am working on them
  - There are some usability problems(heh). Right now, it is meant to be used as a script and it is advised to use the default folder locations the app provides, as they are all relative to the current working directory and should not throw any problems. I am working on a 'fix' for this, so that you may be able to pass in via CMD or a graphical interface any path you want to use.
