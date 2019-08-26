# RPSSL Application & Service
### Rock Paper Scissors Spock Lizard
Author: [Nathan Murrow (murrown)](https://www.linkedin.com/in/nathan-murrow)

## Deployment
This project requires Python >= 3.7 and Django >= 2.2.4
```
git clone https://github.com/murrown/rpssl.git && cd rpssl
pip3 install -r pip3_requirements.txt
```
There are some unit/integration tests for testing the game logic, the AI, and the `/play/` endpoint. Verify that they pass like so:
```
./manage.py test -v2
```
To run the server, you must use `testserver`, not `runserver`. This is because the database is stored entirely in memory, so the application needs to load a fixture from a file. `empty_fixture.json` contains two users and no data.
```
./manage.py testserver empty_fixture.json
```
This will run the server on localhost port 8000.

The test users are as follows:

Username | Password 
-------- | --------
test_user | test_password
test_user2 | test_password2

## API
### Endpoints
Method | URI | Accepts Data | Purpose
------ | --- | ------------ | -------
GET | /choices/ | | Get a list of valid choices and their numerical values.
GET | /choice/ | | Get a random choice from the server.
POST | /play/ | :heavy_check_mark: | Submit a choice to play a round with the server.

#### /choices/
No POST data required.

Response:
```
[{"choice": {
    "id":   [Numerical value of this choice. (1-5)],
    "name": [Name of this choice as a string.],
    }
 }
 ... [Returns all five choices.]
]
```
#### /choice/
No POST data required.

Response:
```
{"choice": {
    "id":   [Numerical value of this choice. (1-5)],
    "name": [Name of this choice as a string.],
    }
}
```
#### /play/
POST data:
```
{"player": [Numerical value of your choice],
}
```

Response:
``` 
{"results":  [Results of the round, one of {"win", "lose", "tie"}],
 "player":   [Numerical value of the player's choice],
 "computer": [Numerical value of the computer's choice],
}
```

A result of "win" is a win for the player, and "lose" is a loss for the player.

## Web Client
To test the client, navigate your web browser to 127.0.0.1:8000 while the server is running.

### Home
You can play the game on the homepage. The gameplay page is a single-page app without refreshes.

Select any button to make your play. You can use the hotkeys `r`, `s`, `p`, `o`, and `l` to play using the keyboard. The computer opponent will make its own selection and the results of the round will be displayed.

The more you play against the computer, the better it will get at predicting your actions. (NOTE: Because the database is stored in memory, the computer's knowledge is not persistent and will be erased as soon as you shut down the server.)

### Scoreboard
Displays the 10 most recent games, from newest to oldest. (NOTE: Because the database is stored in memory, this scoreboard will be erased as soon as you shut down the server.)

### Login/Logout/Register
You can create and play as a user. The computer will personalize its gameplay choices depending on who is playing. Multiple users can play the game at the same time (to test this out, use multiple browsers or containerized tabs).

There are two users already created for testing purposes. They are:

Username | Password 
-------- | --------
test_user | test_password
test_user2 | test_password2

## Stack
Django for backend

SQLite in memory for database

Typescript & jQuery for frontend

Bootstrap for CSS

## Ideas for Future Improvements
- Resettable scoreboard. Each game logs its submission time, so this could be implemented by simply filtering all results older than a specific time.
- Update the scoreboard in real time instead of requiring page refreshes.
- Make the artificial intelligence statistical instead of deterministic and predictable.
- The ability to play as a specific user with the API. Requires authentication and better security to prevent spoofing other users.
- More unit tests for endpoints & frontend.

## Credits
Game rules - http://www.samkass.com/theories/RPSSL.html

Random numbers - https://codechallenge.boohma.com/random
