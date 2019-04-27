This is the README of the project which include basic instruction of how to use it.

This Project is Prepared by Hank Du (WatIAm:r23du, StudentID:20752443) and Zhaoyang Cui (WhatIAm:z45cui, studentID:20781133)

# Set up
```console
mysql -u root -p < lahman2016.sql
```

# Cleaning Data:
The parameters are *commit* (True/False) which indicates whether commit the change to database after data cleaning process or not.
The parameter is *period* which is what period of time that player was inducted do you want to analyze. Specify the 4-digits year number, the analyzed data would be prior this year.
*Note: If there is any clean up issue, server will provide user possible solution and user will be able to choose it*

# Analyzing Data:
There is no parameter for this function.

# Validating Data:
There is no parameter for this function.

# Reverting Database:
You might need to enter password on server side to perform full revert

The server will analyze data use model built by Analyzing data and use rest of year data to validate it.
