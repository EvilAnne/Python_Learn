
import shodan
import sys
from sys import exit

#shodan module
try:
    import shodan
except ImportError:
    print("No import module: pip install shodan")
    sys.exit()

#info
print("#"*30)
print("""
    1.Shodan Search ServerInfo
    2.Search IP Port
          """)
print("#"*30)
parget = input("Input Parget:")


if len(sys.argv) == 1:
    print("Usage: %s <search query>" % (sys.argv[0]))
    sys.exit(1)

#shodan api
SHODAN_API_KEY = "Ntbno1ernNwkVAJwi2TSGXgpi2jcEXWL"

api = shodan.Shodan(SHODAN_API_KEY)



def Shodan_Search_Info(search):
    try:
        request = api.search(search)

        print("Request found: %s" % (request['total']))

        for result in request['matches']:
            print("IP: %s" % (result['ip_str']))
            print(result['data'])
            print(' ')
    except shodan.APIError as e:
        print("Error %s " % (e))



#Search Host
def Shodan_Search_Host():
    IPaddress = input("Input Target IP Address:")
    host = api.host(IPaddress)
    print("""
    IP: %s
    Organzation: %s
    Operating System: %s
    """ % (host['ip_str'],host.get('org','n/a'),host.get('os','n/a'))
    )
    for item in host['data']:
        print("""
        Port: %s
        Banner: %s
        """ % (item['port'],item['data']))



if parget == "1":
    search = input("Search Shodan:")
    Shodan_Search_Info(search)
elif parget == "2":
    Shodan_Search_Host()
else:
    print("No parget")
