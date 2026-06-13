"""
wiki_search.py
Playwright MCP + Claude API를 활용한 위키피디아 검색 및 요약 스크립트

사용법:
    python wiki_search.py <검색어>
    python wiki_search.py 양자컴퓨터

환경변수:
    ANTHROPIC_API_KEY — Anthropic API 키 (필수)
"""

import asyncio
import sys
import os
import json
import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SYSTEM_PROMPT = """\
당신은 위키피디아 검색 전문 어시스턴트입니다.
주어진 검색어로 위키피디아를 탐색하고 첫 번째 검색 결과의 핵심 내용을 한국어로 요약합니다.

작업 순서:
1. https://www.wikipedia.org 접속
2. 검색창에 검색어 입력 후 검색 버튼 클릭
3. 이동된 문서의 본문 내용을 추출
4. 400~600자 분량의 한국어 요약문 작성

최종 응답은 반드시 한국어 요약문만 출력합니다. 도구 실행 과정은 설명하지 않습니다.\
"""


async def search_and_summarize(query: str, api_key: str) -> str:
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp@latest"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # MCP 서버에서 도구 목록 가져오기
            tools_response = await session.list_tools()
            tools = [
                {
                    "name": t.name,
                    "description": t.description or "",
                    "input_schema": t.inputSchema,
                }
                for t in tools_response.tools
            ]

            print(f"  사용 가능한 Playwright 도구: {len(tools)}개")

            client = anthropic.Anthropic(api_key=api_key)
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"위키피디아에서 '{query}'를 검색한 뒤, "
                        "첫 번째로 열리는 문서의 내용을 400~600자로 한국어 요약해 주세요."
                    ),
                }
            ]

            step = 0
            while True:
                step += 1
                print(f"  [단계 {step}] Claude 응답 생성 중...")

                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    tools=tools,
                    messages=messages,
                )

                # 최종 텍스트 응답
                if response.stop_reason == "end_turn":
                    for block in response.content:
                        if hasattr(block, "text"):
                            return block.text
                    return "(응답 없음)"

                # 도구 호출 처리
                tool_results = []
                has_tool_use = False

                for block in response.content:
                    if block.type == "tool_use":
                        has_tool_use = True
                        input_preview = json.dumps(block.input, ensure_ascii=False)[:60]
                        print(f"  [도구] {block.name}({input_preview})")

                        try:
                            result = await session.call_tool(block.name, block.input)
                            content = ""
                            if result.content:
                                content = result.content[0].text if hasattr(result.content[0], "text") else str(result.content[0])
                            # 너무 긴 내용은 잘라서 전달
                            content = content[:4000]
                        except Exception as e:
                            content = f"도구 실행 오류: {e}"

                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": content,
                            }
                        )

                if not has_tool_use:
                    # tool_use 없이 stop_reason이 다른 경우
                    for block in response.content:
                        if hasattr(block, "text"):
                            return block.text
                    return "(응답 없음)"

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

                if step > 20:
                    return "오류: 최대 반복 횟수 초과"


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "인공지능"
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if not api_key:
        print("=" * 55)
        print("오류: ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print("설정 방법:")
        print("  Windows: set ANTHROPIC_API_KEY=sk-ant-...")
        print("  실행:    python wiki_search.py <검색어>")
        print("=" * 55)
        sys.exit(1)

    print("\n" + "=" * 55)
    print(f"  위키피디아 검색: [{query}]")
    print("=" * 55)

    summary = asyncio.run(search_and_summarize(query, api_key))

    print("\n" + "=" * 55)
    print("  [요약 결과]")
    print("=" * 55)
    print(summary)
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
