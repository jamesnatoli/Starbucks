# Script to brute force Sbucks store-locator
# original ritvikmath, edited jamesnatoli

import requests
import json
import re # regular expressions

class Store:
    """A class for Starbucks Store Date """
    # def __init__(self, snum=0, name='', lat=0.0, lon=0.0, city='', pcode=0, add=''):
    #     self.storeNumber = snum
    #     self.name = name
    #     self.latitude = lat
    #     self.longitude = lon
    #     self.city = city
    #     self.postalCode = pcode
    #     self.address = add
    def Organize( self, storeData):
        print( storeData)
        # for item in self.allData:
        #     print(item)
    
    def getStoreNumber():
        return self.storeNumber

    def getName():
        return self.name

    def getLatLong():
        return self.latitude, self.longitude

    def getAddress():
        return self.address
    
    def __init__( self, textDump):
        # Organize and store the data
        self.Organize( textDump)

def getJson( dataDump):
    # Dump the data to a json file
    with open("temp_garage.json", "w") as write_file:
        print( json.dumps( dataDump))
        # json.dumps( dataDump, write_file)

    # Read it back, now that it's nice
    with open("temp_garage.json", "r") as read_file:
        tempData = json.load( read_file)

    # Now return, that the file is closed
    return tempData
        
def processResponse(r):
    # parse out each store's info
    # stores = re.findall(r'"storeNumber":.*?"slug"', r)
    stores = []
    # print(len(re.findall(r'"storeNumber":.*?"slug"', r)))
    for allData in re.findall(r'"storeNumber":.*?"slug"', r):
        newStore = Store( getJson(allData))
        stores.append( newStore)
        break
        # parse out info about each store
        # storeInfo.append(list(re.findall(r'"storeNumber":"(.*?)".*?"name":"(.*?)".*?"latitude":(.*?),.*?"longitude":(.*?)}.*?"city":"(.*?)".*?"countrySubdivisionCode":"(.*?)".*?"postalCode":"(.*?)"', store)[0]))
    # print(stores)
    return stores

def main():
    # open zip code file
    f = open('laZips.txt', 'r')
    # Clean it
    laZips = [z.replace('\n','') for z in f.readlines()]
    
    allStores = []
    for idx,z in enumerate(laZips):
        # call request for 100 stores with current zipcode
        r = requests.get('https://www.starbucks.com/store-locator?place='+z)
        
        # if any response fails, quit immediately
        if r.status_code != 200:
            print(f'Error Code: {r.status_code}... exiting')
            raise SystemExit
        
        # process the text response that Starbucks gives back
        storeInfoList = processResponse(r.text)
        
    # truncate the returned zip code to a 5 digit zip
    for storeInfo in storeInfoList:
        # storeInfo[6] = storeInfo[6][:5]
        
        # add this store to the master list of stores
        allStores += storeInfoList
        

    # construct set of stores (non-duplicates)
    # seenStoreIds = {}
    # laStores = []
    # for store in allStores:
    #     if store[0] in seenStoreIds:
    #         continue
    #     else:
    #         laStores.append(store)
    #         seenStoreIds.append(store[0])

if __name__ == "__main__":
    main()
