from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import festivals, links, search
from places import router as places_router
from crawler_api import router as crawler_router

from models import Festival, Place, Course
from database import Base, engine, SessionLocal
from config import settings

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 초기 데이터 확인
def check_initial_data():
    try:
        db = SessionLocal()
        
        # 테이블 존재 확인
        festival_count = db.query(Festival).count()
        place_count = db.query(Place).count()
        course_count = db.query(Course).count()
        
        print(f"📊 초기 데이터 확인:")
        print(f"   - 축제: {festival_count}개")
        print(f"   - 장소: {place_count}개")
        print(f"   - 코스: {course_count}개")
        
        if place_count == 0:
            print("⚠️  Place 테이블에 데이터가 없습니다!")
        
        db.close()
    except Exception as e:
        print(f"❌ 초기 데이터 확인 오류: {e}")

check_initial_data()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="세종시 축제 및 관광 정보 API"
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(festivals.router, prefix="/api", tags=["festivals"])
app.include_router(links.router, prefix="/api", tags=["links"])
app.include_router(places_router, prefix="/api", tags=["places"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(crawler_router, prefix="/api", tags=["crawlers"])

@app.get("/")
def root():
    return {
        "message": "세모(세종에서 모하지) 백엔드 API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/debug/db")
def debug_db():
    """DB 연결 및 데이터 조회 디버깅"""
    try:
        from database import SessionLocal
        from models import Festival
        
        db = SessionLocal()
        festivals = db.query(Festival).all()
        db.close()
        
        return {
            "status": "success",
            "festival_count": len(festivals),
            "festivals": [
                {
                    "id": f.id,
                    "name": f.name,
                    "date": f.date,
                    "description": f.description
                } for f in festivals
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
