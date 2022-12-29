import array
import csv
import os
import re
import time

import cv2
import face_recognition
import lxml
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField

app = Flask(__name__, template_folder='template',
            static_folder='template/assets')
app.config['UPLOAD_FOLDER'] = 'static'
app.config['SECRET_KEY'] = 'supersecretkey'

path = 'image'
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


class uploadFileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload File')


encodeList = np.loadtxt('train.txt')


@app.route('/', methods=['GET', "POST"])
@app.route('/pt', methods=['GET', "POST"])
def home():
    form = uploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  app.config['UPLOAD_FOLDER'], secure_filename('test.jpg')))

        imgtest = face_recognition.load_image_file('static/test.jpg')
        imgtest = cv2.cvtColor(imgtest, cv2.COLOR_BGR2RGB)
        encodetest = face_recognition.face_encodings(imgtest)[0]
        matches = face_recognition.compare_faces(encodeList, encodetest)
        faceDis = face_recognition.face_distance(encodeList, encodetest)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex+1].upper()
            facedis = faceDis[matchIndex]

        data = []
        data.append(f'Player Name: {name}')
        data.append(f'FaceDis: {facedis}')
        print(name)
        source = requests.get(f"https://www.google.com/search?q={name}%20cricbuzz").text

        page = BeautifulSoup(source, "lxml")
        page = page.find("div",class_="kCrYT")
        link = page.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs["href"]
        c =  requests.get(link[7:]).text
        cric = BeautifulSoup(c, "lxml")

        profile = cric.find("div",id="playerProfile")
        pc = profile.find("div",class_="cb-col cb-col-100 cb-bg-white")

        #name country and image
        name = pc.find("h1",class_="cb-font-40").text  #1
        country = pc.find("h3",class_="cb-font-18 text-gray").text #2
        images = pc.findAll('img')
        for image in images:
            i = image['src']    #3

        #personal information and rankings
        personal =cric.find_all("div",class_="cb-col cb-col-60 cb-lst-itm-sm")
        role = personal[2].text.strip()  #5
        icc = cric.find_all("div",class_="cb-col cb-col-25 cb-plyr-rank text-right")
        tb = icc[0].text.strip()  #6
        ob = icc[1].text.strip()  #7
        twb = icc[2].text.strip() #8

        tbw=icc[3].text.strip()  #9
        obw=icc[4].text.strip()  #10
        twbw=icc[5].text.strip() #11


        #summary of the stata
        summary  = cric.find_all("div",class_="cb-plyr-tbl")
        batting =summary[0]
        bowling =summary[1]

        cat = cric.find_all("td",class_="cb-col-8")


        batstat = batting.find_all("td",class_="text-right")
        #test
        testmatches = batstat[0].text
        testruns = batstat[3].text
        tesths = batstat[4].text
        testavg = batstat[5].text
        testsr = batstat[7].text              
        test100 = batstat[8].text
        test50 = batstat[10].text

        #odii
        odimatches = batstat[13].text
        odiruns = batstat[16].text
        odihs = batstat[17].text
        odiavg = batstat[18].text
        odisr = batstat[20].text
        odi100 = batstat[21].text      
        odi50 = batstat[23].text

        #t20
        tmatches = batstat[26].text
        truns = batstat[29].text
        ths = batstat[30].text
        tavg = batstat[31].text         
        tsr = batstat[33].text
        t100 = batstat[34].text
        t50 = batstat[36].text


        bowstat = bowling.find_all("td",class_="text-right")

        testballs = bowstat[2].text
        testbruns = bowstat[3].text
        testwickets = bowstat[4].text
        testbbi = bowstat[5].text
        testbbm = bowstat[6].text
        testecon = bowstat[7].text
        test5w = bowstat[10].text

        odiballs = bowstat[14].text
        odibruns = bowstat[15].text
        odiwickets = bowstat[16].text
        odibbi = bowstat[17].text
        odiecon = bowstat[19].text
        odi5w = bowstat[22].text

        tballs = bowstat[26].text
        tbruns = bowstat[27].text
        twickets = bowstat[28].text
        tbbi = bowstat[29].text
        tecon = bowstat[31].text
        t5w = bowstat[34].text

        data.append(f'Name: {name}')
        data.append(f'Country: {country}')
        data.append(f'Role: {role}')
        data.append("Matches Runs Highestscore Average StrikeRate 100s 50s")
        data.append(f'Test Batting: {testmatches} {testruns} {tesths} {testavg} {testsr} {test100} {test50}')
        data.append(f'ODI Batting: {odimatches} {odiruns} {odihs} {odiavg} {odisr} {odi100} {odi50}')
        data.append(f'T20 Batting: {tmatches} {truns} {ths} {tavg} {tsr} {t100} {t50}')
        data.append(f'Test Bowling: {testballs} {testbruns} {testwickets} {testbbi} {testbbm} {testecon} {test5w}')
        data.append(f'ODI Bowling: {odiballs} {odibruns} {odiwickets} {odibbi} {odiecon} {odi5w}')
        data.append(f'T20 Bowling: {tballs} {tbruns} {twickets} {tbbi} {tecon} {t5w}')
        data.append(f'Test Batting Ranking: {tb}')
        data.append(f'ODI Batting Ranking: {ob}')
        data.append(f'T20 Batting Ranking: {twb}')
        data.append(f'Test Bowling Ranking: {tbw}')
        data.append(f'ODI Bowling Ranking: {obw}')
        data.append(f'T20 Bowling Ranking: {twbw}')


        return render_template('predict.html', data=data)

    return render_template('upload.html', form=form)


app.run(host='0.0.0.0', port=8080)
