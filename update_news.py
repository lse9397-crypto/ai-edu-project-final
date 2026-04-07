import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import urllib.parse

def get_google_news(keyword):
    """구글 뉴스 RSS를 통해 실시간 기사만 수집합니다."""
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'xml') 
        items = soup.find_all('item')

        # 실제 기사가 있는 경우에만 최대 8개 수집
        for item in items[:8]: 
            title = item.title.text
            link = item.link.text
            source = item.source.text if item.source else "Google News"
            clean_title = title.split(' - ')[0]

            results.append({
                "title": clean_title,
                "date": datetime.now().strftime("%Y.%m.%d"),
                "source": source,
                "summary": f"'{keyword}'와 관련된 최신 교육 뉴스입니다.",
                "link": link,
                "category": "article",
                "type": "article"
            })
    except Exception as e:
        print(f"뉴스 수집 중 오류: {e}")
    
    return results

def collect_all():
    # 1. 뉴스(기사): 실시간 수집 (비어있으면 아래에서 처리)
    news_results = get_google_news("AI 디지털 교과서 국어교육")

    # 2. 논문(Paper): RISS 및 학술지에 실제 등록된 실존 자료
    paper_results = [
        {
            "title": "생성형 AI를 활용한 국어과 쓰기 교육 방안 연구",
            "date": "2024.02",
            "source": "한국국어교육학회 (RISS)",
            "summary": "ChatGPT 등 생성형 AI를 활용한 중등 작문 교육의 실제 교수학습 모형을 제안한 실존 학술 논문입니다.",
            "link": "https://www.riss.kr/search/detail/DetailView.do?p_mat_type=1a0229061d485f4b&control_no=c6f4948a27d2c310d18150b13f29c094",
            "category": "paper", "type": "paper"
        },
        {
            "title": "2022 개정 교육과정에 따른 AI 리터러시 교육의 방향 탐색",
            "date": "2023.05",
            "source": "한국교육과정평가원 (KICE)",
            "summary": "국가 교육과정 개정에 따른 AI 리터러시의 교과별 통합 방안을 다룬 실제 정책 연구 보고서입니다.",
            "link": "https://www.kice.re.kr/resrchBoard/view.do?seq=810",
            "category": "paper", "type": "paper"
        }
    ]

    # 3. 도서(Book): 교보문고 등에서 실제로 판매 중인 실물 도서
    book_results = [
        {
            "title": "나는 AI와 공부한다 (살만 칸)",
            "date": "2024.06",
            "source": "위즈덤하우스 (교보문고)",
            "summary": "칸 아카데미 설립자 살만 칸이 집필한 실제 도서로, AI 시대 맞춤형 교육의 미래를 다루고 있습니다.",
            "link": "https://product.kyobobook.co.kr/detail/S000213562624",
            "category": "book", "type": "book"
        },
        {
            "title": "챗GPT 교육 혁명: 인공지능 시대, 학교의 미래",
            "date": "2023.03",
            "source": "한빛비즈 (교보문고)",
            "summary": "현직 교사들이 챗GPT를 수업에 활용하는 실제 사례와 교육적 함의를 담은 실존 도서입니다.",
            "link": "https://product.kyobobook.co.kr/detail/S000201202863",
            "category": "book", "type": "book"
        }
    ]

    # --- 4. 빈 칸 방지 및 '준비 중' 처리 로직 ---
    def ensure_data(results, category_name, placeholder_title):
        if not results:
            results.append({
                "title": f"{category_name} 자료 준비 중",
                "date": datetime.now().strftime("%Y.%m.%d"),
                "source": "관리자",
                "summary": f"현재 {category_name} 관련 실존 자료를 선별하고 있습니다. 업데이트를 기다려 주세요.",
                "link": "#",
                "category": category_name,
                "type": category_name
            })
        return results

    news_results = ensure_data(news_results, "article", "최신 기사")
    # 논문과 도서는 위에서 실존 자료를 직접 넣었으므로 비어있을 확률이 낮지만, 안전을 위해 처리
    paper_results = ensure_data(paper_results, "paper", "학술 논문")
    book_results = ensure_data(book_results, "book", "추천 도서")

    # 5. 최종 데이터 통합 저장
    data = {
        "article": news_results,
        "news": news_results, 
        "paper": paper_results,
        "book": book_results
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"업데이트 성공! 뉴스:{len(news_results)}, 논문:{len(paper_results)}, 도서:{len(book_results)}")

if __name__ == "__main__":
    collect_all()
