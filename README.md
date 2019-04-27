This is the README of the project which include basic instruction of how to use it.

This Project is Prepared by Hank Du (WatIAm:r23du, StudentID:20752443) and Zhaoyang Cui (WhatIAm:z45cui, studentID:20781133)

# Set up
This script will install all the required dependencies to a virtual environ ment and execute both server and client application
```console
chmod +x setup
./setup
```
# Executing
It is suggested to use two separate window to execute client and server application. Then just following the instruction to complete data mining.
```console
python server.py
python client.py
```

## Cleaning Data:
The parameters are *commit* (True/False) which indicates whether commit the change to database after data cleaning process or not.
The parameter is *period* which is what period of time that player was inducted do you want to analyze. Specify the 4-digits year number, the analyzed data would be prior this year.
*Note: If there is any clean up issue, server will provide user possible solution and user will be able to choose it*

## Analyzing Data:
There is no parameter for this function.

## Validating Data:
There is no parameter for this function.

## Reverting Database:
You might need to enter password on server side to perform full revert

The server will analyze data use model built by Analyzing data and use rest of year data to validate it.

# Database
The Default username and password are both set to 'root', if there is a different name or password, please update it in server.py
