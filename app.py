from flask import Flask, request, jsonify
from indeed import IndeedClient
import requests
from geopy.geocoders import Nominatim

import util

app = Flask(__name__)
indeedClient = IndeedClient(publisher = "7632764340078951")



@app.route('/api/jobs', methods = ['GET'])
def jobs():
    """
    USE THIS ENDPOINT TO AGGREGATE JOBS FROM DIFFERENT PLATFORMS
    """

    # Indeed Search
    payloadForIndeed = {
        'userip' : "0.0.0.0",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
    }
    keyword = request.args.get('q')
    if keyword is None:
        return jsonify({'error' : 'keyword is mandatory'}), 400
    payloadForIndeed['q'] = keyword
    jobType = request.args.get('jobType')
    if jobType:
        payloadForIndeed['jt'] = jobType
    experience = request.args.get('Experience')
    if experience:
        minExperience, maxExprience = experience.split(',')
    company = request.args.get('company')
    applicationStatus = request.args.get('applicationStatus')
    location = request.args.get('location')
    if location:
        payloadForIndeed['l'] = location
    sort = request.args.get('sort')
    page = request.args.get('page', 1)
    if sort in ['relevance', 'date']:
        payloadForIndeed['sort'] = sort
    start = (int(page) - 1) * 25
    payloadForIndeed['limit'] = 25
    payloadForIndeed['start'] = start
    indeedResult = indeedClient.search(**payloadForIndeed)

    # Dice Search
    payloadForDice = {}
    payloadForDice['skill'] = keyword
    if location:
        payloadForDice['city'] = location
    payloadForDice['pgcnt'] = 25
    payloadForDice['page'] = start
    if sort:
        sortMappings = {
            'relevance' : 0,
            'date' : 1,
            'name' : 2,
            'location' : 4
        }
        try:
            payloadForDice['sort'] = sortMappings[sort]
        except:
            return jsonify({'error' : 'Please Specify sort field either relevance, date, name or location'})

    diceResponse = requests.get('http://service.dice.com/api/rest/jobsearch/v1/simple.json', params = payloadForDice)
    diceResponse = diceResponse.json()

    indeedJobs = list(map(util.getJobObjectFromIndeedResponse, indeedResult['results']))
    diceJobs = list(map(util.getJobObjectFromDiceResponse, diceResponse['resultItemList']))
    jobs = indeedJobs + diceJobs

    if company:
        jobs = list(filter(lambda job: job['company'] == company, jobs))

    return jsonify({'response' : {
        'data' : jobs
    }})


if __name__ == '__main__':
    app.run(debug = True)