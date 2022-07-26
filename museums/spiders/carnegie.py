import scrapy

import json
import logging

PER_PAGE = 100

class CarnegieSpider(scrapy.Spider):
    name = 'carnegie'
    allowed_domains = ['collection.cmoa.org', '530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io']
    start_urls = ['http://collection.cmoa.org/']
    headers = {
        'authority': '530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io:9243',
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': 'Basic Y29sbGVjdGlvbnM6bzQxS0chTW1KUSRBNjY=',
        'cache-control': 'no-cache',
        'content-type': 'application/x-ndjson',
        'origin': 'https://collection.cmoa.org',
        'pragma': 'no-cache',
        'referer': 'https://collection.cmoa.org/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    
    def create_search_api_request(self, from_idx):
        json_dict = {'_source': ['id', 'title', 'creators', 'creation_date', 'images', 'type'], 'query': {'function_score': {'query': {'bool': {'must': [{'match_all': {}}], 'filter': []}}, 'random_score': {'seed': 1658836199416, 'field': '_seq_no'}, 'boost_mode': 'replace'}}, 'aggs': {'uniqueClassification': {'terms': {'field': 'medium', 'order': {'_key': 'asc'}, 'shard_size': 2000, 'size': 500}}, 'uniqueDepartment': {'terms': {'field': 'department', 'order': {'_key': 'asc'}, 'shard_size': 2000, 'size': 500}}, 'uniqueLocation': {'terms': {'field': 'current_location', 'order': {'_key': 'asc'}, 'shard_size': 2000, 'size': 500}}, 'creators': {'nested': {'path': 'creators'}, 'aggs': {'uniqueCreator': {'terms': {'field': 'creators.label', 'order': {'_count': 'desc'}, 'shard_size': 2000, 'size': 500}, 'aggs': {'cited': {'terms': {'field': 'creators.cited_name'}, 'aggs': {'sort': {'terms': {'field': 'creators.cited_name.sort'}}}}}}, 'uniqueNationality': {'terms': {'field': 'creators.nationality', 'order': {'_key': 'asc'}, 'shard_size': 2000, 'size': 500}}}}}, 'sort': [{'_score': 'desc'}], 'size': 100, 'from': from_idx}

        json_str = json.dumps(json_dict)
        
        # XXX: is this big shebang needed here?
        body = '{}\n' + json_str + '''{}
{"_source":["id","title","creators","creation_date","images","type"],"query":{"function_score":{"query":{"bool":{"must":[{"term":{"department":"Fine Arts"}}],"filter":[]}},"random_score":{"seed":1658836199418,"field":"_seq_no"},"boost_mode":"replace"}},"from":0,"size":20}
{}
{"_source":["id","title","creators","creation_date","images","type"],"query":{"function_score":{"query":{"bool":{"must":[{"term":{"department":"Fine Arts: Teenie Harris Archive"}}],"filter":[]}},"random_score":{"seed":1658836199418,"field":"_seq_no"},"boost_mode":"replace"}},"from":0,"size":20}
{}
{"_source":["id","title","creators","creation_date","images","type"],"query":{"function_score":{"query":{"bool":{"must":[{"term":{"department":"Decorative Arts and Design"}}],"filter":[]}},"random_score":{"seed":1658836199418,"field":"_seq_no"},"boost_mode":"replace"}},"from":0,"size":20}
{}
{"_source":["id","title","creators","creation_date","images","type"],"query":{"function_score":{"query":{"bool":{"must":[{"term":{"department":"Film and Video"}}],"filter":[]}},"random_score":{"seed":1658836199418,"field":"_seq_no"},"boost_mode":"replace"}},"from":0,"size":10}
{}
{"_source":["id","title","creators","creation_date","images","type"],"query":{"function_score":{"query":{"bool":{"must":[{"term":{"department":"Heinz Architectural Center"}}],"filter":[]}},"random_score":{"seed":1658836199418,"field":"_seq_no"},"boost_mode":"replace"}},"from":0,"size":10}
{}
{"_source":["id","title","creators","creation_date","images","type"],"query":{"function_score":{"query":{"bool":{"must":[{"term":{"department":"Modern and Contemporary Art"}}],"filter":[]}},"random_score":{"seed":1658836199418,"field":"_seq_no"},"boost_mode":"replace"}},"from":0,"size":10}
{}
{"_source":["id","title","creators","creation_date","images","type"],"query":{"function_score":{"query":{"bool":{"must":[{"term":{"department":"Photography"}}],"filter":[]}},"random_score":{"seed":1658836199418,"field":"_seq_no"},"boost_mode":"replace"}},"from":0,"size":10}\n'''

        logging.debug(body)

        url = 'https://530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io:9243/cmoa_objects/_msearch'

        meta_dict = { 'from': from_idx }

        return scrapy.Request(url, method="POST", headers=self.headers, body=body, callback=self.parse_search_api_response, meta=meta_dict)

    def start_requests(self):
        yield self.create_search_api_request(0)

    def parse_search_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        for resp_dict in json_dict.get('responses', []):
            for hit_dict in resp_dict.get('hits', dict()).get('hits', []):
                source_id = hit_dict.get("_id")
                url = 'https://530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io:9243/cmoa_objects/object/{}/_source'.format(source_id.replace(":", "%3A").replace("/", "%2F"))
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_source_api_response)
        
        if len(json_dict.get('responses')) > 0 and len(json_dict.get('responses')[0].get('hits').get('hits')) == PER_PAGE:
            from_idx = response.meta.get('from')
            from_idx += PER_PAGE
            yield self.create_search_api_request(from_idx)

    def parse_source_api_response(self, response):
        pass

