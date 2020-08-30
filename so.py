import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"


def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)  # next 그 앞 값 가져옴 앞뒤 공백 제거

    return int(last_page)


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company, location = html.find("h3").find_all("span", recursive=False)
    # 이대로 쓰면 중첩되어 있는 모든 span 가져올거임 그래서 recursive=False 옵션 추가(첫번째 레벨의 span만 가져옴)
    # company, location -> 2개 모두 가져와야하는데 한개만 클래스가 존재하는 경우 식별해서 가져오기 불편함. 같은 레벨에 있는 span을 순서대로 가져오도록 함
    company = company.get_text(strip=True)
    location = location.get_text(
        strip=True).strip("-").strip(" \r").strip("\n")
    # get_text(strip=True) get_text에서 strip=True 옵션 주면 앞뒤 공백제거
    # get_text 태그 벗겨내고 유니코드 스트링으로 출력. \n 이런것까지 출력. 개인적으론 string이 더 편한것 같음
    # strip("-") "-" 잘라냄. 현재 사이트에서는 없으나 공부용으로 남김
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        "apply_link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page {page}")
        result = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = get_last_pages()
    jobs = extract_jobs(last_page)
    
    return jobs
