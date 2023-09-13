import tkinter as tk
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup


valid_proxies = []

def get_proxies():
    url = "https://www.sslproxies.org"

    # Make a GET request to fetch the raw HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the textarea with class 'form-control'
    textarea_content = soup.find('textarea', {'class': 'form-control'}).text

    proxies = textarea_content.split("\n")[3:]

    return proxies




def get_valid_proxies():
    global proxies
    proxies = get_proxies()

    while proxies:
        if len(valid_proxies) >= 5:
            break
        proxy = proxies.pop()
        try:
            requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https":proxy}, timeout=1)
            # print(proxy)
            if proxy:
                valid_proxies.append(proxy)
        except:
            print("Proxy Failed!")
            continue


# Function to make the GET request using Selenium
def make_request():
    # Get the domain from entry2 and proxy from entry1
    domain = entry2.get()
    prox = proxy = entry1.get()
    
    
    # if ',' in proxy:
    #     proxies = proxy.split(',')
    # else:
    #     proxies = [proxy]


    # Set up the WebDriver with the specified proxy
    # for prox in valid_proxies:
        # options = {
        #     'proxy': {
        #         'http': '',
        #         'https': '',
        #         'no_proxy': 'localhost,127.0.0.1'
        #     }
        # }

        
    if not prox:
        return
    
    if not domain:
        return

    # Configure the WebDriver to use the proxy settings
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=http://' + prox)
    chrome_options.add_argument('--headless')  # Make Chrome headless

    # Create the WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Define the URL with the provided domain
        url = f"https://majestic.com/reports/site-explorer?IndexDataSource=F&defaultQ={domain}&q={domain}&oq={domain}"
        # Navigate to the URL
        driver.get(url)
        
        # You can perform further actions with Selenium here if needed
        import time
        time.sleep(2)

        content = driver.page_source

        # Check if 'citation_flow_innertext' is present in the content
        if ('citation_flow_innertext' in content) or ('trust_flow_innertext' in content):
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Find the element with id 'citation_flow_innertext'
            citation_flow_element = soup.findAll('text', {'class': 'citation_flow_innertext'})
            
            # Find the element with id 'trust_flow_innertext'
            trust_flow_element = soup.findAll('text', {'class': 'trust_flow_innertext'})

            
            print("Citation")
            print(citation_flow_element)           
            print("trust")
            print(trust_flow_element)           

            if citation_flow_element or trust_flow_element: 

                if len(citation_flow_element) > 1:
                    trust_flow_value = citation_flow_element[0].text
                    citation_flow_value = citation_flow_element[1].text

                else:
                    citation_flow_value = citation_flow_element[0].text
                    trust_flow_value = trust_flow_element[0].text

                # Print or use the values as needed
                print("Citation Flow:", citation_flow_value)
                print("Trust Flow:", trust_flow_value)

                entry3.delete(0, END)
                entry4.delete(0, END)
                
                # Set text for entry3 and entry4
                entry3.insert(0, citation_flow_value)
                entry4.insert(0, trust_flow_value)


            else:
                print("Element not found")

        else:
            print("'citation_flow_innertext' not found in content")
        # Close the WebDriver
        driver.quit()
        
        print("Request successful")
        
    except Exception as e:
        print("Error:", e)



# Create the main window
root = tk.Tk()
root.title("Majestic trust flow checker")

# Create the top frame with 3 columns and 2 rows
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.BOTH, expand=True)

# Labels in the first column of the top frame
label1 = tk.Label(top_frame, text="proxy")
label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label2 = tk.Label(top_frame, text="domain")
label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Input fields in the second column of the top frame
entry1 = tk.Entry(top_frame)
entry1.grid(row=0, column=1, padx=10, pady=10, sticky="w")

entry2 = tk.Entry(top_frame)
entry2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Dropdown in the first row of the third column
options = ["HTTP",]
dropdown = ttk.Combobox(top_frame, values=options, width=10)
dropdown.grid(row=0, column=2, padx=10, pady=10, sticky="w")
dropdown.set(options[0])

# Button in the second row of the third column
button = tk.Button(top_frame, text="get_info", command=make_request)
button.grid(row=1, column=2, padx=10, pady=10)

# Create the second frame with 2 columns and 2 rows
second_frame = tk.Frame(root)
second_frame.pack(fill=tk.BOTH, expand=True)

# Labels in the first row of the second frame
label3 = tk.Label(second_frame, text="trust flow found")
label3.grid(row=0, column=0, padx=10, pady=0, sticky="w")

label4 = tk.Label(second_frame, text="citation flow found")
label4.grid(row=0, column=1, padx=10, pady=0, sticky="w")

# Input fields in the second row of the second frame
entry3 = tk.Entry(second_frame)
entry3.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry4 = tk.Entry(second_frame)
entry4.grid(row=1, column=1, padx=10, pady=10, sticky="w")


if __name__ == '__main__':
    # Start the main loop
    root.mainloop()
