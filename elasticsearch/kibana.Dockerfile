
# 베이스가 될 Kibana 공식 이미지를 지정합니다.
# .env 파일에 정의된 버전이 ${ELK_VERSION}으로 들어옵니다.
FROM docker.elastic.co/kibana/kibana:8.18.3