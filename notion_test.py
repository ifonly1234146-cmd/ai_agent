"""
Notion API 접근 테스트 스크립트
Reference: https://developers.notion.com/guides/get-started/overview
"""

import urllib.request
import json

import os
NOTION_SECRET = os.environ.get("NOTION_SECRET", "")
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_SECRET}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


def notion_request(method: str, endpoint: str, body: dict = None) -> dict:
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def test_user_info():
    """현재 인증된 통합(integration) 정보 조회"""
    print("\n[1] 통합 정보 (GET /users/me)")
    result = notion_request("GET", "/users/me")
    print(f"  이름: {result.get('name')}")
    print(f"  타입: {result.get('type')}")
    print(f"  ID  : {result.get('id')}")


def test_search_pages():
    """워크스페이스 내 페이지 검색"""
    print("\n[2] 페이지 검색 (POST /search)")
    body = {"filter": {"value": "page", "property": "object"}, "page_size": 5}
    result = notion_request("POST", "/search", body)
    pages = result.get("results", [])
    print(f"  검색된 페이지 수: {len(pages)}")
    for page in pages:
        title_prop = page.get("properties", {}).get("title", {})
        title_parts = title_prop.get("title", [])
        title = "".join(t.get("plain_text", "") for t in title_parts) if title_parts else "(제목 없음)"
        print(f"  - [{page['id']}] {title}")


def test_fetch_page(page_id: str):
    """특정 페이지 내용 조회"""
    print(f"\n[3] 페이지 조회 (GET /pages/{page_id[:8]}...)")
    result = notion_request("GET", f"/pages/{page_id}")
    title_parts = result.get("properties", {}).get("title", {}).get("title", [])
    title = "".join(t.get("plain_text", "") for t in title_parts) if title_parts else "(제목 없음)"
    print(f"  제목: {title}")
    print(f"  URL : {result.get('url')}")
    print(f"  최종 수정: {result.get('last_edited_time')}")


def test_create_page(parent_page_id: str):
    """테스트 페이지 생성"""
    print("\n[4] 페이지 생성 (POST /pages)")
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": "API 스크립트 테스트 생성 페이지"}}]}
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "Python urllib로 Notion API 직접 호출 성공!"}}]
                },
            }
        ],
    }
    result = notion_request("POST", "/pages", body)
    print(f"  생성된 페이지 ID : {result.get('id')}")
    print(f"  생성된 페이지 URL: {result.get('url')}")
    return result.get("id")


if __name__ == "__main__":
    print("=== Notion API 접근 테스트 ===")
    try:
        test_user_info()
    except Exception as e:
        print(f"  오류: {e}")

    TARGET_PAGE_ID = "3868fb56-c419-8070-9ee8-eb600f2b4cfd"

    try:
        test_search_pages()
    except Exception as e:
        print(f"  오류: {e}")

    try:
        test_fetch_page(TARGET_PAGE_ID)
    except Exception as e:
        print(f"  오류: {e}")

    try:
        new_page_id = test_create_page(TARGET_PAGE_ID)
        print(f"\n  신규 페이지 생성 완료: {new_page_id}")
    except Exception as e:
        print(f"  오류: {e}")

    print("\n=== 테스트 완료 ===")
