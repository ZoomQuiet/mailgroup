import urllib2
import json
import mg_log

log = mg_log.sysLogger()
def get_url(email_address):
    '''get the url for the email in 42qu
    Todo:
        How to process the chinese? The escape character!
    
    Args:
        email_address: the email_address
    Return:
        the 42qu url of the email owner
    '''
    prefix_url = 'http://api.42qu.com/search/man/'
    request_url = prefix_url + email_address
    try:
        response = urllib2.urlopen(request_url)
    except urllib2.HTTPError:
        log.error("cann't open url %s"%request_url)
        return False
    dict = json.loads(response.read())
    if dict:
        prefix_url = 'http://42qu.com/-'
        return prefix_url + str(dict['id'])
    else:
        return False

if __name__ == '__main__':
    id = get_url('zsp007@gmail.com')
    print id
    
