import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


BeginState = "S1"

endStates = dict()
endStates["S5"] = 'End'

yesTrans = dict()
yesTrans["S1"] = ["S2", "S1_Yes"]
yesTrans["S2"] = ["S3", "S2_Yes"]
yesTrans["S3"] = ["S4", "S3_Yes"]
yesTrans["S4"] = ["S5", "S4_Yes"]

noTrans = dict()
noTrans["S1"] = ["S2", "S1_No"]
noTrans["S2"] = ["S3", "S2_No"]
noTrans["S3"] = ["S4", "S3_No"]
noTrans["S4"] = ["S5", "S4_No"]




@ask.launch

def new_game():
    
    welcome_msg = render_template('welcome')
    session.attributes['state'] = BeginState
    session.attributes['help'] = False

    start = render_template(session.attributes['state'])

    return question(welcome_msg + " " + start)


@ask.intent("YesIntent")

def next_round():

    #if currently in help state
    if(session.attributes['help']):
        round_msg1 = render_template('continue')
        round_msg2 = render_template(session.attributes['state'])
        session.attributes['help'] = False
        return question(round_msg1 + " " + round_msg2)

    session.attributes['state'], next_statement = yesTrans[session.attributes['state']]
    
    if(session.attributes['state'] in endStates):
        #retrieve the specific end message for the specific state
        round_msg = render_template(endStates[session.attributes['state']])
        round_msg1 = render_template(next_statement)
        return statement( round_msg1 + " " + round_msg)
    else:
        round_msg = render_template(next_statement)
        round_msg1 = render_template(session.attributes['state'])
        return question(round_msg+ " " + round_msg1)

@ask.intent("NoIntent")
def next_round():
    if(session.attributes['help']):
        round_msg = render_template('helpno')
        return statement(round_msg)


    session.attributes['state'], next_statement = noTrans[session.attributes['state']]

    if(session.attributes['state'] in endStates):
        #retrieve the specific end message for the specific state
        round_msg = render_template(endStates[session.attributes['state']])
        round_msg1 = render_template(next_statement)
        return statement(round_msg1 + " " + round_msg)
    else:
        round_msg = render_template(next_statement)
        round_msg1 = render_template(session.attributes['state'])
        return question(round_msg + " " + round_msg1)


@ask.intent("AMAZON.HelpIntent")

def next_round():

    session.attributes['help'] = True
    round_msg = render_template('help')
    return question(round_msg)

@ask.intent("AMAZON.StopIntent")
def next_round():
    round_msg = render_template('stop')
    return statement(round_msg)

@ask.intent("AMAZON.CancelIntent")
def next_round():
    round_msg = render_template('stop')
    return statement(round_msg)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
