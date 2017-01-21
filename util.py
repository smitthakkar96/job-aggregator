def getJobObjectFromIndeedResponse(object):
    return {
        'jobTitle' : object['jobtitle'],
        'active' : object['expired'],
        'sponsored' : object['sponsored'],
        'location' : object['formattedLocationFull'],
        'company' : object['company'],
        'state' : object['state'],
        'date' : object['date'],
        'description' : object['snippet'],
        'source' : 'Indeed',
        'detailUrl' : object['url']
    }

def getJobObjectFromDiceResponse(object):
    return {
        'jobTitle' : object["jobTitle"],
        'active' : True,
        'sponsored' : False,
        'location' : object["location"],
        'company' : object["company"],
        'state' : '',
        'date' : object["date"],
        'description' :  '',
        'source' : 'DICE'
    }