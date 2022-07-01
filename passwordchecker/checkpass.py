import requests
import hashlib
import sys
from pprint import pprint

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    print(type(res.status_code))
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res:status_code}, check the api and try again")
    return res


def read_res(response):
    print(response.text)


# read_res(request_api_data('ABCED'))

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(pasword):
    # Check password if it exists in API response
    sha1password = hashlib.sha1(pasword.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(first5_char, tail, response)
    return get_password_leaks_count(response, tail)


def main(args: str = '12345678'):
    for password in args:
        count = pwned_api_check(password)
        if count:
            pprint(f'{password} was found in {count} times.... you should probably change your password!')
        else:
            pprint(f'{password}  was Not found. Carry on!')
    return 'done!'
    
x = sys.argv[1:] 

sys.exit(main(x))