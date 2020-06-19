from gtts import gTTS
import speech_recognition as sr
import re
import time
from time import ctime
import webbrowser
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import requests
from pygame import mixer
import urllib.request
import urllib.parse
import json
import bs4
import wolframalpha
import wikipedia


def talk(audio):
    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text=audio, lang='en-uk')
        text_to_speech.save('audio.mp3')
        mixer.init()
        mixer.music.load("audio.mp3")
        mixer.music.play()
        

def myCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Waiting for command...')
        r.pause_threshold = 2

        r.adjust_for_ambient_noise(source, duration=1)

        audio = r.listen(source)
        print('analyzing...')

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
        time.sleep(2)

    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand()
    return command

def commands_for_assistant(command):
    errors=[
        "Sorry, I didn't get that",
        "I didn't hear you my Sir",
        "Could you say it again my Sir?",
        "Could you repeat my Sir?"
    ]
    

    if 'open google and search' in command:
        regex = re.search('open google and search (.*)', command)
        search_for = command.split("search", 1)[1]
        print(search_for)
        url = 'https://www.google.com/'
        if regex:
            subgoogle = regex.group(1)
            url = url + 'r/' + subgoogle
            talk('Yes Sir, I am searching!')
            driver = webdriver.Firefox(executable_path='/home/kuba/Pulpit/geckodriver/geckodriver')
            driver.get('http://www.google.com')
            search = driver.find_element_by_name('q')
            search.send_keys(str(search_for))
            search.send_keys(Keys.RETURN)
    
    elif 'send email' in command:
        talk('What is the subject?')
        time.sleep(3)
        subject = myCommand()
        talk('What should i say?')
        message = myCommand()
        from_mail_address = 'mail@mail'
        to_mail_address = 'mail@mail'
        content = 'Subject: {}\n\n{}'.format(subject, message)
        
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        mail.login('mail', 'password')

        mail.sendmail(from_mail_address, to_mail_address, content)

        mail.close()
        talk('Email sent successfully Sir.')

    elif 'wikipedia search' in command:
        regex = re.search('wikipedia (.+)', command)
        if regex:
            query = command.split("wikipedia search",1)[1]
            response = requests.get("https://en.wikipedia.org/wiki/" + query)
            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')
                title = html.select("#firstHeading")[0].text
                paragraphs = html.select('p')
                for para in paragraphs:
                    print(para.text)
                intro = '\n'.join([ para.text for para in paragraphs[0:2]])
                print(intro)
                mp3name = 'speech.mp3'
                language = 'en'
                myobj = gTTS(text=intro, lang=language, slow=False)
                myobj.save(mp3name)
                mixer.init()
                mixer.music.load('speech.mp3')
                mixer.music.play()
    elif 'stop' in command:
        mixer.music.stop()

    elif 'open youtube' in command:
        talk('Yes Sir, I am opening youtube!')
        regex = re.search('open youtube (.+)', command)
        if regex:
            domain = command.split("youtube",1)[1]
            query_string = urllib.parse.urlencode({"search_query" : domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            pass

    elif 'weather in' in command:
        city = command.split("in", 1)[1]

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=19da9a9fe38156dfb6094e86c35679a7'.format(city)
        response = requests.get(url)
        data = response.json()

        temperature = data['main']['temp']
        round_temperature = int(round(temperature))

        talk('It is {} degree celsius in {}, my Sir!'.format(round_temperature, city))
        time.sleep(3)

    elif 'where is' in command:
        command = command.split(" ")
        url_maps = "https://www.google.nl/maps/place/" + str(command[2]) + '/&amp;'
        talk("Let me check my Sir")
        webbrowser.get().open(url_maps)

    elif 'what time is it' in command:
	    #current_time = ctime()
        #print(ctime())
        talk(f'It is' + ' '+ ctime() + ' ' + 'my Sir!')
        time.sleep(2)

    elif 'how much is' in command:
        question = command
        application_id = "VY97WR-GLQVJGA42U"
        client = wolframalpha.Client(application_id)
        result = client.query(question)
        answer = next(result.results).text
        talk(f'It is {answer} my Sir!')

    elif 'who is' in command:
        response = command.split(" ")
        wiki = wikipedia.summary(response, sentences=1)
        talk(wiki)
        time.sleep(2)


    elif 'layla' in command:
        talk('What can I do for You?')
        time.sleep(2)

    elif 'hello' in command:
        talk('Hello Sir! How can I help you?')
        time.sleep(2)

    elif 'hi' in command:
        talk('What\'s up Buddy?')
        time.sleep(2)

    elif 'good morning' in command:
        talk('Good morning! What a beautiful day my Sir! ')
        time.sleep(2)
    
    elif 'hey' in command:
        talk('Hey hey, Wanna something?')
        time.sleep(2)

    elif 'who are you' in command:
        talk('I am your personal virtual assistant my Sir!')
        time.sleep(2)

    elif 'what is your name' in command:
        talk('My name is LAYLA my Sir!')
        time.sleep(2)

    elif 'thank you' in command:
        talk('It is pleasure my Sir!')
        time.sleep(2)

    elif 'who am i' in command:
        talk('You are Jacob, my Boss, my Sir, my Lord, my best Friend, You\'re my everything!')
        time.sleep(2)
    
    elif 'by' in command:
        talk('Bye my lovely friend!')
        time.sleep(2)
        exit()

    elif 'arrivederci' in command:
        talk('Arrivederci my Sir!')
        time.sleep(2)
        exit()

    elif 'how are you' in command:
        talk('I feel exciting because of You my Sir!')
        time.sleep(2)

    elif 'nice' in command:
        talk('Everything for you my Sir!')
        time.sleep(2)

    else:
        error = random.choice(errors)
        talk(error)
        time.sleep(3)

    
talk('Welcome my Sir! I am all for you!')


while True:
    time.sleep(4)
    commands_for_assistant(myCommand())
