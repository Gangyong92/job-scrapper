# 설치한 package
# requests : Python HTTP for Humans
# beautifulsoup4 : Screen-scraping library

import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]: # 마지막에 next 문자열이 있어서 제외 시켜줬음, 제외안하면 int()에서 오류뜸
    # pages.append(link.find("span").string) # "span" 태그 찾아서 pages 리스트에 저장 + 태그안에 str만 가져오겠음
    pages.append(int(link.string)) # span 태그까지 찾을 필요 없이 a 태그에서 str 가져올 수 있음. 필터링 정도에 따라 입맛대로 코딩하면됨. a 태그에 불필요한 str이 있었으면 span 태그까지 찾아서 필터링 했을것임.

  max_page = pages[-1]
  return max_page

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page * LIMIT}")
    print(result.status_code)

  return jobs