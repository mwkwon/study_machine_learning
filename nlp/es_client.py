from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search, Q

class ElasticsearchClient:

    def __init__(self, url: str, username: str, password: str):
        """
        :param url: elasticsearch url 정보
        :param username: 계정명
        :param password: 비밀번호
        """
        self.es_client = Elasticsearch(url, http_auth=(username, password))

    def search(self, index_name: str, query: dict, scroll_time_value: str = None):
        """
        검색
        :param index_name: 검색할 인덱스명
        :param query: 검색 쿼리 dictionary
        :param scroll_time_value: scroll api 사용 시 설정 scroll time value string ex: 5m
        :return: 검색 결과 search_response 객체
        """
        return self.es_client.search(index=index_name, body=query, scroll=scroll_time_value)

    def search_scroll(self, scroll_id: str, scroll_time_Value: str):
        """
        scroll id를 이용하여 검색
        :param scroll_id: 검색 시 반환 받은 scroll id 문자열
        :param scroll_time_Value: scroll api 사용 시 설정 scroll time value string ex: 5m
        :return: 검색 결과 search_response 객체
        """
        return self.es_client.scroll(scroll_id=scroll_id, scroll=scroll_time_Value)

    def exists_index(self, index_name: str):
        """
        검색엔진에 인덱스 존재 여부 확인
        :param index_name: 존재 여부를 확인할 인덱스명
        :return: True(존재 시), False(미 존재 시)
        """
        return self.es_client.indices.exists(index=index_name)

    def create_index(self, index_name: str, mappings: dict):
        """
        검색엔진에 인덱스 생성
        :param index_name: 생성할 인덱스명
        :param mappings: 생성 시 설정할 mapping, setting 정보 dictionary
        :return: 생성 결과가 담겨 있는 dictionary
        {
            'acknowledged': True,
            'shards_acknowledged': True,
            'index': 'index_name'
        }
        """
        return self.es_client.indices.create(index=index_name, body=mappings)

    def bulk_index(self, docs: list):
        """
        대량 색인 처리
        :param docs: 색인할 document list
        :return: success -> 성공 갯수, errors -> 에러 발생 시 에러 객체가 담겨 있는 list
        """
        success, errors = helpers.bulk(self.es_client, docs)
        return success, errors

    def exists_alias(self, alias_name: str):
        """
        alias 존재 여부 확인
        :param alias_name: 존재 여부를 확인할 alias명
        :return: True(존재 시), False(미 존재 시)
        """
        return self.es_client.indices.exists_alias(alias_name)

    def get_alias_indices(self, alias_name: str):
        """
        alias가 설정되어 있는 index list 조회
        :param alias_name: 대상 alias명
        :return: alias가 가지고 있는 index명 list
        ['jn3_dev_product_cafe_20200210',
         'jn3_dev_product_cafe_20200211',
         'jn3_dev_product_cafe_20200212',
         'jn3_dev_product_cafe_20200213',
         'jn3_dev_product_cafe_20200214',
         'jn3_dev_product_cafe_20200215',
         'jn3_dev_product_cafe_20200216',
         'jn3_dev_product_cafe_20200217',
         'jn3_dev_product_cafe_20200218',
         'jn3_dev_product_cafe_20200219',
         'jn3_dev_product_cafe_20200220',
         'jn3_dev_product_cafe_20200222',
         'jn3_dev_product_cafe_20200223',
         'jn3_dev_product_cafe_20200224',
         'jn3_dev_product_cafe_20200225',
         'jn3_product_202102190400']
        """
        return list(self.es_client.indices.get(alias_name).keys())

    def update_aliases(self, action: dict):
        return self.es_client.indices.update_aliases(action)['acknowledged']
    
    def scan_search(self, index_name, query: Q, source: list = None):
        s = Search(using=self.es_client, index=index_name).query(query).source(source)
        return [hit.to_dict() for hit in s.scan()]