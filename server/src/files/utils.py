import uuid
import os

def generate_uuid_stored_filename(original_filename: str) -> str:
    """
    원본 파일명을 기반으로 고유한 저장용 파일명을 생성합니다.
    (예: 'my_image.jpg' -> 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.jpg')

    :param original_filename: 사용자가 업로드한 원본 파일명
    :return: UUID와 원본 확장자로 조합된 새로운 파일명
    """
    # 파일 확장자 추출 (예: '.jpg')
    _, extension = os.path.splitext(original_filename)
    
    # UUID를 생성하고 확장자를 붙여 고유한 파일명 생성
    unique_filename = f"{uuid.uuid4()}{extension}"
    
    return unique_filename