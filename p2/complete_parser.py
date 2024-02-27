"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub
import json
import os

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
My Helper Function for handling strings.
Written by Nott Laoaroon
"""
def str_correct_quotation(s):
    return '"'+s.replace('"','""')+'"'

def good_str(s):
    if s == None:
        return 'NULL'
    assert '\n' not in s
    if '"' in s:
        return str_correct_quotation(s)
    return s

"""
Written by Nott Laoaroon
"""

def parseJson(json_file):
    with open(json_file, 'r') as f:
        itemss = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        #print(itemss[0])
        """
        Open data files and process if exist
        """
        sellers = set()
        items = set()
        bids = set()
        categories = set()
        person = set()
        
        sell_counter = {}
        def sell_inc(name):
            if name not in sell_counter:
                sell_counter[name] = 0
            sell_counter[name] += 1
        bid_counter = {}
        def bid_inc(name):
            if name not in bid_counter:
                bid_counter[name] = 0
            bid_counter[name] += 1
        
        if os.path.isfile('Seller.dat'):
            with open('Seller.dat','r') as g:
                sellers = set(g.read().strip().split('\n'))
        
        if os.path.isfile('Item.dat'):
            with open('Item.dat','r') as g:
                items = set(g.read().strip().split('\n'))
            
        if os.path.isfile('Bid.dat'):
            with open('Bid.dat','r') as g:
                bids = set(g.read().strip().split('\n'))
            
        if os.path.isfile('Category.dat'):
            with open('Category.dat','r', encoding='utf-8') as g:
                categories = set(g.read().strip().split('\n'))
                
        if os.path.isfile('Person.dat'):
            with open('Person.dat','r', encoding='utf-8') as g:
                person = set(g.read().strip().split('\n'))
        
        """
        Finished processing
        """
        
        for row in itemss:
            
            # Add to Seller
            sellers.add(good_str(row['Seller']['UserID'])+'|'+
                         good_str(row['ItemID'])+'|'+
                         good_str(row['Location'])+'|'+
                         good_str(row['Country'])+'|'+
                         row['Seller']['Rating'])
            
            # Add to Item
            buy_price = "NULL"
            if "Buy_Price" in row:
                buy_price = transformDollar(row["Buy_Price"])
            currently = "NULL"
            if "Currently" in row:
                currently = transformDollar(row['Currently'])
            
            items.add(good_str(row['ItemID'])+'|'+
             good_str(row['Name'])+'|'+
             buy_price+'|'+
             transformDollar(row['First_Bid'])+'|'+
             row['Number_of_Bids']+'|'+
             currently+'|'+
             transformDttm(row['Started'])+'|'+
             transformDttm(row['Ends'])+'|'+
             good_str(row['Description'])
            )
            
            # Add to Bid
            if row['Bids'] != None:
                for _ in row['Bids']:
                    bid = _['Bid']
                    bids.add(good_str(bid['Bidder']['UserID'])+'|'+
                          good_str(row['ItemID'])+'|'+
                          transformDttm(bid['Time'])+'|'+
                          transformDollar(bid['Amount'])
                    )
                    
                    location = 'NULL'
                    if 'Location' in bid['Bidder']:
                        location = bid['Bidder']['Location']
                    country = 'NULL'
                    if 'Country' in bid['Bidder']:
                        country = bid['Bidder']['Country']
                    person.add(good_str(bid['Bidder']['UserID']) + '|' + 
                        'NULL' + '|' + 
                        'NULL' + '|' + 
                        good_str(location) + '|' + 
                        bid['Bidder']['Rating'])
                
            # Add to Category
            assert len(row['Category'])>0
            for category in row['Category']:
                #print(f"{row['ItemID']}"+'|'+f"{category}\n")
                assert '\n' not in category
                categories.add(f"{good_str(row['ItemID'])}"+'|'+f"{good_str(category)}")
                
            # Add to Person
            person.add(good_str(row['Seller']['UserID'])+'|'+
                        'NULL'+'|'+
                        'NULL'+'|'+
                        good_str(row['Location'])+'|'+
                        row['Seller']['Rating'])
            
        """
        Count the number of sellings and biddings
        """
        for x in bids:
            bid_inc(x.split('|')[0])
        for x in sellers:
            sell_inc(x.split('|')[0])
        person2 = set()
        for x in person:
            y = x.split('|')
            if y[0] not in sell_counter:
                y[1] = str(0)
            else:
                y[1] = str(sell_counter[y[0]])
            if y[0] not in bid_counter:
                y[2] = str(0)
            else:
                y[2] = str(bid_counter[y[0]])
            person2.add('|'.join(y))
        
        person = person2
        
        """
        Save and close data files
        """
        with open('Seller.dat','w') as g:
            g.write('\n'.join(list(sellers)))
        
        with open('Item.dat','w') as g:
            g.write('\n'.join(list(items)))
            
        with open('Bid.dat','w') as g:
            g.write('\n'.join(list(bids)))
            
        with open('Category.dat','w') as g:
            g.write('\n'.join(list(categories)))
            
        with open('Person.dat','w') as g:
            g.write('\n'.join(list(person)))
        """
        Finish closing data files
        """

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print ('Usage: python skeleton_json_parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing ", f)

if __name__ == '__main__':
    main(sys.argv)
