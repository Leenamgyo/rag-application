
# 베이스가 될 Elasticsearch 공식 이미지를 지정합니다.
# .env 파일에 정의된 버전이 ${ELK_VERSION}으로 들어옵니다.
FROM docker.elastic.co/elasticsearch/elasticsearch:8.18.3

# 컨테이너 빌드 시점에 Nori 플러그인을 설치합니다.
RUN ./bin/elasticsearch-plugin install analysis-nori