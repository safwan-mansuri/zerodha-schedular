from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests_html import HTML,HTMLSession
import pandas, numpy, json, requests, zipfile, io
from .constants import BSEINDIA, BACKEND_API
import logging

logging.basicConfig(level=logging.DEBUG)

equity_data = []

def getLink() :
  try: 
    logging.info('getLink entry point .......')
    with requests.Session() as s :
      session = HTMLSession()
      r = session.get(BSEINDIA)
      soup = BeautifulSoup(r.content, 'html.parser')
    
    containers = soup.find_all('a',{'id':'ContentPlaceHolder1_btnhylZip'})

    return containers[0]['href']
  except Exception as e :
    logging.error('cant get the link from the bse website', str(e))


def downloadData(link) :
  try: 
    logging.info('downloadData entry point ......')
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'origin': 'https://www.bseindia.com',
    'referer': 'https://www.bseindia.com/'
    }
    r = requests.get(link, headers=headers)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("./equity-datas")

    return z.namelist()[0]
  except Exception as e:
    logging.error('cant download the data', str(e))


def sendData(filename) :
  try:
    logging.info('sendData entry point .....')
    url = BACKEND_API
    headers = {}
    data = json.dumps({
      "data": equity_data
    })

    fullDate = filename.split('.')[0][2:]
    date = f'{fullDate[0:2]}-{fullDate[2:4]}-{fullDate[4:6]}'

    requests.post(url, data={'equity': data, 'date': date})
  except Exception as e:
    logging.error('cannot send data to the backend service', str(e))

def startProcess() :
  try: 
    logging.info('startProcess entry point .......')
    link = getLink()
    filename = downloadData(link)
    data = numpy.array(pandas.read_csv('./equity-datas/' + filename))
    for rows in data :
      equity_data.append(json.dumps({
        "code": rows[0], 
        "name": rows[1].strip(), 
        "open": rows[4], 
        "high": rows[5], 
        "low": rows[6], 
        "close": rows[7]
      }))  
    sendData(filename)
    equity_data.clear()
  except Exception as e:
    logging.error('cannot start the process', str(e))

  
  
  return True
