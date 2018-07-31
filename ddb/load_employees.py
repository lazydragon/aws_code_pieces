from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
import csv
import sys

def import_csv(tableName, fileName):
    dynamodb = boto3.resource('dynamodb')
    dynamodb_table = dynamodb.Table(tableName)
    count = 0

    time1 = time.time()
    with open(fileName, 'rb') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            count += 1
            newEmployee = {}
            if len(row) == 10:
                newEmployee['employeeid'] = int(row[0])
                newEmployee['colA']  = 'master'
                newEmployee['name'] = row[1]
                newEmployee['title'] = row[2]
                newEmployee['dept'] = row[3]
                newEmployee['city'] = row[4]
                newEmployee['state'] = row[5]
                newEmployee['city_dept'] = row[4] + ':' + row[3]
                newEmployee['dob'] = row[6]
                newEmployee['hire_date'] = row[7]
                newEmployee['previous_title'] = row[8]
                newEmployee['previous_title_end'] = row[9]
                newEmployee['lock']  = '0'
            else:
                newEmployee['employeeid'] = int(row[0])
                newEmployee['colA']  = 'master'
                newEmployee['name'] = row[1]
                newEmployee['title'] = row[2]
                newEmployee['dept'] = row[3]
                newEmployee['city'] = row[4]
                newEmployee['state'] = row[5]
                newEmployee['city_dept'] = row[4] + ':' + row[3]
                newEmployee['dob'] = row[6]
                newEmployee['hire_date'] = row[7]
                newEmployee['previous_title'] = row[8]
                newEmployee['previous_title_end'] = row[9]
                newEmployee['is_manager'] = row[10]
                newEmployee['lock']  = '0'

            item = dynamodb_table.put_item(Item=newEmployee)

            newCurrentTitle = {}
            newCurrentTitle['employeeid'] = newEmployee['employeeid']
            newCurrentTitle['colA'] = 'current_title:' + newEmployee['title']
            newCurrentTitle['name'] = newEmployee['name']
            newCurrentTitle['hire_date'] = newEmployee['previous_title_end']
            item = dynamodb_table.put_item(Item=newCurrentTitle)

            newPreviousTitle = {}
            newPreviousTitle['employeeid'] = newEmployee['employeeid']
            newPreviousTitle['colA'] = 'previous_title:' + newEmployee['previous_title']
            newPreviousTitle['name'] = newEmployee['name']
            newPreviousTitle['hire_date'] = newEmployee['hire_date']
            item = dynamodb_table.put_item(Item=newPreviousTitle)

            newLocation = {}
            newLocation['employeeid'] = newEmployee['employeeid']
            newLocation['colA'] = 'state:' + newEmployee['state']
            newLocation['name'] = newEmployee['name']
            newLocation['hire_date'] = newEmployee['hire_date']
            newLocation['city_dept'] = newEmployee['city_dept']

            item = dynamodb_table.put_item(Item=newLocation)

            if count % 100 == 0:
                time2 = time.time() - time1
                print("employee count: %s in %s" % (count, time2))
                time1 = time.time()
    return count

if __name__ == "__main__":
    args = sys.argv[1:]
    tableName = args[0]
    fileName = args[1]

    begin_time = time.time()
    count = import_csv(tableName, fileName)

    # print summary
    print('RowCount: %s, Total seconds: %s' %(count, (time.time() - begin_time)))
