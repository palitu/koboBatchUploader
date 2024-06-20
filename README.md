# koboBatchUploader
Script to easily upload bulk data to https://www.kobotoolbox.org/.  it takes a properly formatted csv and uploads it to a form that you have access to.

It takes a csv file, which has the top row as the column names, and these MUST align with columns in your database/form.  

 - `Column name` - where you have ungrouped columns.
 - `group name` `/` `column name` - these columns are where a column is within a group in the form.  it will only go down one level, so if you have groups in groups, it will not work.  The `/` is the divider between groups and column names.
 - `remove` `/` `description` - these columns are used to have working data in the csv, that will not be uploaded.  
Where you have groups, you need to prefix the column name with the group name, and seperate it with a `/`

you **MUST** have the `meta/instanceID` column in the csv  and it **MUST** be created from a legitimate UUID.  you can generate UUIDs within libreoffice Calc with the following formula:

```
=LOWER(CONCATENATE(DEC2HEX(RANDBETWEEN(0,4294967295),8),"-",DEC2HEX(RANDBETWEEN(0,65535),4),"-",DEC2HEX(RANDBETWEEN(0,65535),4),"-",DEC2HEX(RANDBETWEEN(0,65535),4),"-",DEC2HEX(RANDBETWEEN(0,4294967295),8),DEC2HEX(RANDBETWEEN(0,65535),4)))
```


# Features
- [x] handles single level groups
- [x] fetches a list of forms you are able to upload to
- [x] dynamic selection of list to upload to.
- [x] de-duplicates data submissions, based on the UUID that you generate in the csv.

**It does not have**
- [ ] handles multi level groups
- [ ] data validation(!!)


# Contributing
If you would like to contribute, i am happy to review. Maybe stick a comment into the issues firsts. Also note that i am a novice programmer (as you can see :D), so my ability to determine good quality code is limited, apart from seeing that my code is sunny-day, and has limited/no error handling.