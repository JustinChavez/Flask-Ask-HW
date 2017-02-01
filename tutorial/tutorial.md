In this tutorial I will be teaching how to make a Yes/No Framework easily as an Amazon Alexa skill.

For this tutorial I will demonstrate by encoding one of my favorite flowcharts from PHD Comics:

http://www.phdcomics.com/comics.php?f=1632

(Note: I will be adding slight adjustments to the logic flow since not all answers are Yes/No in the comic.)

We will be using the Python framework [Flask-Ask](https://github.com/johnwheeler/flask-ask) for this tutorial. Please follow [this quick introduction](https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development) to the framework to get your development environment setup.

With your development environment set we can now move on 

First before you start you should have the framework you want to build into the Alexa skill ready. Just make sure that there is only one state that your logic flow starts with and only Yes/No answers each question.

Next take your flowchart and label each question and ending statement with a number for reference to its state. 

Insert phd02

In Python we will be using these state references to build the framework. 

Now in your Python file, set a variable BeginState to reference the state that your framework begins on. For mine that would be state S1

'''Python
BeginState = "S1"
'''
