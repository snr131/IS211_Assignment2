"""
IS 211 Assignment 2 in Python 3
Sarah May
Start program by entering python assignment2.py into the command line
You will be prompted to enter a url, then you will be prompted to enter an id
"""
# importing modules
import argparse
import urllib3
import logging
import datetime

# this url was used to test this code
#url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'

def downloadData(url):
    birthday_list = []
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    data = "".join(map(chr,r.data))
    data = data.split('\n')
    for row in data:
        birthday_list.append(row.split(','))
    return birthday_list

# the csvData variable was used to test the downloadData function
#csvData = downloadData(url)


def processData(csvData):
    data_dict = {}
    for lst in csvData:
        try:
            id = int(lst[0])
            name = lst[1]
            birthday = datetime.datetime.strptime(lst[2], '%d/%m/%Y')
            birthday = birthday.strftime("%Y%m%d")
            data_dict[id] = (name, birthday)
        except Exception as e:
            logging.basicConfig(
                filename='errors.log',
                filemode='w',
                level=logging.ERROR,
                format='time: %(asctime)s,%(msecs)d level: %(levelname)-8s [%(filename)s, line:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d:%H:%M:%S'
                )
            logger = logging.getLogger('assignment2')
            logger.setLevel(logging.ERROR)
            logger.error(logging.error("Error processing ID {id}".format(id = lst[0])))
    return data_dict 

# the personData variable was used to test the processData function
#personData = processData(csvData)


def displayPerson(id, personData):
    display = personData.get(id, 'No user found with that id.')
    if id in personData:
        return "ID {id} belongs to {name} whose birthday is {birthday}.".format(id=id, name=display[0], birthday=display[1])
    else:
        return display

def main(url):
  print(f"Running main with URL = {url}...")
  return url


if __name__ == "__main__":
    # main entry point
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str)
    args = parser.parse_args()
    args.url = str(input('Enter the url\n'))
    main(args.url)
    csvData = downloadData(args.url)
    personData = processData(csvData)
    id = input('Enter an id number\n')
    answer = displayPerson((int(id)), personData)
    

if int(id) <= 0:
    print('Enter an id greater than 0')
else:
    print(answer)
