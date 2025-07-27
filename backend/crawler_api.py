from fastapi import APIRouter, BackgroundTasks, HTTPException
import requests
import logging
from typing import Optional
from config import settings
from database import SessionLocal
from models import Place, Festival, Course, CoursePlace, YouTubeLink, CrawlRequest, CrawledData

# 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# ngrok URL을 config에서 가져오기
LOCAL_CRAWLER_URL = settings.LOCAL_CRAWLER_URL

def clear_database():
    """데이터베이스의 모든 데이터를 삭제"""
    try:
        db = SessionLocal()
        db.query(Place).delete()
        db.query(CoursePlace).delete()
        db.query(Course).delete()
        db.query(Festival).delete()
        db.query(YouTubeLink).delete()
        db.query(CrawlRequest).delete()
        db.query(CrawledData).delete()
        db.commit()
        db.close()
        logger.info("데이터베이스 초기화 완료")
        return True
    except Exception as e:
        logger.error(f"데이터베이스 초기화 실패: {e}")
        return False

def request_local_crawler(type: str, url: Optional[str] = None, festival: Optional[str] = None, address: Optional[str] = None):
    """로컬 크롤러에 요청을 보내는 함수"""
    try:
        payload = {"type": type}
        if url:
            payload["url"] = url
        if festival:
            payload["festival"] = festival
        if address:
            payload["address"] = address
            
        response = requests.post(f"{LOCAL_CRAWLER_URL}/crawl", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"로컬 크롤러 연결 실패: {str(e)}")

@router.post("/crawl/sejong_festival")
async def crawl_sejong_festival():
    """세종축제 크롤링"""
    try:
        logger.info("세종축제 크롤링 요청")
        result = request_local_crawler(type="festival", url="https://sjfestival.kr")
        return {"message": "세종축제 크롤링 완료", "result": result}
    except Exception as e:
        logger.error(f"세종축제 크롤링 실패: {e}")
        raise HTTPException(status_code=500, detail=f"세종축제 크롤링 실패: {str(e)}")

@router.post("/crawl/light_festival")
async def crawl_light_festival():
    """세종 빛 축제 크롤링"""
    try:
        logger.info("세종 빛 축제 크롤링 요청")
        result = request_local_crawler(type="festival", url="https://sejong.go.kr/tour/sub02_0104.do")
        return {"message": "세종 빛 축제 크롤링 완료", "result": result}
    except Exception as e:
        logger.error(f"세종 빛 축제 크롤링 실패: {e}")
        raise HTTPException(status_code=500, detail=f"세종 빛 축제 크롤링 실패: {str(e)}")

@router.post("/crawl/fire_festival")
async def crawl_fire_festival():
    """세종 낙화축제 크롤링"""
    try:
        logger.info("세종 낙화축제 크롤링 요청")
        result = request_local_crawler(type="festival", url="https://sjcf.or.kr/content.do?key=2111060044")
        return {"message": "세종 낙화축제 크롤링 완료", "result": result}
    except Exception as e:
        logger.error(f"세종 낙화축제 크롤링 실패: {e}")
        raise HTTPException(status_code=500, detail=f"세종 낙화축제 크롤링 실패: {str(e)}")

@router.post("/crawl/peach_festival")
async def crawl_peach_festival():
    """조치원복숭아축제 크롤링"""
    try:
        logger.info("조치원복숭아축제 크롤링 요청")
        result = request_local_crawler(type="festival", url="https://jcwpeach.kr")
        return {"message": "조치원복숭아축제 크롤링 완료", "result": result}
    except Exception as e:
        logger.error(f"조치원복숭아축제 크롤링 실패: {e}")
        raise HTTPException(status_code=500, detail=f"조치원복숭아축제 크롤링 실패: {str(e)}")

@router.post("/crawl/courses")
async def crawl_courses():
    """여행코스 크롤링 실행 - 로컬 크롤러로 요청"""
    try:
        result = request_local_crawler(
            type="course", 
            url="https://sejong.go.kr/tour/sub02_020"
        )
        return {
            "message": "여행코스 크롤링이 시작되었습니다.",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"여행코스 크롤링 실패: {str(e)}")

from pydantic import BaseModel, Field

class PlacesRequest(BaseModel):
    festival: str = Field(..., description="축제 이름 (예: 세종축제, 조치원복숭아축제, 세종낙화축제, 세종 빛 축제)")

@router.post("/crawl/places")
async def crawl_places(request: PlacesRequest):
    """주변 장소 크롤링 실행 - 축제 이름만 입력하면 s_place.py의 저장된 주소로 자동 매핑"""
    try:
        festival = request.festival
        
        # s_place.py의 festivals 딕셔너리와 동일한 주소 매핑
        festival_addresses = {
            "세종축제": "세종특별자치시 세종동 1201",
            "조치원복숭아축제": "세종특별자치시 조치원읍 대첩로 98",
            "세종낙화축제": "세종특별자치시 세종동 1201",
            "세종 빛 축제": "세종특별자치시 보람동 623-1"
        }
        
        # 축제 이름으로 주소 자동 매핑
        address = festival_addresses.get(festival)
        if not address:
            raise HTTPException(status_code=400, detail=f"'{festival}' 축제의 주소 정보가 없습니다. 지원되는 축제: {list(festival_addresses.keys())}")
        
        result = request_local_crawler(
            type="places", 
            festival=festival, 
            address=address
        )
        return {
            "message": f"{festival} 주변 장소 크롤링이 시작되었습니다. (주소: {address})",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"주변 장소 크롤링 실패: {str(e)}")

@router.post("/crawl/all")
async def crawl_all():
    """모든 크롤링 실행 - 로컬 크롤러로 요청"""
    try:
        results = []
        
        # 축제들 크롤링
        results.append(request_local_crawler(type="festival", url="https://sjfestival.kr"))
        results.append(request_local_crawler(type="festival", url="https://sejong.go.kr/tour/sub02_0104.do"))
        results.append(request_local_crawler(type="festival", url="https://sjcf.or.kr/content.do?key=2111060044"))
        results.append(request_local_crawler(type="festival", url="https://jcwpeach.kr"))
        
        # 여행코스 크롤링
        results.append(request_local_crawler(type="course", url="https://sejong.go.kr/tour/sub02_020"))
        
        return {
            "message": "모든 크롤링이 시작되었습니다.",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"전체 크롤링 실패: {str(e)}")

@router.post("/crawl/all-with-clear")
async def crawl_all_with_clear():
    """데이터베이스 초기화 후 모든 크롤링 실행"""
    try:
        # 먼저 데이터베이스 초기화
        if clear_database():
            logger.info("데이터베이스 초기화 완료, 크롤링 시작")
        else:
            logger.warning("데이터베이스 초기화 실패, 기존 데이터 유지하며 크롤링")
        
        results = []
        
        # 축제들 크롤링
        results.append(request_local_crawler(type="festival", url="https://sjfestival.kr"))
        results.append(request_local_crawler(type="festival", url="https://sejong.go.kr/tour/sub02_0104.do"))
        results.append(request_local_crawler(type="festival", url="https://sjcf.or.kr/content.do?key=2111060044"))
        results.append(request_local_crawler(type="festival", url="https://jcwpeach.kr"))
        
        # 여행코스 크롤링
        results.append(request_local_crawler(type="course", url="https://sejong.go.kr/tour/sub02_020"))
        
        return {
            "message": "데이터베이스 초기화 후 모든 크롤링이 시작되었습니다.",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"전체 크롤링 실패: {str(e)}")

@router.post("/clear-database")
async def clear_database_endpoint():
    """데이터베이스 초기화 API"""
    try:
        if clear_database():
            return {"message": "데이터베이스 초기화 완료"}
        else:
            raise HTTPException(status_code=500, detail="데이터베이스 초기화 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 초기화 실패: {str(e)}")

@router.get("/crawl/status")
async def get_crawl_status():
    """로컬 크롤러 상태 확인"""
    try:
        response = requests.get(f"{LOCAL_CRAWLER_URL}/", timeout=5)
        return {"status": "connected", "local_crawler_url": LOCAL_CRAWLER_URL}
    except:
        return {"status": "disconnected", "local_crawler_url": LOCAL_CRAWLER_URL} 