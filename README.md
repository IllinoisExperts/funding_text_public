# Funding Text to Bibliographic Note

## Description

This is a python program that takes in a csv file list of research outputs with funding text information from Pure and uses the Pure (CRUD) API to copy the funding information into the Bibliographic Note field. The purpose of this process is to improve the findability of funding information in Pure as "Bibliographic Note" is a searchable field while "Funding Text on Record" is not. 

**IMPORTANT**: This program is written to copy the information from the Funding Text field and **replace** whatever is in the Biblographic Note field with that information. If you have important information in the Bibliographic Note field that you would **not** like to overwrite, please do not use this program or modify it to your needs.

## What you need to get started

* main.py Python script

* API key for Production or Staging with read/write permissions for the Research Outputs endpoint (see Administrator > Pure API in the Pure admin interface)

* A __CSV__ file of research outputs with funding text. (This can be exported as an excel file from Pure--see below--and then re-saved in Excel as a CSV file.)

## A note on exporting from Pure

Each Research output's UUID must be included in the csv file. If the UUID is not included in the current export from Pure, navigate to Administrator > Export to Excel > Research outputs and add UUID to the export configuration (preferrably as the first column).

To export for initial update of existing Research outputes:

* In the Pure backend, navigate to Editor > Research outputs.
* Apply the filter "Funding information" (and select "Funding Text - With"--The program is not equipped to handle API responses that do not have funding text present and this will likely cause a fatal error).
* Apply the filter "Visibility" (select "public"--this program will throw a 404 error when attempting to read a restricted item)
* To reduce the potential for timeouts, it is also advisable to limit the size of the export to, e.g., one year's worth of data by applying the "Period" filter. (Depending on the number of outputs in your Pure instance, the program may be able to handle very large lists--up to over 10-20,000--but this will make the program take hours to complete and increases the risks of errors stopping the program before it can complete.)

To export for routine updates of Research outputs:

* In the Pure backend, navigate to Editor > Research outputs.
* Apply the filter "Funding information" (and select "Funding Text - With"--The program is not equipped to handle API responses that do not have funding text present and this will likely cause a fatal error).
* Apply the filter "Visibility" (select "public"--this program will throw a 404 error when attempting to read a restricted item)
* Apply the "Period" filter and enter a "Content created date" corresponding with the last run of this program.

## Dependencies

This program requires installing some external python packages. The packages you will need to install include:
* requests
* tqdm
* pandas

If you need helping installing these packages, the following guide may be useful: https://packaging.python.org/en/latest/tutorials/installing-packages/

Many Python IDEs also include convenient tools for installing packages. You can look for guides based on your specific IDE, such as this one for PyCharm: https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html

## How to Run

This program is composed of a single python script titled **"main.py"** 

To run the program, download "main.py" and run it from your integrated development environment (IDE). The program will walk you through the process of entering your API key and indicating file locations for the csv file of research outputs to be updated. 

To copy the file path from Windows file explorer in a format that is understandable to the program, right click on the file and select "Copy as path" (Keyboard shortcut CTRL+SHIFT+C) and then paste it into the program console. Make sure the file type extension is also included. The same can be done for folder locations by right clicking the folder name at the top address bar in file explorer and clicking "Copy address as text." Once you have entered a path, press ENTER and the program will automatically move to the next step. 

You will also need to input the URL for the Research Outputs endpoint for your instance of the Pure CRUD (read/write) API (this URL should include a final "/" e.g. https://experts.illinois.edu/ws/api/research-outputs/). (Please note that the URL will likely be different for the Staging and Production sides of your Pure instance, so be sure you are using the right one while testing the program in Staging to avoid making unwanted changes to the Production side. The API key should also be different, so that will reduce the risks of this happening.)

You will be asked to input the column header from your CSV file for the column that includes the unique UUID for each research output.

Finally, you will be asked to provide the file path for the folder that will hold the error logs once the program completes.

Once you have entered all of this information, the program will begin to read through the CSV file you indicated and make successive GET then PUT requests to copy the Funding Text information into the Bibliographic Note field. If there are no errors while making the requests, you will see the program output a message that the request went through along with the URL for the request. Otherwise, an error message will be printed and written to the error files. A progress bar will also update with each request visualizing the program's progress as it runs. 

## Contact Info

If you have questions or comments about using this program, you can contact the Illinois Experts team at experts-help@illinois.edu

