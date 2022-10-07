 

import requests,json,argparse,openpyxl 

headers={'Authorization':'cpanel USERNAME:APITOKEN'} 

parser = argparse.ArgumentParser() 

parser.add_argument("-f","--file", help="excel file to read", required=True) 

parser.add_argument("-o","--output", help="file to write errors and results", default="errorslogs.txt", required=False) 

args = parser.parse_args() 

def main(): 

    # Define variable to load the wookbook 
    wookbook = openpyxl.load_workbook(args.file) 

    # Define variable to read the active sheet: 
    worksheet = wookbook.active 

    with open(args.output, "w", encoding='utf8') as file1: 

        for row in wookbook.worksheets[0].iter_rows(min_row = 2, max_row = worksheet.max_row, max_col = 3): 
            email = row[0].value 
            domain = row[1].value 
            passwd = row[2].value 

            if (email and passwd and domain) is not None:
                result = updatepassword(str(email),str(passwd),str(domain)) 
                file1.write(str(bool(result['status']))+"\t"+result['errors']+"\n")
              
                print(result['status'],end='\t') 
                print(result['errors'],end='\n') 

 

def updatepassword(email,password,domain): 

    url="https://example.com:2083/execute/Email/passwd_pop?email={}&password={}&domain={}".format(email,password,domain) 

    resp = requests.get(url,headers=headers) 

    # Decode UTF-8 bytes to Unicode, and convert single quotes  

    # to double quotes to make it valid JSON 

    my_json = resp.content.decode('utf8').replace("'", '"') 

    # Load the JSON to a Python list & dump it back out as formatted JSON 

    data = json.loads(my_json) 

    #record the result 

    resultat={'status':data['status']} 

    if not data['errors']: 

        resultat['errors']="null" 

    else: 

        resultat['errors']=data['errors'][0] 

    #return the result 

    return resultat 

 

if (__name__=="__main__"): 

    main() 
