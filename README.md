# Brief Explanation.

This API has been designed with the database primary key on the record number for autoincrement as **Create** is done at the client end 
hence lawyers can make entries with no error response of duplicate entry for a desgin based on employeeIDs primary key.<br><br>
*Multiple timesheets or records created by a lawyer.*

# App Prepworks <br>
**Server-Side package:**<br>
Database: sqlite, comes pre-installed on ubuntu<br>
ORM: pip install -U Flask-SQLAlchemy<br>
Web Framework: pip install Flask<br>

**Database setup:**<br>
1. Enter the terminal: ( Ctrl + Alt + T)
2. Enter python interpreter:  python3 
3. Run commands
```
>>> from yourapplication import db
>>> db.create_all()
>>> exit()
```
*yourapplication = filename.py, for this assignment, filename = app*

## Run App <br>
1. Enter the terminal: ( Ctrl + Alt + T)
2. Run command: python3 filename.py

## NOTE:<br>
Test API endpoints with the tool Postman(prefered) / cURL / Chrome Developer tools <br>
**form-data** HTTP Request is friendly with Postman.

# API Docs

 ## C: Create<br>
 **HTTP METHOD := POST**<br>
 A lawyer can create multiple timesheets(records) on PROMPT<br>
 **Endpoint:**
 http://localhost/create-timesheet<br>
 **Body:**<br>
 **form-data:**<br>
 {<br>
 employeeID *Integer* <br>
 billableRate *Integer* <br>
 company *String* <br>
 date *Text* <br>
 startTime *Text* <br>
 endTime *Text* <br>
 }
 <br>


## R: Read <br>
**HTTP METHOD := GET** <br>
A lawyer can read or view timesheet(s) <br>
**Query Params:**<br>
employeeID *Integer*<br>
**Endpoint:**
http://localhost/view-timesheet?employeeID=2

## U: Update<br>
**HTTP METHOD := PUT** <br>
A lawyer can update timesheet entries. <br>
**Query Params:**<br>
employeeID *Integer*<br>
record_number *Integer*<br>
**Endpoint:**
http://localhost/update-timesheet?employeeID=1&record_number=2<br>
**Body:**<br>
 **form-data:**<br>
 {<br>
 billableRate *Integer* <br>
 company *String* <br>
 date *Text* <br>
 startTime *Text* <br>
 endTime *Text* <br>
 }


## D: Delete <br>
**HTTP METHOD := DELETE** <br>
A lawyer can delete timesheet(s)<br>
**Query Params:**<br>
employeeID *Integer*<br>
record_number *Integer*<br>
**Endpoint:**
http://localhost/delete-timesheet?employeeID=1&record_number=2

## Generate-Invoice<br>
**HTTP METHOD := GET** <br>
Finance team generate invoice for each client or company.<br>
**Query Params:**<br>
company *String*<br>
**Endpoint:**
http://localhost/generate-invoice?company=entercompanyhere<br>
*entercompanyhere = Arch Services, Power, MTN, Tigo, Ecobank*




