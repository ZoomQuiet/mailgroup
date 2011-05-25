import urllib2

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
    response = urllib2.urlopen(prefix_url + email_address)
    dict = eval(response.read())
    prefix_url = 'http://42qu.com/-'
    return prefix_url + str(dict['id'])

if __name__ == '__main__':
    id = get_url('zsp007@gmail.com')
    print id
    
