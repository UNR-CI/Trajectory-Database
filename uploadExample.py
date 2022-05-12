import requests 


def uploadCSV(url='http://134.197.75.31:30574/csv',filename='2021-12-8-17-0-0_cl.csv',location='Some Virginia Corner'): 
    files = {'files':open(filename,'rb')}
    requests.post(url+'?location='+location,files=files)

uploadCSV()