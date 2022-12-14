from urllib.request import urlopen, urlparse
import re



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_robots(test_url):
    print(test_url)
    print("getting robots..")
    patterns = ["^https:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+$", "^http:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+$"]
    for pattern in patterns:
        result = re.findall(pattern, test_url)
        if result:
            print(str(result))
            domain = urlparse(test_url).netloc
            scheme = urlparse(test_url).scheme
            robots =  f'{scheme}://{domain}/robots.txt'
            sitemap_url = ''    
            sitemap_ls = []
            try:
                with urlopen(robots) as stream:
                    for line in urlopen(robots).read().decode("utf-8").split('\n'):
                        #if "disallow".lower() in line.lower():
                            #print(line)
                        if 'Sitemap'.lower() in line.lower():
                            sitemap_url = re.findall(r' (https.*xml)', line)[0]
                            sitemap_ls.append(sitemap_url)
                        if "allow".lower() in line.lower():
                            print(f"{bcolors.OKGREEN}{line}")
                print(f"{bcolors.WARNING}Sitemap: {sitemap_ls}")
                return list(set(sitemap_ls))
            except Exception as err:
                print(err)
                print(type(err))


