from pydantic import BaseModel
from typing import List, Union, Optional

class PlaceBase(BaseModel):
    name: str
    category: str
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    url: Optional[str] = None

class PlaceCreate(PlaceBase):
    pass

class Place(PlaceBase):
    id: int
    class Config:
        orm_mode = True

class FestivalBase(BaseModel):
    name: str
    date: str
    time: str
    location: str
    description: Optional[str] = None  # 실제 DB 테이블 구조에 맞게 수정
    contact: Optional[str] = None
    image_url: Optional[str] = None
    programs: Optional[str] = None
    url: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class FestivalCreate(FestivalBase):
    pass

class Festival(FestivalBase):
    id: int

    class Config:
        orm_mode = True

class YouTubeLinkBase(BaseModel):
    title: str
    url: str
    description: str
    created_at: str

class YouTubeLinkCreate(YouTubeLinkBase):
    pass

class YouTubeLink(YouTubeLinkBase):
    id: int

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str
    img: Optional[str] = None
    detail_url: Optional[str] = None

class CourseCreate(CourseBase):
    places: List[str]

class Course(CourseBase):
    id: int
    class Config:
        orm_mode = True

class CoursePlaceBase(BaseModel):
    course_id: int
    place_name: str

class CoursePlaceCreate(CoursePlaceBase):
    pass

class CoursePlace(CoursePlaceBase):
    id: int
    class Config:
        orm_mode = True
