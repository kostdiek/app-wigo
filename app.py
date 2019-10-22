# app.py
from flask import Flask, request, jsonify
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

#Trigger
@app.route('/trigger/',  methods=['GET'])
def words():
    # Retrieve the name from url parameter
    title = request.args.get("name", None)

    # For debugging
    print(f"got name {title}")

    response = {}

    # Check if user sent a name at all
    if not title:
        response["ERROR"] = "no title found, please send a title."
    # Check if the user entered a number not a name
    elif str(title).isdigit():
        response["ERROR"] = "title can't be numeric."
    # Now the user entered a valid name
    else:
        ia = IMDb()

        #search for the movie title
        movie_title = ia.search_movie(title)
        movie_id = movie_title[0].movie_id
        movie = ia.get_movie(movie_id)
        response["MESSAGE"] = f"Let's look at this movie: {movie} "

    # Return the response in json format
    return jsonify(response)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
