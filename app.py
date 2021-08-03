# This a Billable Rate System for Quantum Legal Firm for their lawyers to Create timesheets,
# View, Update and Delete timesheets.
# Also has a functionality for the finance department to generate invoice.

# Date started: 30th July 2021.
# Date ended: 3rd August 2021.
# written with love by Sammy or Samuel Brifo



# let's connect to the web over http = [POST,GET, PUT, DELETE] with the help of a friend FLASK
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json

# @@DONE: TODO: config app to talk with database to hold data for client submission
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"clientdatabase.db"))

# alright, let us introduce our friend
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # suppress sqlalchemy track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app) # introduce app to SQLALCHEMY ORM



# Client Model
class Client(db.Model):
    recordID = db.Column(db.Integer, primary_key=True,nullable=False)
    employeeID = db.Column(db.Integer,nullable=False)
    billableRate = db.Column(db.Integer,nullable=False)
    company = db.Column(db.String(50),nullable=False)
    date = db.Column(db.Text,nullable=False)
    startTime = db.Column(db.Text,nullable=False)
    endTime = db.Column(db.Text,nullable=False)

    # custom defined toJson Parser for this use case of a several lawyers working with more than one client hence primary key autoincrement is to the recordID
    # to allow N lawyers Create timesheet of their own ID number yet record ID is of system generated.
    def toJson(object):
        # get list of objects
        clientJson = {}
        # for single client record.
        if(len(object) == 1):
            # create dictionary dynamically.
            clientJson = dict(record_number=object[0].recordID,
                     employeeID=object[0].employeeID,
                     billableRate=object[0].billableRate,
                     company=object[0].company,
                     date=object[0].date,
                     startTime=object[0].startTime,
                     endTime=object[0].endTime)
            return clientJson

        # for multiple client record
        if (len(object) > 1):
            clientlistJson = []
            for i in range(len(object)):
                ##DONE @@TODO: implement a dictionary dynamically from a list.
                clientJsonDict = dict(record_number=object[i].recordID, employeeID=object[i].employeeID,
                                  billableRate=object[i].billableRate,
                                  company=object[i].company,
                                  date=object[i].date,
                                  startTime=object[i].startTime,
                                  endTime=object[i].endTime)
                clientlistJson.append(clientJsonDict)
            return clientlistJson # return clientListJson





# lawyers have to create a timesheets.
@app.route('/create-timesheet', methods=['POST']) # friend handles POST request to web
def createTimeSheet():

    employeeID = request.form['employeeID'] # submit employeeID
    billableRate = request.form['billableRate'] # submit billableRate
    company = request.form['company'] # submit company
    date = request.form['date'] # submit date
    startTime = request.form['startTime'] # submit time started
    endTime = request.form['endTime'] # sumbit end time
    clientDetails = [employeeID,billableRate,company, date,startTime, endTime] # alright, all client details kept neat in tidy
    # @@TODO: return clientDetails in a more dynamic form as to string for further processing.

    client = Client(employeeID=employeeID, billableRate=billableRate,company=company,
                    date=date,startTime=startTime,endTime=endTime) # pass data from lawyer to Client Model
    db.session.add(client) # session -> clientdatabase.db
    db.session.commit() # commit to clientdatabase.db
    return 'Data passed to clientdatabase.db'
   # return 'TimeSheet Created:\n' +  'Details:' + str(clientDetails) # return data captured.

#R: Read
# lawyers would like to view timesheets
@app.route('/view-timesheet', methods=['GET']) # our friend handles the request: GET
def viewTimeSheet():
    employeeID = request.args['employeeID'] # get employeeID entered
    employeeClients = Client.query.filter_by(employeeID=employeeID).all() # query clients of employeeID
    return jsonify(Client.toJson(employeeClients))




#U: Update
# Lawyers update by passing the record_number they want to work with.
# lwayers would like to update their timesheets
@app.route('/update-timesheet', methods=['PUT'])
def updateTimeSheet():
    employeeID = request.args['employeeID'] # get employeeID
    recordNumber = request.args['record_number'] # get record number of client
    # if there exist a record for that employeeID then update the fields
    recordPattern = "record_number#" + recordNumber
    clientList  = Client.query.filter_by(employeeID=employeeID).all() # query clients of employeeID

    record = Client.toJson(clientList)
    theRecord = [] # for no record found, the list is empty
    # scan through the list and find the record number
    for i in range(len(record)):
      if recordPattern in record[i]:
          theRecord = record[i] # save the found record
          break # stop searching

    if theRecord is not []: # if the record is found
        # then we update
        billableRate = request.form['billableRate']  # submit billableRate
        company = request.form['company']  # submit company
        date = request.form['date']  # submit date
        startTime = request.form['startTime']  # submit time started
        endTime = request.form['endTime']  # sumbit end time

        # @DONE:TODO: implement update for primary key based record_number
        theUpdateClient = db.session.query(Client).get(recordNumber)

        theUpdateClient.billableRate = billableRate
        theUpdateClient.company = company
        theUpdateClient.date = date
        theUpdateClient.startTime = startTime
        theUpdateClient.endTime = endTime

         # commit changes
        db.session.commit()
        return "record_number#" + recordNumber + "updated."


    #return '<h1>Update TimeSheet</h1>'

#D: Delete
# lawyers would like to delete their timesheets
@app.route('/delete-timesheet', methods=['DELETE'])
def deleteTimeSheet():
    employeeID = request.args['employeeID']  # get employeeID
    recordNumber = request.args['record_number']  # get record number of client

    # if there exist a record for that employeeID then update the fields
    recordPattern = "record_number#" + recordNumber
    clientList = Client.query.filter_by(employeeID=employeeID).all()  # query clients of employeeID

    record = Client.toJson(clientList)
    theRecord = []  # for no record found, the list is empty
    # scan through the list and find the record number
    for i in range(len(record)):
        if recordPattern in record[i]:
            theRecord = record[i]  # save the found record
            break  # stop searching

    if theRecord is not []:  # if the record is found
        theDeleteClient = db.session.query(Client).get(recordNumber)
        # return str(theDeleteClient)
        db.session.delete(theDeleteClient)
        db.session.commit()
        return "record_number#" + recordNumber + "deleted."
    else:
        return "no record to delete"



# INVOICE GENERATION
# finance company generates invoices for each client queried
@app.route('/generate-invoice/', methods=['GET'])
def generateInvoice():
    company = request.args['company'] # get the client or company name from the query string

    #@@TODO: Generate Invoice
    # for the company queried, retrieve all records
    allRecords = Client.query.filter_by(company=company).all()
    record = Client.toJson(allRecords)
    #return jsonify(record) # debug the records for that company


    employeeIDs = []
    numberOfHours = []
    unitPrice = []
    cost = []

    # loop through the records of that company
    for i in range(len(record)):

        # save all employeeIDs from the record
        employeeIDs.append(record[i]["employeeID"])

        # get number of hours
        endTime = record[i]["endTime"].split(":")
        startTime = record[i]["startTime"].split(":")

        endTimeHours = endTime[0]
        endTimeMinutes = endTime[1]

        startTimeHours = startTime[0]
        endTimeMinutes = endTime[1]

        # the number of hours
        calculatedNumberOfHours = int(endTimeHours) - int(startTimeHours)

        numberOfHours.append(calculatedNumberOfHours) # save the number hours spent

        # unit price
        unitPrice.append(record[i]["billableRate"])  # save all billable rate
        totalUnitPrice = sum(unitPrice) # total unit price
        # calculate cost = billablerate * number of hours
        calculateCost = calculatedNumberOfHours * record[i]["billableRate"]
        cost.append(calculateCost) # save all the cost
        totalCost = sum(cost) # total cost

    # generate invoice
    invoice = {
        "1": {"Company":company},
        "2": {"EmployeeIDs":employeeIDs},
        "3": {"NumberOfHours": numberOfHours},
        "4": {"UnitPrice":unitPrice},
        "5": {"Cost":cost},
        "6": {"Total": totalCost}
    }

    return invoice # invoice generated is ready.


# run flask app
if __name__ == "__main__":
    app.run(debug=True)