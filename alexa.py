import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


BeginState = "S1"

endStates = list()
endStates.append("S4")

yesTrans = dict()
yesTrans["S1"] = "S4"
yesTrans["S2"] = "S4"
yesTrans["S3"] = "S1"

noTrans = dict()
noTrans["S1"] = "S2"
noTrans["S2"] = "S3"
noTrans["S3"] = "S4"



@ask.launch

def new_game():
    
    welcome_msg = render_template('welcome')
    win = render_template('win')
    #win = render_template('win')
    session.attributes['state'] = BeginState
    session.attributes['help'] = False

    return question(welcome_msg + " " + win)


@ask.intent("YesIntent")

def next_round():

    #if currently in help state
    if(session.attributes['help']):
        round_msg = render_template('round', state=session.attributes['state'])
        session.attributes['help'] = False
        return question(round_msg)

    session.attributes['state'] = yesTrans[session.attributes['state']]
    
    if(session.attributes['state'] in endStates):
        round_msg = render_template('end')
        return statement(round_msg)
    else:
        round_msg = render_template('round', state=session.attributes['state'])
        return question(round_msg)

@ask.intent("NoIntent")
def next_round():
    if(session.attributes['help']):
        round_msg = render_template('helpno')
        return question(round_msg)


    session.attributes['state'] = noTrans[session.attributes['state']]

    if(session.attributes['state'] in endStates):
        round_msg = render_template('end')
        return statement(round_msg)
    else:
        round_msg = render_template('round', state=session.attributes['state'])
        return question(round_msg)


@ask.intent("AMAZON.HelpIntent")

def next_round():

    session.attributes['help'] = True
    round_msg = render_template('help')
    return question(round_msg)

@ask.intent("AMAZON.StopIntent")
def next_round():
    round_msg = render_template('stop')
    return statement(round_msg)

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)
