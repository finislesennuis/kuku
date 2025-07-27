from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from importlib import import_module
schemas = import_module('schemas')
crud = import_module('crud')
from models import Place

router = APIRouter()

@router.get("/places/", response_model=list[schemas.Place])
@router.get("/places", response_model=list[schemas.Place])
def read_places(category: str = None, db: Session = Depends(get_db)):
    try:
        print(f"🔍 Places API 호출됨 - category: {category}")
        
        # 데이터베이스 연결 확인
        try:
            db.execute("SELECT 1")
            print("✅ 데이터베이스 연결 성공")
        except Exception as db_error:
            print(f"❌ 데이터베이스 연결 실패: {db_error}")
            raise HTTPException(status_code=500, detail=f"데이터베이스 연결 오류: {str(db_error)}")
        
        # Place 테이블 존재 확인
        try:
            place_count = db.query(Place).count()
            print(f"✅ Place 테이블 확인됨 - 총 {place_count}개 레코드")
        except Exception as table_error:
            print(f"❌ Place 테이블 오류: {table_error}")
            raise HTTPException(status_code=500, detail=f"Place 테이블 오류: {str(table_error)}")
        
        if category:
            places = crud.get_places_by_category(db, category)
            print(f"✅ 카테고리 '{category}'로 {len(places)}개 장소 조회 성공")
        else:
            places = crud.get_all_places(db)
            print(f"✅ 전체 {len(places)}개 장소 조회 성공")
        
        return places
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Places API 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")

@router.post("/places/", response_model=schemas.Place)
def create_place(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    return crud.create_place(db, place)

@router.get("/courses/", response_model=list[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)

@router.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)

@router.get("/courses/{course_id}/places", response_model=list[schemas.CoursePlace])
def read_course_places(course_id: int, db: Session = Depends(get_db)):
    return crud.get_places_by_course(db, course_id) 