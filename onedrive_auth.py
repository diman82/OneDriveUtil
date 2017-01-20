import onedrivesdk
from selenium import webdriver
from onedrivesdk.helpers import GetAuthCodeServer

#Onedrive Access
redirect_uri = 'http://localhost'
client_secret = 'wPguLq9FqNWxiUR69vWzwva'
client_id_str = '0000000044194611'
api_base_url = 'https://api.onedrive.com/v1.0/'
scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']


user_name = 'diman82@gmail.com'
password = 'Master82'

client = onedrivesdk.get_default_client(client_id=client_id_str,
                                        scopes=scopes)

auth_url = client.auth_provider.get_auth_url(redirect_uri)


def getAuthCodeSelenium():

    phantomjs_path = r'C:\Python36\selenium\bin\phantomjs.exe'
    driver = webdriver.PhantomJS()  # 'phantomjs')

    # driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    # driver.set_window_size(1, 1)
    driver.get(auth_url)
    driver.implicitly_wait(15)
    login_field = driver.find_element_by_name("loginfmt")
    password_field = driver.find_element_by_name("passwd")
    sign_btn = driver.find_element_by_id("idSIButton9")

    # Fill user name and password
    login_field.send_keys(user_name)
    password_field.send_keys(password)
    sign_btn.click()
    element = driver.find_element_by_name('ucaccept')
    element.click()

    # parse URL to get code and close the browser
    tokens = driver.current_url.split('=')
    driver.quit()

    # access allow to execute all onedrive API's
    access_code = tokens[1].split('&')[0]
    print("access code is here ", access_code)
    return access_code

def getAuthCodeFromBrowser() :

    # this will block until we have the code
    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

    return code

def getManualCode() :

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider=http_provider,
        client_id=client_id_str,
        scopes=scopes)

    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
    auth_url = client.auth_provider.get_auth_url(redirect_uri)
    # Ask for the code
    print('Paste this URL into your browser, approve the app\'s access.')
    print('Copy everything in the address bar after "code=", and paste it below.')
    print(auth_url)
    code = input('Paste code here: ')

    return code