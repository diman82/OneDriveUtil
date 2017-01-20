import onedrivesdk
import os.path
# import asyncio
from onedrivesdk.helpers import GetAuthCodeServer

session_saved = True

redirect_uri = "http://localhost/"
client_secret = "wPguLq9FqNWxiUR69vWzwva"
my_client_id = "0000000044194611"

client = onedrivesdk.get_default_client(client_id=my_client_id,
                                        scopes=['wl.signin',
                                                'wl.offline_access',
                                                'onedrive.readwrite'])

if session_saved:
    # Next time you start up, check for an existing session. If one is found,
    client.auth_provider.load_session()
    client.auth_provider.refresh_token()
else:
    auth_url = client.auth_provider.get_auth_url(redirect_uri)
    # this will block until we have the code
    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
    print(type(code))
    client.auth_provider.authenticate(code, redirect_uri, client_secret)

    # save session
    client.auth_provider.save_session()
    print('Session saved')

# get the top x elements of folder, leaving the next page for more elements
collection = client.item(drive='me', id='8930240577EB1134%2114312').children.request().get()
# folder = client.item(drive='me', id='8930240577EB1134%2114312').children.request(top=3).get()

for n in collection:
    # get the first item in the collection
    item = n
    id_of_file = item.id
    path = os.path.join('e:/test', item.name)
    if os.path.exists(path):
        continue

    client.item(drive='me', id=id_of_file).download(path)
