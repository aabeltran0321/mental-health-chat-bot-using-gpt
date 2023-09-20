from gpt_wrapper import GPTAPI

# Change API Key if needed
GPT_API = GPTAPI(api_key="YOUR-OPENAI-API-KEY-HERE")

def converse_gpt(input_text = "", system_rules = ""):
    output = GPT_API.chat_output_text_only(input_text,system_rules)
    success = not(output=='error')

    return success, {'text': output}
def converse_gpt2(input_text: str):
    output = GPT_API.text_output_text_only(input_text)
    success = not(output=='error')

    return success, {'text': output}

def get_overview_with_name_loc(c_name: str, loc: str):
    system_rules = "Complete and recreate these sentences from the data of %s from %s:" % (c_name,loc)
    input_text = '''Its website is: 
    Its Email Address is:
    This company is engaged in <Primary Business Line>.
    The company was (incorporated, founded, established, started) in <Establishment Year>.
    It was (founded by; established by; a joint venture of) <History>.
    The company specialises in <specific products/activities>. 
    It also operates branch/es in <countries; cities; region>.
    Its products are sold and distributed in domestic market as well as overseas including <countries; cities; region>.
    The company is <one of the leading; the leader> distributor of <products/services> in the domestic market and overseas. 
    Its <mission is to; is committed to; aims to>.
    The company <establishes partnership with; partners with>. 
    It serves customer including <companies>. 
    The company <operates as part of; operates as a subsidiary of; is wholly owned by>.
    The company specialises in <specific products> under <brand names; trademarks>.
    '''

    success, gpt_output = converse_gpt(input_text,system_rules)
    #success = False
    if success:
        output_json = {}
        data = gpt_output['text'].splitlines()

        overview = data[2].replace("\n","") +" "
        if overview[0]=="-":
            overview = overview[2:]
        overview = overview.replace("    ", "")
        overview += f"It conducts business from its registered head office located in {loc}. "
        for a in range(3,len(data)):
            txt = data[a].replace("\n","")
            
            
            if txt[0]=="-":
                txt = txt[2:]
            txt = txt.replace("    ", "")
            overview += txt
            overview += " "

        output_json["Overview"] = overview[:-1]
        with open("fields.txt", "r") as f:
            lines = f.readlines()
            for i,kk in enumerate(lines):
                if i<2:
                    output_json[lines[i].replace("\n","")] = data[i].split(": ")[1]
                elif i==3:
                    output_json[lines[i].replace("\n","")] = data[i][-5:-1]
                else:
                    str1 = data[i]
                    str1 = str1.replace("    ", "")
                    str1 = str1.replace("- ", "")
                    output_json[lines[i].replace("\n","")] = str1
                #print(output_json[lines[i].replace("\n","")])
            f.close()
        return success,output_json
    #else:
    dict1 = {}
    dict1['Overview'] = "GPT was not able to process data from the provided link"
    with open("fields.txt", "r") as f:
        lines = f.readlines()
        for ii in lines:
            dict1[ii.replace("\n","")] = ""
    return success,dict1
    
    # Getting the data for JSON format
    # fields_data = gpt_output['text'].replace("\n\n","\n").splitlines()
    

    # if len(fields_data)>1:
    #     #creating overview
    #     overview = fields_data[2].replace("\n","") +" "
    #     if overview[0]=="-":
    #         overview = overview[2:]
    #     overview += f"It conducts business from its registered head office located in {loc}. "
    #     for a in range(3,len(fields_data)):
    #         txt = fields_data[a].replace("\n","")
    #         if txt[0]=="-":
    #             txt = txt[2:]
    #         overview += txt
    #         overview += " "
        
    #     #print(overview)
        
    #     output = {}

    #     output["Overview"] = overview

    #     #JSON keys
    #     with open("fields.txt", "r") as f:
    #         lines = f.readlines()
    #         # Creating the JSON output
    #         for i,k in enumerate(fields_data):
                
    #             data = k.replace("\n","")
    #             if data[0]=="-":
    #                 data = data[2:]
    #             data = data.replace("Its website is: ","")
    #             data = data.replace("Its Email Address is: ","")
    #             if "Establishment year" in lines[i]:
    #                 output[lines[i].replace("\n","")] = data[-5:-1]
    #             else:
    #                 output[lines[i].replace("\n","")] = data

    #         f.close()
    #     #print(output)
    #     return success,output
    # else:
    #     return False,{"text":"error"}

def translation_to_english(text: str):
    input_text = f'translate this to english:\n' \
                 f'{text}'
    
    return converse_gpt(input_text=input_text)

def keyword_extraction(text: str):
    input_text = f'extract important keywords:\n' \
                 f'{text}'
    
    return converse_gpt(input_text=input_text)
def translation(language: str, text: str):
    input_text = f'translate this to {language}:\n' \
                 f'{text}'
    
    return converse_gpt(input_text=input_text)

def Scraping_v2(link: str):
    input_text = '''Complete and recreate these sentences from this link: %s:
    Its website is 
    Its Email Address is
    This company is engaged in <Primary Business Line>.
    The company was (incorporated, founded, established, started) in <Establishment Year>.
    It was (founded by; established by; a joint venture of) <History>.
    The company specialises in <specific products/activities>. 
    It also operates branch/es in <countries; cities; region>.
    Its products are sold and distributed in domestic market as well as overseas including <countries; cities; region>.
    The company is <one of the leading; the leader> distributor of <products/services> in the domestic market and overseas. 
    Its <mission is to; is committed to; aims to>.
    The company <establishes partnership with; partners with>. 
    It serves customer including <companies>. 
    The company <operates as part of; operates as a subsidiary of; is wholly owned by>.
    The company specialises in <specific products> under <brand names; trademarks>.
    It conducts business from its registered head office located in'''

    #return converse_gpt2(input_text=input_text % (link))

    success, gpt_output = converse_gpt2(input_text=input_text % (link))
    
    # Getting the data for JSON format
    fields_data = gpt_output['text'].replace("\n\n","\n").splitlines()

    if len(fields_data)>1:
        #creating overview
        overview = fields_data[3].replace("\n","") +" "
        overview += fields_data[len(fields_data)-1].replace("\n","") +" "
        for a in range(3,len(fields_data)-1):
            overview += fields_data[a].replace("\n","")
            overview += " "
        
        #print(overview)
        
        output = {}

        output["Overview"] = overview

        #JSON keys
        with open("fields.txt", "r") as f:
            lines = f.readlines()
            # Creating the JSON output
            for i in range(len(lines)):
                k = fields_data[i+1]
                data = k.replace("\n","")
                data = data.replace("Email Address: ","")
                data = data.replace("Website: ","")
                if "Establishment year" in lines[i]:
                    
                    output[lines[i].replace("\n","")] = data[-5:-1]
                else:
                    output[lines[i].replace("\n","")] = data

            f.close()
        #print(output)
        return success,output
    else:
        dict1 = {}
        dict1['Overview'] = "GPT was not able to process data from the provided link"
        with open("fields.txt", "r") as f:
            lines = f.readlines()
            for ii in lines:
                dict1[ii.replace("\n","")] = ""
        return False,dict1
    
def gpt_raw_input(text: str):
    return converse_gpt2(input_text=text)

def scraping(link: str):
    fields1 = "Overview,"
    with open("fields.txt", "r") as f:
            lines = f.readlines()
            for l in lines:
                fields1 += l.replace("\n",",")
    fields1 += ",City,Main Domestic Country"

    import requests
    from bs4 import BeautifulSoup
    import re


    # Make a request to the website
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    url = "http://%s/" % (link)
    response = requests.get(url, headers=headers)

    links = []
    data = ""
    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all('a'):
        href = link.get('href')
        #print(href)
        if href and ("about" in href or "story" in href or "who" in href or "company" in href or "service" in href or "contact" in href):
            
            url1 = ""
            if href.startswith('http'):
                url1 = href
            elif href.startswith('/'):
                url1 = url+href[1:]
            print(url1)
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

            r = requests.get(url1, headers=headers)
            soup1 = BeautifulSoup(r.content, "html.parser")
            for pp in soup1.find_all('p'):
                #try:
                
                content1 = str(pp).replace("<p>", "")
                content1 = content1.replace("</p>","")
                content1 += chr(13)
                
                data += content1
                
            
            try:
                data += soup1.find("p").text + chr(13)
                data += soup1.find("div").text + chr(13)

                for link1 in soup1.find_all('a'):
                    href1 = link1.get('href')
                    #print(href1)
                    if href1 and "mailto" in href1:
                        data+=chr(13)
                        data+=href1
                        data+=chr(13)
            except:
                pass
            #break
    input_text = data

    fields2 = '''About Us, Company Profile, Who we are, Products, Services, Partnership'''
    import json
    system_rules = f"From the input text, get the {fields1} JSON format. Leave it blank string if not found."     

    success, output1 = converse_gpt(input_text,system_rules)
    #print(success,output1)
    return True, output1
    # if success:
    #     try:
    #         return success, eval(output1['text'])
    #     except:
    #         dict1 = {}
    #         dict1['Overview'] = "GPT was not able to process data from the provided link"
    #         with open("fields.txt", "r") as f:
    #             lines = f.readlines()
    #             for ii in lines:
    #                 dict1[ii.replace("\n","")] = ""
    #         return True,dict1
    # else:
    #     dict1 = {}
    #     dict1['Overview'] = "GPT was not able to process data from the provided link"
    #     with open("fields.txt", "r") as f:
    #         lines = f.readlines()
    #         for ii in lines:
    #             dict1[ii.replace("\n","")] = ""
    #     return True,dict1

if __name__ == "__main__":
    #print(scraping("https://aurabiosciences.com/")[1])
    #c_name="S T L LOGISTICS"
    #loc="NEWTOWNABBEY"
    # print(get_overview_with_name_loc(c_name,loc)[1])
    ##print(overview)

    #print(keyword_extraction(overview)[1]['text'])
    #print(gpt_raw_input(text = input_text)[1])
    _,output = scraping(link = "www.awrlloyd.com")
    print(output)
    #print(output['text'])
    # output_json = {}
    # data = output['text'].splitlines()
    # with open("fields.txt", "r") as f:
    #     lines = f.readlines()
    #     for i,kk in enumerate(lines):
    #         if i<2:
    #             output_json[lines[i].replace("\n","")] = data[i].split(": ")[1]
    #         elif i==3:
    #             output_json[lines[i].replace("\n","")] = data[i][-5:-1]
    #         else:
    #             str1 = data[i]
    #             str1 = str1.replace("    ", "")
    #             str1 = str1.replace("- ", "")
    #             output_json[lines[i].replace("\n","")] = str1
    #         print(output_json[lines[i].replace("\n","")])
