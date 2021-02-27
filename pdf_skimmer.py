# import packages
import PyPDF2
import re, os, glob, time
from csv import DictWriter 

#Initialize Variables
matchList = []
field_names = ['name','match','lines', 'error'] 
element = {"name": "", 'match': False, "lines": [], 'error': False }

#Directory Handling
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
Source_DIR = f'{ROOT_DIR}\\pdfs_toscan\\'
Match_Destination_DIR = f'{ROOT_DIR}\\match\\'
NoMatch_Destination_DIR = f'{ROOT_DIR}\\no_match\\'
Error_Destination_DIR = f'{ROOT_DIR}\\errors\\'

# define keyterms
keyWords = ["C\+\+" ,"python" ,"ROS", "web", "javascript", "react" ,"angular", "unity", "js"]
file_list = glob.glob(f"{Source_DIR}\*.pdf")

Enable_Sort = input('Sort Pdfs to folder? (y/n)')

for file in file_list:
    #reset working vars
    file_name = file.split("\\")
    element['name'] = None
    element['lines'] = []
    error = False
    match = False
    print(file)

    # open the pdf file
    try:
        object = PyPDF2.PdfFileReader(f"{file}")
    except Exception as e:
        print(e)
        error = True

    # get number of pages
    if error != True:
        try:
            NumPages = object.getNumPages()
        except Exception as e:
            print(e)
            error = True

    element['name'] = file

    # extract text and do the search
    if error != True:
        for i in range(0, NumPages):
            page = object.getPage(i)
            text = page.extractText()
            for line in text.splitlines():
                for x in keyWords:
                    if re.match(x, line):
                        match = True
                        element['lines'] += [line]

    
    element['match'] = match
    element['error'] = error
    print(element)

    if(Enable_Sort == "y"):
        if not os.path.exists(Error_Destination_DIR):
            os.makedirs(Error_Destination_DIR)
        if not os.path.exists(Match_Destination_DIR):
            os.makedirs(Match_Destination_DIR)
        if not os.path.exists(NoMatch_Destination_DIR):
            os.makedirs(NoMatch_Destination_DIR)

        if (error):
            os.replace(file, f'{Error_Destination_DIR}{file_name[-1]}')
        elif(match):
            os.replace(file, f'{Match_Destination_DIR}{file_name[-1]}')
        else:
            os.replace(file, f'{NoMatch_Destination_DIR}{file_name[-1]}')

    # Open your CSV file in append mode 
    # Create a file object for this file 
    with open('list.csv', 'a', newline='') as f_object: 
        
        # Pass the file object and a list  
        # of column names to DictWriter() 
        # You will get a object of DictWriter 
        dictwriter_object = DictWriter(f_object, fieldnames=field_names) 
    
        #Pass the dictionary as an argument to the Writerow() 
        dictwriter_object.writerow(element) 
    
        #Close the file object 
        f_object.close()




   
    