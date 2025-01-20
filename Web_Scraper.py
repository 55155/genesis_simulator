import requests
import urllib.parse
from bs4 import BeautifulSoup
import os

def get_sidebar_links(url: str):
    """
    주어진 URL에서 사이드바 내 (링크 텍스트, href) 쌍을 리스트로 반환한다.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[get_sidebar_links] HTTP 요청 에러: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # pydata-sphinx-theme 사이드바: <div id="pst-primary-sidebar">
    sidebar = soup.find("div", {"id": "pst-primary-sidebar"})
    if not sidebar:
        print("[get_sidebar_links] 사이드바를 찾지 못했습니다.")
        return []

    # 사이드바 내 모든 <a> 태그
    a_tags = sidebar.find_all("a")

    links_list = []
    for a in a_tags:
        text = a.get_text(strip=True)
        href = a.get("href", "")
        if text and href:
            links_list.append((text, href))

    return links_list


def get_filename_from_href(href: str) -> str:
    """
    링크의 마지막 부분을 추출해, *.txt 형태의 파일 이름으로 변환.
    예) 'options/renderer/renderer.html' -> 'renderer.txt'
    """
    parts = href.rstrip("/").split("/")  # 뒤쪽 슬래시 제거 후 "/" 분할
    last_part = parts[-1]  # 예: 'renderer.html'

    # '.'으로 분할하여 확장자 제거
    if "." in last_part:
        file_base = last_part.split(".")[0]  # 'renderer'
    else:
        file_base = last_part

    return f"{file_base}.txt"


def save_tex2jax_text(url: str, output_filename: str):
    """
    주어진 URL에서 'class="tex2jax_ignore mathjax_ignore"'인 요소들의 텍스트를 추출해
    줄바꿈/여러 공백을 하나의 공백으로 정리한 뒤 output_filename에 저장한다.
    """
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[save_tex2jax_text] 페이지 요청 실패: {url} / 에러: {e}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # 'tex2jax_ignore mathjax_ignore' 클래스를 가진 요소들
    elements = soup.select(".tex2jax_ignore.mathjax_ignore")

    texts = []
    for elem in elements:
        # (1) 기본적으로 '\n'으로 줄을 구분하여 텍스트 추출
        raw_text = elem.get_text("\n", strip=True)
        # (2) split() → 연속 공백/줄바꿈 전부 토큰화 → ' '.join()으로 단일 공백으로 치환
        one_line_text = " ".join(raw_text.split())
        texts.append(one_line_text)

    # 요소별로 '\n\n'(또는 '\n')로 구분해 저장할 수 있음
    # -> 원하는 형태에 따라 '\n'.join(...) 또는 ' '.join(...) 가능
    joined_text = "\n".join(texts)

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(joined_text)

    print(f"[SAVE] '{url}' → '{output_filename}' (추출 길이: {len(joined_text)})")


if __name__ == "__main__":
    # https://genesis-world.readthedocs.io/en/latest/user_guide/index.html# -> Guide
    # https://genesis-world.readthedocs.io/en/latest/api_reference/index.html -> API info
    base_url = "https://genesis-world.readthedocs.io/en/latest/user_guide/index.html#"
    # (1) 사이드바 링크 불러오기
    sidebar_links = get_sidebar_links(base_url)
    print("=== 사이드바 링크 목록 ===")
    for idx, (text, href) in enumerate(sidebar_links, start=1):
        print(f"{idx}. '{text}' -> {href}")

    # (2) 각 링크를 순회, 텍스트를 파일로 저장
    for link_text, href in sidebar_links:
        # 절대 경로 URL
        full_url = urllib.parse.urljoin(base_url, href)
        # 링크의 마지막 부분으로부터 파일명 생성
        output_file = get_filename_from_href(href)
        # 추출 & 저장
        save_tex2jax_text(full_url, output_file)
