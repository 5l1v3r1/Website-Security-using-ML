# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 21:23:55 2019

@author: Parth
"""
import numpy as np
import pandas as pd
import pickle
from urllib.request import urlopen
from linkcrawler import LinkFinder
from general import *
from domain import *
from Features import Hello

class Spider:
    project_name=''
    base_url=''
    domain_name=''
    queue_file=''    #indicates the path of the queue file
    crawled_file=''  #indicates the path of the crawled file
    defect_file=''
    queue=set()
    crawled=set()
    #We have used sets to enable faster access to the memory. 
    defect=set()
    
    def __init__(self,project_name,base_url,domain_name):
        Spider.project_name=project_name
        Spider.base_url=base_url
        Spider.domain_name=domain_name
        Spider.queue_file=Spider.project_name+"/queue.txt"     #file address appending
        Spider.crawled_file=Spider.project_name+"/crawled.txt" 
        Spider.defect_file=Spider.project_name+"/defect.txt"
        self.boot()
        self.crawl_page("First Spider",Spider.base_url)
        
    @staticmethod
    def boot():
        '''
        ->Just as it boots up, it will create a project directory and the files in it.
        
        ->It will also store the contents of the queue and crawled file in the sets so as 
          to perform faster memory access operations.
        '''
        create_project_directory(Spider.project_name)
        create_project_file(Spider.project_name,Spider.base_url)
        Spider.queue=file_to_set(Spider.queue_file)
        Spider.crawled=file_to_set(Spider.crawled_file)
        #Spider.defect=file_to_set(Spider.defect_file)
    
    @staticmethod
    def pred(url):
        protocol = []
        domain = []
        path = []
        having_ip = []
        len_url = []
        having_at_symbol = []
        redirection_symbol = []
        prefix_suffix_separation = []
        sub_domains = []
        tiny_url = []
        abnormal_url = []
        web_traffic = []
        domain_registration_length = []
        dns_record = []
        statistical_report = []
        age_domain = []
        http_tokens = []
    
    #    arr=df['urls']
        a=Hello()
        #for url in arr:
        print("Analyzing: ",url)
        protocol.append(a.getProtocol(url))
        path.append(a.getPath(url))
        having_ip.append(a.having_ip_address(url))
        domain.append(a.getDomain(url))
        len_url.append(a.url_length(url))
        having_at_symbol.append(a.check_at(url))
        redirection_symbol.append(a.redirection(url))
        prefix_suffix_separation.append(a.check_dash(url))
        sub_domains.append(a.check_dots(url))
        tiny_url.append(a.shortening_service(url))
        web_traffic.append(a.web_traffic(url))
        domain_registration_length.append(a.check_date(url))
        dns_record.append(a.check_dns(url))
        statistical_report.append(a.statistical_report(url))
        age_domain.append(a.check_age(url))
        http_tokens.append(a.https_token(url))
                
                
        d={'Having_IP':pd.Series(having_ip),'URL_length':pd.Series(len_url),'@':pd.Series(having_at_symbol),
               'Redirection':pd.Series(redirection_symbol),'Prefix_Suffix_separation':pd.Series(prefix_suffix_separation),
               'SubDomains':pd.Series(sub_domains),'tiny_url':pd.Series(tiny_url),
               'Web traffic':pd.Series(web_traffic),
               'Domain_length':pd.Series(domain_registration_length),'DNS record':pd.Series(dns_record),
               'statistical_report':pd.Series(statistical_report),'Domain Age':pd.Series(age_domain),
               'HTTP token':pd.Series(http_tokens)}
                
        finaldata=pd.DataFrame(d)
    
        abc=finaldata.iloc[:,:].values
    
        file= 'DecisionTree.pkl'
        with open(file,'rb') as f:
            classifier=pickle.load(f)
            f.close()
            
        x_pred=classifier.predict(abc)
        if x_pred[0]==1:
            Spider.defect.add(url)
        
        #print("The prediction is: ",x_pred)
    
    
    @staticmethod
    def crawl_page(thread_name,page_url):
        if page_url not in Spider.crawled:
            try:
                print(thread_name," now crawling ",page_url)
                print("Queue ", len(Spider.queue), " | Crawled ",len(Spider.crawled))
                Spider.add_links_to_queue(Spider.gather_link(page_url))
                Spider.queue.remove(page_url)
                Spider.crawled.add(page_url)
                Spider.pred(page_url)                                
                Spider.update_files()
            except Exception as e:
                print(str(e))
    @staticmethod
    def gather_link(page_url):
        '''
        Algorithm:
            1. Opens the url.
            2. Checks if the webpage opened is an html document. If true, then reads and decodes the document in a string format.
            3. Creates and object of LinkFinder and passes the html_string obtained in step 2 to the LinkFinder class for further processing. 
            4. If there is an error, return an empty set. 
            5. return page links at the end. 
        '''

        html_str=''
        try:        
            response=urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):         #Checks if the document we are crawling is a webpage and then proceeds. 
                a=response.read()
                html_str=a.decode('utf-8')          #Decode into string format for HTMLPraser class. 
            finder=LinkFinder(Spider.base_url,page_url)     
            finder.feed(html_str)       #This will implicitly pass the html_string, call the methods and start the processing. 
        except Exception as e:
            print(str(e))
            return set()        #Returns an empty set. 
        return finder.page_links()      
    
    @staticmethod
    def add_links_to_queue(links):
        '''
        This method checks if the links are not already present in the queue and crawled queue.
        It also checks if the link's domain name is anything other than the domain name we want to crawl on. 
        '''
        for i in links:
            if i in Spider.queue:
                continue
            if i in Spider.crawled:
                continue
            if Spider.domain_name != get_domain_name(i):
                continue
            Spider.queue.add(i)
            
    @staticmethod
    def update_files():
        set_to_file(Spider.queue_file,Spider.queue)
        set_to_file(Spider.crawled_file,Spider.crawled)
        set_to_file(Spider.defect_file,Spider.defect)    
    
    
    
            
            
    