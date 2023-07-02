import requests
from bs4 import BeautifulSoup

def find_target_links(html_link):
    html_content = requests.get(html_link).text
    soup = BeautifulSoup(html_content, 'html.parser')
    target_links = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'upgrade-pipeline' in href:
            target_links.append(href)
    print(target_links)
    return target_links

def check_link_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return 'oc describe cluster' in response.text
    else:
        return False

def main():
    given_html = 'http://virt-openshift-05.lab.eng.nay.redhat.com/buildcorp/ocp_upgrade/39532.html'

    target_links = find_target_links(given_html)

    for link in target_links:
        if check_link_content(link):
            print(f'给定的地址 {given_html} 包含 "oc describe cluster" 字段。')
            print(f'满足条件的地址为 {link}')
            break

if __name__ == '__main__':
    main()

