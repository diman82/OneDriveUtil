import onedrivesdk
import onedrive_auth
import asyncio
import os.path
from onedrivesdk.helpers import GetAuthCodeServer

PATH_TO_LOCAL_UL = "k:/test"
PATH_TO_REMOTE_UL = "/test/"
ROOT_FOLDER_ID = '8930240577EB1134%2190277'

def main():
    SESSION_SAVED = False

    redirect_uri = "http://localhost"
    client_secret = "wPguLq9FqNWxiUR69vWzwva"
    my_client_id = "0000000044194611"

    client = onedrivesdk.get_default_client(client_id=my_client_id,
                                            scopes=['wl.signin',
                                                    'wl.offline_access',
                                                    'onedrive.readwrite'])
    if SESSION_SAVED:
        # Next time you start up, check for an existing session. If one is found,
        client.auth_provider.load_session()
        client.auth_provider.refresh_token()
    else:
        # code = onedrive_auth.getAuthCodeSelenium()
        code = onedrive_auth.getAuthCodeFromBrowser()
        # code = onedrive_auth.getManualCode()
        client.auth_provider.authenticate(code, redirect_uri, client_secret)

        # save session
        client.auth_provider.save_session()
        print('Session saved')

        # Run the function recursively to iterate through all subdirs
        placeFiles(client, PATH_TO_LOCAL_UL)

current_folder_id = ROOT_FOLDER_ID
def placeFiles(client, path_to_ul):
    foldermappingdict = {}
    for name in os.listdir(path_to_ul):
        global current_folder_id
        localpath = os.path.join(path_to_ul, name)
        print("Current path", localpath)
        if os.path.isfile(localpath):
            print("STOR", name)
            rel_path = os.path.relpath(localpath, path_to_ul).replace('\\', '/')    # change the path to *nix platform style
            rel_path_to_ul = os.path.relpath(localpath, PATH_TO_LOCAL_UL).replace('\\', '/')    # change the path to *nix platform style
            print("Relative path", rel_path)
            print('Uploading item/s.. ', path_to_ul)
            client.item(drive="me", path=(PATH_TO_REMOTE_UL+rel_path_to_ul).replace('\\', '/')).upload_async(localpath.replace('\\', '/'))
            # client.item(drive="me", id=current_folder_id).children[rel_path].upload_async(localpath.replace('\\', '/'))
        elif os.path.isdir(localpath):
            print("MKD", name)
            try:
                f = onedrivesdk.Folder()
                i = onedrivesdk.Item()
                i.name = name
                i.folder = f

                returned_item = client.item(drive='me', id=current_folder_id).children.add(i)
                foldermappingdict[localpath] = current_folder_id   # map current folder path to cloud folder_id
                current_folder_id = returned_item._prop_dict['id']
            # ignore "directory already exists"
            except Exception as e:
                print(e)

            print("CWD", name)
            placeFiles(client, localpath)
            current_folder_id = foldermappingdict[localpath]    # reference back to initial current_folder_id to continue create directories in cloud in the proper place

if __name__ == "__main__":
    main()

# Upload an item
# client.item(drive="me", id="8930240577EB1134%2166557").children["Adobe.Photoshop.Lightroom.CC.2015.8.(6.8).RePack.by.KpoJIuK.iso"].upload("./Adobe.Photoshop.Lightroom.CC.2015.8.(6.8).RePack.by.KpoJIuK.iso")
# client.item(drive="me", id="8930240577EB1134%2166557").children["Adobe.Photoshop.Lightroom.CC.2015.8.(6.8).RePack.by.KpoJIuK.iso"].upload_async("./Adobe.Photoshop.Lightroom.CC.2015.8.(6.8).RePack.by.KpoJIuK.iso")
# client.item(drive="me", path="/Adobe.Photoshop.Lightroom.CC.2015.8.(6.8).RePack.by.KpoJIuK.iso").upload_async("/tmp/mnt/sda1/Upload/Adobe.Photoshop.Lightroom.CC.2015.8.(6.8).RePack.by.KpoJIuK.iso")