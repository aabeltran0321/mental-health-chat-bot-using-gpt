import requests
from bs4 import BeautifulSoup
import re
import openai
from translator_gpt import translate_website,translate_text,remove_excess_empty_lines
import tiktoken

openai.api_key = "YOUR-OPENAI-API-KEY-HERE"
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def chunk_string(text, max_token_length):
    tokens = encoding.encode(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for token in tokens:
        current_length += 1
        if current_length <= max_token_length:
            current_chunk.append(token)

        else:
            chunks.append(current_chunk)
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(current_chunk)

    decoded_chunks = [encoding.decode(chunk) for chunk in chunks]
    return decoded_chunks

def scrapingv2(link = "", location = ""):
    dict1 = {}
    
    with open("fields.txt", "r") as f:
        lines = f.readlines()
        for ii in lines:
            dict1[ii.replace("\n","")] = ""
    try:

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

        url = "http://%s/" % (link)
        response = requests.get(url, headers=headers)

        links = []
        data = ""
        soup = BeautifulSoup(response.content, "html.parser")
        for link1 in soup.find_all('a'):
            

            href1 = link1.get('href')
            #print(href)
            txt2 = link1.text
            txt2 = txt2.replace("\n", "")
            if href1 is not None:
                href = href1.lower()
                if href and ("about" in href or "who" in href or "product" in href or "service" in href  or "story" in href or "company" in href) and not("linkedin" in href) and not("product/" in href):
                    
                    url1 = ""

                    if href.startswith('http'):
                        url1 = href1
                    elif href.startswith("/"):
                        url1 = f"http://{link}{href1}"
                    else:
                        url1 = f"http://{link}/{href1}"
                    if len(url1):
                        if not(url1 in links):
                            links.append(url1)
                            print(url1)
                            try:
                                # translation = translate_website(url1)
                                # if "403" in translation:
                                #     r = requests.get(url1, headers=headers)
                                #     soup1 = BeautifulSoup(r.content, "html.parser")
                                #     data += soup1.get_text()
                                # else:
                                #     data += chr(13)
                                #     data += translation
                                r = requests.get(url1, headers=headers)
                                soup1 = BeautifulSoup(r.content, "html.parser")
                                data += remove_excess_empty_lines(soup1.get_text())
                            except Exception as e:
                                print(e)
            
                elif len(txt2):
                    #print(txt2, len(txt2))
                    text1 = str(translate_text(txt2))
                    text1 = text1.lower()
                    if ("welcome" in text1 or "about" in text1 or "us"==text1 or "product" in text1 or "service" in text1 or "story" in text1 or "company" in text1) and not("linkedin" in text1) and not("product/" in text1)  and not("culture" in text1) and not("our services" in text1):
                        url1 = ""
                        href = href1.lower()
                        if href.startswith('http'):
                            url1 = href1
                        elif href.startswith("/"):
                            url1 = f"http://{link}{href1}"
                        else:
                            url1 = f"http://{link}/{href1}"
                        if len(url1):
                            if not(url1 in links):
                                links.append(url1)
                                print(url1)
                                try:
                                    # translation = translate_website(url1)
                                    # if "403" in translation:
                                    #     r = requests.get(url1, headers=headers)
                                    #     soup1 = BeautifulSoup(r.content, "html.parser")
                                    #     data += soup1.get_text()
                                    # else:
                                    #     data += chr(13)
                                    #     data += translation
                                    r = requests.get(url1, headers=headers)
                                    soup1 = BeautifulSoup(r.content, "html.parser")
                                    data += remove_excess_empty_lines(soup1.get_text())
                                except Exception as e:
                                    print(e)
        if len(data):
            input_text = data
            chunks = chunk_string(input_text,2400)
            input_prompt = ""
            for index, chunk in enumerate(chunks):
                #print(chunk)
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {'role': 'system', 'content': "You are a company researcher. Get the company information on the input text, automatically translate to english, and summarize the response without omitting company information."},
                        {'role': 'user', 'content': chunk}
                    ],
                    max_tokens=1000,
                    temperature=0
                )

                # Extract the assistant's reply from the response
                output = response.choices[0].message['content'].strip()
                output = re.sub(r'\.', '', output)
                #print(output)
                input_prompt += output
                input_prompt+=chr(13)

            #print(input_prompt)

            main_system = f'''From the input text, complete these sentences and please strictly follow this format. Don't include company name on the text. For establishment date, get the year only.:
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
            The company specialises in <specific products> under <brand names; trademarks>.'''

            response1 = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {'role': 'system', 'content': main_system},
                        {'role': 'user', 'content': input_prompt}
                    ],
                    temperature=0
            )
            resp = response1.choices[0].message['content'].strip()
            resp = resp.replace("\n"," ")
            

            

            if len(resp)>100:
                dd = resp.split(". ")
                dd.insert(1,f"It conducts business from its registered head office located in {location.title()}")
                resp1 = ""
                for d in dd:
                    resp1 += (d + ". ")

                resp1 = resp1.replace("..",".")
                resp1 = resp1.replace("  "," ")
                resp1 = resp1[:(len(resp1)-1)] 
                dict1['Overview'] = resp1
            else:
                dict1['Overview'] = "" 
        else:
            dict1['Overview'] = "" 
    except Exception as e:
        dict1['Overview'] = "" #str(e)
        
    return True,dict1


def update_comparison(prev_overview:str,curr_overview:str):
    main_system = '''You are a document analyst. Measure the Update Percentage in JSON format of the previous and current text being analyzed. Consider the similarity. 0 is the lowest. 100 is the highest. return it in this format:
    {
        "update_percentage" : <percentage in float>
    }
    '''

    input_prompt = f'''"previous text:" {prev_overview}

    "current text": {curr_overview}
    '''

    response1 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': main_system},
                {'role': 'user', 'content': input_prompt}
            ],
            temperature=0
    )
    resp = response1.choices[0].message['content'].strip()
    resp = resp.replace("\n"," ")
    pcnt = {}
    pcnt = eval(resp)
    dict1 = {
            "flag": "False",
            "overview": curr_overview
        }
    if pcnt["update_percentage"]>=50:
        dict1 = {
            "flag": "True",
            "overview": prev_overview
        }
    return dict1
    

if __name__=="__main__":
    #print(scrapingv2(link="www.awrlloyd.com",location="JIANGMEN, China"))

    curr = '''This company operates as a specialist strategy and M and A advisory firm focused on the Indo-Pacific region. It conducts business from its registered head office located in Hong Kong. The company was founded in 2000. It was founded by three partners including Alex Wood and Jeremy Ayre.
The company services is divided into two generic categories: Transactions Advisory and Strategy Consulting. Its Transactions Advisory service modules provide hands-on and on-the-ground support to our clients for the full range of corporate finance transactions in Asia-Pacific including mergers, acquisitions, equity capital raising, strategic investor deals, divestments, project finance, IPOs and restructuring. The company's Strategy Consulting service modules is designed to help its clients understand the dynamics around existing value, capital and corporate structures and to formulate plans for new configurations that will maximize shareholder value over the medium to long term. The company is present in Australia, Hong Kong, Singapore, Vietnam, Thailand, Indonesia, India, Sri Lanka, Oman and the UAE with principal offices in Mumbai, Bangkok, Jakarta, and Ho Chi Minh City.
The company serves various customers including SK group, Petronas, PetroVietnam group, PTT group, MPRL, Sojitz, Chubu Electric, Sumitomo, Toyota Tsusho, Tuas, KEPCO, Doosan, Woodside, Banpu, Ratch, B Grimm, Goldwind, XEMC, PTL Holding, Siam Motor, Raimon Land, The Erawan Group, Tata Steel, Saudi Aramco, Kuwait Petroleum, DP World, Renaissance Heavy Industries, Chevron, BG, GDF Suez, Ophir, APICO, Hess, AES, BOC, Michelin, Swedish Space Corp, Airbus, Thales and the IFC.
The company offers its services in the domestic market and abroad including United Kingdom, Australia, Hong Kong, Singapore, Vietnam, Thailand, Indonesia, India, Sri Lanka, Oman and the UAE with principal offices in Mumbai, Bangkok, Jakarta, and Ho Chi Minh City.'''

    prev = '''This company is engaged in providing M and A support and industry intelligence. It conducts business from its registered head office located in Hong Kong. It also operates in Mumbai, Bangkok, and Ho Chi Minh City. The company was founded in 2000.
The company is involved in providing M and A support and industry intelligence to companies in the Asia-Pacific region. It completes more than 500 assignments for clients in various countries. The company has developed extensive client, partner, and intelligence networks throughout the Indo-Pacific. Moreover, the company primarily serves clients including SK group, Petronas, PetroVietnam group, PTT group, MPRL, Sojitz, Chubu Electric, Sumitomo, and Toyota Tsusho, among others.'''

    print(update_comparison(prev_overview=prev,curr_overview=curr))
