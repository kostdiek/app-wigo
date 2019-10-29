# README for the Triggers in Movie application

## A Tutorial involving Python, Flask, Heroku, and HTML

#### By Karen Ostdiek
##### With massive help from the internet...

## Introduction
---
This idea was originally convinced because I have my own triggers - things I would rather not see come up in a movie or at least not be blindsided by it. The following will be a (hopefully) complete tutorial of how I made this, from start to finish.


## Things Needed
---
1. IMDbpy - Python package for IMDb database
2. Python 3 (I started by testing out my Python code in Jupyter notebooks but it's not specifically neccessary).
3. Flask - micro web framework written in Python
4. Heroku - cloud platform to build, run, and operate applications
5. HTML/CSS
6. Github

## Project Walkthrough
---
## Python Code
I won't go over here how to install Python or Jupyter.

In order for this project to even get off the ground, I needed to figure out a way to pull movie information (like a synopsis...) from Wikipedia or IMDb. Conveniently, there already exisits a Python package that retrieves data from the International Movie Database (IMDb) web server. This package is called IMDbPY and can be found here: [https://pypi.org/project/IMDbPY/](https://pypi.org/project/IMDbPY/). Installing the package is straight forward (as documented on their site) and you can other usefuly information on their site as well.

Once the IMDbPY package is installed, the Python code goes like the following:
```Python
#import the IMDbPY package
from imdb import IMDb
#create an instance of IMDb
ia = IMDb()
#set a title (or ask the user for one)
title =
#search for a movie title
movie_title = ia.search_movie(title)
#there will be multiple search results; for now let's the pick the first one [0] and find it's ID
movie_id = movie_title[0].movieID
#now let's really get the movie - all of the IMDb information
movie = ia.get_movie(movie_id)
#from here there are lots of things one could get about this movie, but we need specifically it's synopsis
#the [0] in the following is used to get the synopsis as a string for searching later
synopsis = movie['synopsis'][0]
#next, set a trigger word or have the user set one
trigger =
#and search for it using the find Python function
trigger_lookup = synopsis.find(trigger)
#if the trigger_lookup is -1 then the trigger word wasn't found in the synposis. Otherwise the find function will return the location of the trigger word in the string.
```
The Python code is relatively straight forward, though further complexities could be added.

So how do we make this usable by people who aren't on my computer running a Jupyter notebook?

## Flask Code
Using Flask and Heroku was a idea I got from the internet, specifically the GitHub repository on [Building an Insight App](https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50).

While the above repository is a good start, I whole-heartedly recommend the post on [Deploying a Flask Application to Heroku]{https://stackabuse.com/deploying-a-flask-application-to-heroku/}. This walk-through is a good place to start with a Hello World type app.

I hope that I can bring the gaps that I found between the two above tutorials but I won't go through every line of my code, just the useful examples.

First (after installing Flask of course, see their documentation [here](http://flask.palletsprojects.com/en/1.1.x/)), import Flask and several other needed-later pieces.
```Python
from flask import Flask, request, jsonify, render_template, redirect, url_for
app = Flask(__name__)
```
Each page on our app/website will have its own "function". For example, the homepage for this application looks like:

```python
@app.route('/')
def hello_world():
    return render_template('index.html')
```

Basically, when the app runs and is directed to the homepage (the '/' part of @app.route('/')), the hello_world function will run. In this case, hello_world finds the index.html file (more on that later) and renders it on the page.

## HTML + Flask
Logically it makes sense to walk through the HTML code along side the Flask code as they are intimately connected. So let's start with the HTML file for the homepage.

Beyond the standard HTML code such as style, titles, language, etc., the coding for this application's homepage include a form. In this form, the user can enter the name of a movie:

```html
<h4>Search for a Movie: </h4>
    <p>Please use the text box to search for a movie title. Then click "Submit."</p>
    <form action="/multi_movie" method="post">
      <input type="text" name="title2"></input>
      <input type="submit" value="Submit"></input>
    </form>
```
which renders like:

<h4>Search for a Movie: </h4>
    <p>Please use the text box to search for a movie title. Then click "Submit."</p>
    <form action="/multi_movie" method="post">
      <input type="text" name="title2"></input>
      <input type="submit" value="Submit"></input>
    </form>
<br>

When a user enters a string into the text box (`<input type="text">`), and clicks on the submit button (`<input type="submit">`), then the html code sends that information back to the Flask code, which matches with the form's action value (`<form action ="/multi_movie" method="post">`). The corresponding Flask code contains the following:

```Python
@app.route('/multi_movie', methods = ['POST'])
def multi_movie():
    title = request.form['title2']
    ia = IMDb()
    #search for the movie title
    movie_title = ia.search_movie(title)

    return render_template('multi_movie.html', title=movie_title, len=len(movie_title))
```

Note the '/multi_movie' in the route. On clicking submit on the HTML form from the homepage, the application is sent to this page and runs the function `def multi_movie()`. This function takes the string from the text box (title2) and uses that value in the IMDbPY search_movie function. In this case, the search result is more than one movie. I wanted the user to be able to select which movie they meant from the search results. So in the `return render_template`, we render the next html page (multi_movie.html) and send other variables to be used in that html code: 1. the search results and 2. the length (or number) of those results (which I didn't use... but could have).

The html code for multi_movies.html takes the search results and the number of results and produces a drop down list for the user to pick from using the following:

```HTML
<form action= "/calculate" method="POST">

      <select name = 'title' >
          <option value = "Please Select One" SELECTED>Please Select One </option>
          {%for name in title %}
          <option value = "{{name.movieID}}" >{{name["long imdb canonical title"]}}</option>"
          {%endfor%}
      </select>
      <input type="text" name="word3"></input>
      <input type="submit" value="Submit"></input>
    </form>
```

The for loop in the middle loops over the results (sent from the Flask function using the variable 'title'; remember `title=movie_title` from `render_template`). The value for each in the dropdown list is the movie's ID number (as specified by IMDb) but the movie's full title is what the user sees. The default value that the page renders is "Please Select One" as indicated by the `SELECTED` piece of the `<option value = "Please Select One" SELECTED>`. In this form, we also ask the user for their trigger word in `input type="text"` and include a submit button as before.

When this submit button is clicked, it looks for the corresponding route in the Flask code (`/calculate`) as we saw before.

Once the Python, Flask, and HTML/CSS are looking good, we can push this on to Heroku.

## Heroku

The first thing to do is to define the libraries used by our application. This allows Heroku to know which ones we need just like we do for running the application locally. To do this, we need to create a requirements text file by running the following:

`pip freeze > requirements.txt`

This will find all of the libraries that we are currently using and put their names and versions into a text file, saved as requirements.txt. In this file, we may get far more libraries than Heroku really needs. We may also get lines that look like `html5lib=1.0.1=py37_0` which should be trimmed down to `html5lib==1.0.1` (note the double equal sign as well). For each libary used, you'll need to make sure it is in this file. If it's not, Heroku will not be able to run your application.

Next, you'll need a file saved as "Procfile", no extension, that contains the following:

`web: gunicorn app:app`

The web command tells Heroku to start a web server using gunicorn. Since I've saved my application as app.py, app is set to app as well.

Next, create a Heroku account and a new app from the dashboard.

Now, in the terminal, we'll use git to send what we need to Heroku. Make a git repository first, in the application's local directory.

`git init .`

Now add the files, all of them including the html files (which for me were located in a subfolder called templates):

`git add app.py Procfile requirements.txt templates/index.html templates/multi_movie.html templates/calculate.html`
`git commit -m "some commit message goes here"`

Log in to your Heroku account (use the option -i for doing this in the terminal):

`heroku login -i`

Next add the repository to the remote one (using your Heroku's project name):

`heroku git: remote -a {your-project-name}`

And then push the files to Heroku:

`git push heroku master`

You'll get some outputs to the terminal that should end with `remote: Verifying deploy ... done.`

From here, you can test the application by going to its domain, which you'll find in the application's Setting tab on the Heroku dashboard. Look for Domains and certificates. The webpage should be something along the lines of https://{your-project-name}.herokuapp.com/.

## Future Improvements
---
1. Allow for multiple words to be added to the trigger text box, separated by commas possibly.
2. Create "users" so an individual doesn't have to add their trigger in each time they want to search.
3. Maching learning - Natural language processing to analyze **IF** a movie **could** contain a trigger. 
