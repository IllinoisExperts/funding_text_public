# Funding Text to Bibliographic Note

## Description

This is a python program that takes in a csv file list of research outputs with funding text information from Pure and uses the Pure (CRUD) API to copy the funding information into the Bibliographic Note field. The purpose of this process is to improve the findability of funding information in Pure as "Bibliographic Note" is a searchable field while "Funding Text" is not. 

**IMPORTANT**: This program is written to copy the information from the Funding Text field and **replace** whatever is in the Biblographic Note field with that information. If you have important information in the Bibliographic Note field that you would **not** like to overwrite, please do not use this program or modify it to your needs.
## How to Run

This program is composed of a single python script titled **"main.py"** 

To run the program, download "main.py" and run it from your IDE. The program will walk you through the process of entering your API key and indicating file locations for the csv file of research outputs to be updated. 

You will also need to input the URL for the Research Outputs endpoint for your instance of the Pure CRUD (read/write) API (this URL should include a final "/" e.g. "https://experts.illinois.edu/ws/api/research-outputs/" without the quotation marks).

Finally, you will be asked to input the column header from your CSV file for the column that includes the unique UUID for each research output. 

Once you have entered all of this information, the program will begin to read through the CSV file you indicated and make successive GET then PUT requests to copy the Funding Text information into the Bibliographic Note field. If there are no errors while making the requests, you will see the program output a message that the request went through along with the URL for the request. Otherwise, an error message will be printed and written to the error files. A progress bar will also update with each request visualizing the program's progress as it runs. 

## What you need to get started

* A __CSV__ file of research outputs with funding text. This can be downloaded as an excel file from Pure and then re-saved in Excel as a CSV file. Before exporting the list, please be sure that you have filtered your research outputs to ensure that all have Funding Text and that all are publicly visible. The program is not equipped to handle API responses that do not have funding text present and this will likely cause a fatal error. Additionally, you might consider filtering by dates of publication or creation in order to complete this process in batches. Depending on the number of outputs in your Pure instance, the program may be able to handle very large lists (up to over 10-20,000) but this will make the program take hours to complete and increases the risks of errors stopping the program before it can complete. 
* main.py Python script
* API key for Production or Staging (with read/write permissions)

## Dependencies

This program requires installing some external python packages. The packages you will need to install through your IDE include:
* requests
* tqdm
* pandas
