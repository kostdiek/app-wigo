# app.py

#Heroku app setttings: https://dashboard.heroku.com/apps/app-wigo/settings

#Udacity NYC Subway Data Analysis: https://github.com/rkpaira/Udacity_NYC-Subway-Data-Analysis/blob/master/Analyzing_Subway_Data_NDFDSI.ipynb

#Building an Insight App: https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50

#Deploying Flask App on Heroku: https://stackabuse.com/deploying-a-flask-application-to-heroku/

#Websites with Python and Flask: https://opentechschool.github.io/python-flask/core/form-submission.html

#info for dropdown list?: https://stackoverflow.com/questions/49628274/unable-to-get-value-selected-in-python-from-a-dropdown-using-flask

#find process to kill:  ps -fA | grep python
#kill process: kill -9 processNumber

from flask import Flask, request, jsonify, render_template, redirect, url_for
app = Flask(__name__)

#imdb package
from imdb import IMDb

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    print("The email address is '" + email + "'")
    return redirect('/thanks/')

@app.route('/thanks/')
def thanks():
    return 'Thanks for signing up!'


@app.route('/movie', methods = ['POST'])
def movie():
    title = request.form['title']
    trigger = request.form['word']
    ia = IMDb()
    #search for the movie title
    movie_title = ia.search_movie(title)
    movie_id = movie_title[0].movieID
    movie = ia.get_movie(movie_id)
    #find the synopsis
    synopsis = movie['synopsis'][0]
    #using the python find function, see if the trigger word is in the synopsis of the movie
    trigger_lookup = synopsis.find(trigger)
    #using the python find function, see if the trigger word is in the synopsis of the movie
    trigger_lookup = synopsis.find(trigger)
    if trigger_lookup == -1:
        trigger_output = "Okay but proceed with caution"
    else:
        trigger_output = "Trigger word detected"
    return render_template('movie.html', output = trigger_output, title = movie_title[0])

@app.route('/multi_movie', methods = ['POST'])
def multi_movie():
    title = request.form['title2']
    trigger = request.form['word2']
    ia = IMDb()
    #search for the movie title
    movie_title = ia.search_movie(title)

    return render_template('multi_movie.html', output = trigger, title=movie_title, len=len(movie_title))

#Trigger
#@app.route('/trigger/',  methods=['GET'])
#def words():
    # Retrieve the name from url parameter
#    title = request.args.get("name", None)

    # For debugging
#    print(f"got name {title}")

#    response = {}

    # Check if user sent a name at all
#    if not title:
#        response["ERROR"] = "no title found, please send a title."
    # Check if the user entered a number not a name
#    elif str(title).isdigit():
#        response["ERROR"] = "title can't be numeric."
    # Now the user entered a valid name
#    else:
#        ia = IMDb()
        #search for the movie title
#        movie_title = ia.search_movie(title)
#        movie_id = movie_title[0].movieID
#        movie = ia.get_movie(movie_id)
        #find the synopsis
#        synopsis = movie['synopsis'][0]
        #set a trigger word
#        trigger = 'suicide'
        #using the python find function, see if the trigger word is in the synopsis of the movie
#        trigger_lookup = synopsis.find(trigger)
#        if trigger_lookup == -1:
#            response["MESSAGE"] = f"Okay but proceed with caution"
#        else:
#            response["MESSAGE"] = f"Trigger word detected"

    # Return the response in json format
#    return jsonify(response)


    #using the python find function, see if the trigger word is in the synopsis of the movie
    #trigger_lookup = synopsis.find(trigger)
    #if trigger_lookup == -1:
    #    response["MESSAGE"] = f"Okay but proceed with caution"
    #else:
    #    response["MESSAGE"] = f"Trigger word detected"

    # Return the response in json format
    #return jsonify(response)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
