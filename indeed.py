# 설치한 package
# requests : Python HTTP for Humans
# beautifulsoup4 : Screen-scraping library

import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:  # 마지막에 next 문자열이 있어서 제외 시켜줬음, 제외안하면 int()에서 오류뜸
        # pages.append(link.find("span").string) # "span" 태그 찾아서 pages 리스트에 저장 + 태그안에 str만 가져오겠음
        pages.append(
            int(link.string)
        )  # span 태그까지 찾을 필요 없이 a 태그에서 str 가져올 수 있음. 필터링 정도에 따라 입맛대로 코딩하면됨. a 태그에 불필요한 str이 있었으면 span 태그까지 찾아서 필터링 했을것임.

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {
        "class": "title"
    }).find("a")["title"]  #["title"] 속성값을 가져옴
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)  # str은 앞쪽 공백이 있어서 제거하기 위해 추가
    else:
        company = str(company.string)  # str은 앞쪽 공백이 있어서 제거하기 위해 추가
    company = company.strip()  # 사이드 문자 제거 아무것도 안쓰면 공백 제거
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]

    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page * LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

    for result in results:
        job = extract_job(result)
        jobs.append(job)
  return jobs


def get_jobs():
  last_page = get_last_pages()
  jobs = extract_jobs(last_page)
  return jobs