---
name: wiki-search
description: |
  Playwright MCP를 활용해 위키피디아(Wikipedia)를 자동으로 탐색하고,
  첫 번째 검색 결과의 핵심 내용을 한국어로 요약해 응답하는 스킬.

  다음 상황에서 반드시 이 스킬을 사용할 것:
  - "위키피디아에서 ~검색해줘 / 찾아줘 / 알려줘"
  - "위키백과로 ~요약해줘 / 정리해줘"
  - "wikipedia에서 ~ 검색"
  - "wiki로 ~찾아봐"
  - 특정 개념·인물·사건에 대해 위키피디아 출처 정보를 요청하는 모든 경우
  - 검색어만 주어졌더라도 위키피디아 검색 의도가 명확하면 즉시 적용
---

# 위키피디아 검색 및 요약 스킬

Playwright MCP 브라우저 도구를 사용해 위키피디아를 직접 탐색하고,
첫 번째 문서의 본문을 추출한 뒤 한국어 요약문을 반환한다.

---

## 작업 흐름

### 1단계 — 위키피디아 메인 접속

```
mcp__playwright__browser_navigate  →  url: "https://www.wikipedia.org"
```

### 2단계 — 검색어 입력

```
mcp__playwright__browser_type
  target: 검색창 (searchbox "Search Wikipedia", ref e53 또는 동등한 ref)
  text: <사용자가 요청한 검색어>
```

언어 드롭다운이 한국어(ko)로 설정되어 있는지 확인한다.
설정되어 있지 않으면 드롭다운에서 한국어를 선택한 뒤 진행한다.

### 3단계 — 검색 실행

```
mcp__playwright__browser_click
  target: Search 버튼 (ref e59 또는 동등한 ref)
```

### 4단계 — 결과 확인 및 문서 이동

- 검색 후 **바로 문서 페이지**로 이동한 경우 → 5단계로 진행
- **검색 결과 목록**이 표시된 경우 → 첫 번째 항목을 클릭해 문서로 이동

### 5단계 — 본문 추출

`mcp__playwright__browser_evaluate`로 아래 JavaScript를 실행한다:

```javascript
() => {
  const title = document.querySelector('h1')?.textContent?.trim() || '';
  const url = location.href;
  const paras = Array.from(document.querySelectorAll('p'))
    .filter(p => p.textContent.trim().length > 50)
    .slice(0, 7)
    .map(p => p.textContent.trim().replace(/\[\d+\]/g, '').slice(0, 400));
  const headings = Array.from(document.querySelectorAll('h2'))
    .map(h => h.textContent.replace(/\[편집\]/g, '').trim())
    .filter(h => h && !['각주','같이 보기','외부 링크','목차'].some(x => h.includes(x)));
  return { title, url, paras, headings };
}
```

### 6단계 — 요약 작성 및 응답

추출한 `title`, `paras`, `headings`를 바탕으로 아래 형식에 맞게 응답한다.

---

## 출력 형식

```
## [문서 제목]
**출처**: [페이지 URL]

[400~600자 한국어 요약문]

**주요 섹션**: [섹션1], [섹션2], ...
```

요약문 작성 원칙:
- 개념 정의 → 핵심 원리/특징 → 활용 분야 또는 역사적 맥락 순으로 서술
- 각주 번호([1], [2] 등)는 모두 제거
- 전문 용어는 원어 병기 허용 (예: 큐비트(qubit))
- 도구 실행 과정과 중간 단계는 최종 응답에 포함하지 않음

---

## 주의사항

- `browser_evaluate` 결과의 `paras[0]`이 CSS·광고 텍스트인 경우 해당 항목을 건너뛰고
  실제 본문 단락부터 사용한다.
- 검색어가 모호해 여러 동음이의어 문서가 존재할 경우, 가장 일반적인 의미의 문서를 선택한다.
- 페이지 로딩이 느릴 경우 `browser_wait_for`로 대기 후 재시도한다.
