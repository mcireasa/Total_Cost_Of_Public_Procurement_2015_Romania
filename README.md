# Total_Cost_Of_Public_Procurement_2015_Romania
Small Python project that uses API requests to retrieve the data about public procurement in Romania in 2015.


The project retrieves data from [Data Gov](https://data.gov.ro/dataset/achizitii-publice-2010-2015-anunturi-de-participare/resource/9e0f19f1-b4ce-4f27-b5ec-6f644145e7f3)  in CSV format using the [urrlib](https://docs.python.org/3/library/urllib.html) library.
The data is then formatted and the total cost of acquisitions per County is inserted in an dictionary that has **County_Name:Total_Acquisitions** as **key:value** pairs. The values from the dictionary are then saved in a CSV file having the header **County,Total_Cost**.
The program than goes to also calculate the total cost of acquisitions for each month and then save this data in a JSON file using a **json** object.
The user has also the ability to use a Convertor in which he can insert the sum and the currency from which he wants to make the transformation to RON. The exchange rates are from the official [BNR site](https://www.bnr.ro/nbrfxrates.xml) and always up to date. The program uses [bs4](https://pypi.org/project/beautifulsoup4/) library to create a web scrapper that will get the exchange rates. 
Finally, the program can also update the values to RON from the CSV that keeps data about total cost of acquisitions per County. This was implemented because the data from the BNR website gives values both in RON and EUR. 
