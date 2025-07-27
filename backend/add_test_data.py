from database import SessionLocal
from models import Festival
from datetime import datetime

def add_test_festivals():
    db = SessionLocal()
    
    try:
        # 기존 데이터 확인
        existing_count = db.query(Festival).count()
        print(f"기존 축제 데이터: {existing_count}개")
        
        if existing_count > 0:
            print("이미 데이터가 존재합니다.")
            return
        
        # 테스트 축제 데이터 추가
        test_festivals = [
            Festival(
                name="세종시 봄꽃 축제",
                date="2025.03.15 ~ 2025.03.30",
                time="10:00 ~ 18:00",
                location="세종시 정부청사 주변",
                description="봄의 시작을 알리는 아름다운 벚꽃 축제입니다.",
                contact="044-123-4567",
                image_url="src/assets/nav/test.svg",
                programs="벚꽃 감상, 사진 촬영, 음악 공연",
                url="https://example.com/spring-festival",
                lat=36.5044,
                lng=127.2644
            ),
            Festival(
                name="세종시 여름 음악 축제",
                date="2025.07.20 ~ 2025.07.27",
                time="19:00 ~ 22:00",
                location="세종시 중앙공원",
                description="시원한 여름밤을 즐기는 음악 축제입니다.",
                contact="044-234-5678",
                image_url="src/assets/nav/test.svg",
                programs="재즈 공연, 팝 음악, 클래식",
                url="https://example.com/summer-music",
                lat=36.5044,
                lng=127.2644
            ),
            Festival(
                name="세종시 가을 문화 축제",
                date="2025.10.10 ~ 2025.10.20",
                time="09:00 ~ 21:00",
                location="세종시 문화회관",
                description="다양한 문화 프로그램을 즐길 수 있는 축제입니다.",
                contact="044-345-6789",
                image_url="src/assets/nav/test.svg",
                programs="전시회, 공연, 체험 프로그램",
                url="https://example.com/autumn-culture",
                lat=36.5044,
                lng=127.2644
            ),
            Festival(
                name="세종시 겨울 빛 축제",
                date="2025.12.20 ~ 2026.01.05",
                time="17:00 ~ 23:00",
                location="세종시 정부청사 광장",
                description="겨울밤을 밝히는 아름다운 빛 축제입니다.",
                contact="044-456-7890",
                image_url="src/assets/nav/test.svg",
                programs="조명 설치, 겨울 놀이, 새해 카운트다운",
                url="https://example.com/winter-light",
                lat=36.5044,
                lng=127.2644
            )
        ]
        
        for festival in test_festivals:
            db.add(festival)
        
        db.commit()
        print(f"✅ {len(test_festivals)}개의 테스트 축제 데이터 추가 완료!")
        
        # 추가된 데이터 확인
        total_count = db.query(Festival).count()
        print(f"총 축제 데이터: {total_count}개")
        
    except Exception as e:
        print(f"❌ 데이터 추가 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_festivals() 