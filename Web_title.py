import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_sidebar_links(url: str):
    # 1) 원격 URL에서 HTML 가져오기
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 200 OK 이외에 에러 발생 시 예외
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 에러: {e}")
        return []

    # 2) BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # 3) 사이드바 영역 찾기
    #    - pydata-sphinx-theme: 일반적으로 id="pst-primary-sidebar" 또는 class="bd-sidebar-primary"
    sidebar = soup.find("div", {"id": "pst-primary-sidebar"})
    if not sidebar:
        print("사이드바를 찾지 못했습니다.")
        return []

    # 4) 사이드바 내 모든 링크(a 태그) 추출
    a_tags = sidebar.find_all("a")

    # 5) (텍스트, href) 쌍으로 리스트 구성
    links_list = []
    for a in a_tags:
        text = a.get_text(strip=True)
        href = a.get("href", "")
        links_list.append((text, href))
    
    return links_list

def parse_linked_pages(links_list, base_url: str):
    """
    (text, href) 리스트를 순회하며, 각 href를 절대 경로로 만든 후 요청을 보냄.
    해당 페이지의 주된 본문 내용(div.bd-content 등)을 추출해
    { '링크 텍스트': '본문 텍스트' } 형태의 dict로 반환한다.
    """
    results = {}

    for text, href in links_list:
        if not href:
            # 링크가 없으면 스킵
            continue

        # base_url과 href를 합쳐 절대 경로 생성
        full_url = urllib.parse.urljoin(base_url, href)

        try:
            r = requests.get(full_url, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"페이지 요청 실패: {full_url}\n에러 내용: {e}")
            continue

        page_soup = BeautifulSoup(r.text, "html.parser")
        # Sphinx 문서에서 실제 내용이 들어있는 컨테이너를 찾아봄 (예: <div class="bd-content">)
        content_div = page_soup.find("div", class_="bd-content")

        if content_div:
            # 텍스트만 추출. 구분자는 '\n' (필요에 따라 공백, 줄바꿈 등 원하는 대로)
            page_text = content_div.get_text("\n", strip=True)
        else:
            # 만약 찾지 못하면 전체 페이지에서 텍스트 추출 등 원하는 로직
            page_text = page_soup.get_text("\n", strip=True)

        # 링크 텍스트를 key로, 본문 텍스트를 value로 저장
        results[text] = page_text

    return results

if __name__ == "__main__":
    # 테스트 URL: https://genesis-world.readthedocs.io/en/latest/api_reference/index.html
    test_url = "https://genesis-world.readthedocs.io/en/latest/api_reference/index.html"
    sidebar_links = get_sidebar_links(test_url)

    print("=== 사이드바 링크 목록 ===")
    for idx, (text, href) in enumerate(sidebar_links, start=1):
        print(f"{idx}. 텍스트: {text}, 링크: {href}")
