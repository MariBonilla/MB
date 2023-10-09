from flask import Blueprint, render_template, request, redirect

import pyrebase
import time
import requests

# Firebase configuration 
firebase_config = {
    "apiKey": "AIzaSyBPqJ-k5eE3VvcwohxAPUjk0FtI9CmuQQk",
    "authDomain": "venom-36428.firebaseapp.com",
    "databaseURL": "https://venom-36428-default-rtdb.firebaseio.com",
    "projectId": "venom-36428",
    "storageBucket": "venom-36428.appspot.com",
    "messagingSenderId": "918438359333",
    "appId": "1:918438359333:web:3c95ae1e6ea1cb872eaacc",
    "measurementId": "G-6ML5XV7KN3"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database() # reference to our database

storage = firebase.storage() # reference to our storage

# allows routes to be called in other files
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about-us')
def aboutus():
    return render_template("aboutus.html")

@views.route('/search/<query>', methods = ['POST','GET'])
def search(query):
    # Gets all text after /search/ and saves it in the string "query".
    
    gameDBSnapshot = db.child("games").get().val()
    searchedList = dict()
    
    for game in gameDBSnapshot:
        """
        For every game, if the search query is in that the title, add
        that game to the list of games to display to the user.
        """
        imageURLS = list()
        if query.lower() in game.lower():
            searchedList[game]=gameDBSnapshot[game]
            
            gameImagePath = "games/" + game + "/" + game + ".png"
            
            # requires None as a token for pyrebase - known issue since 2017
            imageURL = storage.child(gameImagePath).get_url(None)
            
            searchedList[game]["imageURL"] = imageURL
    
    # Supply a backup image for games with no image
    backupImage = storage.child("games/defaultGameImage.png").get_url(None)
    
    return render_template("searchResults.html", gameList = searchedList, backupImage = backupImage)