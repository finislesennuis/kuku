from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from importlib import import_module
crud = import_module('crud')
from models import Festival, Place, Course

router = APIRouter()

@router.get("/search")
def search_all(
    q: str = Query(..., description="검색어"),
    db: Session = Depends(get_db)
):
    """
    축제, 장소, 코스에서 검색어를 포함하는 항목들을 검색
    """
    try:
        print(f"🔍 Search API 호출됨 - 검색어: {q}")
        
        # 데이터베이스 연결 확인
        try:
            db.execute("SELECT 1")
            print("✅ 데이터베이스 연결 성공")
        except Exception as db_error:
            print(f"❌ 데이터베이스 연결 실패: {db_error}")
            raise HTTPException(status_code=500, detail=f"데이터베이스 연결 오류: {str(db_error)}")
        
        results = {
            "festivals": [],
            "places": [],
            "courses": []
        }
        
        # 축제 검색
        try:
            festivals = db.query(Festival).filter(
                Festival.name.contains(q) | 
                Festival.description.contains(q) |
                Festival.location.contains(q)
            ).all()
            results["festivals"] = [
                {
                    "id": f.id,
                    "name": f.name,
                    "date": f.date,
                    "location": f.location,
                    "image_url": f.image_url,
                    "type": "festival"
                }
                for f in festivals
            ]
            print(f"✅ 축제 검색 완료: {len(results['festivals'])}개")
        except Exception as festival_error:
            print(f"❌ 축제 검색 오류: {festival_error}")
            results["festivals"] = []
        
        # 장소 검색
        try:
            places = db.query(Place).filter(
                Place.name.contains(q) | 
                Place.description.contains(q) |
                Place.category.contains(q)
            ).all()
            results["places"] = [
                {
                    "id": p.id,
                    "name": p.name,
                    "category": p.category,
                    "address": p.address,
                    "type": "place"
                }
                for p in places
            ]
            print(f"✅ 장소 검색 완료: {len(results['places'])}개")
        except Exception as place_error:
            print(f"❌ 장소 검색 오류: {place_error}")
            results["places"] = []
        
        # 코스 검색
        try:
            courses = db.query(Course).filter(
                Course.name.contains(q)
            ).all()
            results["courses"] = [
                {
                    "id": c.id,
                    "name": c.name,
                    "img": c.img,
                    "type": "course"
                }
                for c in courses
            ]
            print(f"✅ 코스 검색 완료: {len(results['courses'])}개")
        except Exception as course_error:
            print(f"❌ 코스 검색 오류: {course_error}")
            results["courses"] = []
        
        print(f"✅ 검색 완료 - 총 결과: {len(results['festivals']) + len(results['places']) + len(results['courses'])}개")
        return results
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Search API 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"검색 오류: {str(e)}") 