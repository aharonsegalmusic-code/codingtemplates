"""
loads env 
    -   related to kafka
    READ TOPIC: "RAW"
    READ TOPIC: "Clean"
    READ TOPIC: "Analytic"
    KAFKA_GROUP_INDEXER: "Indexer"

    - elastic search env



get from -> raw topic

    {'image_id': '32421f607e5c7b53',
    'metadata': {'file_size': 17036,
                'filename': 'tweet_0.png',
                'format': 'PNG',
                'height': 300,
                'mode': 'RGB',
                'width': 600},
    'raw_text': '2020-02-15 17:57:21+00:00\n'
                '\n'
                'AIPAC should be registered as a foreign agent meddling in US\n'
                'elections. American Israel Political Action Committee. It is\n'
                'interfering in the US electoral process and should be put on '
                'trial\n'
                "and it's leaders imprisoned. @benshapiro @charliekirk11\n"
                'https://t.cofebO4iPUah8\n'}
"""
import os


class elasticConfig:

    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
        self.indexer_group = os.getenv("KAFKA_GROUP_INDEXER", "Indexer")
        self.kafka_topics_raw_clean = [os.getenv("KAFKA_TOPIC_RAW", "raw"),os.getenv("KAFKA_TOPIC_CLEAN", "clean")]
        self.es_index = os.getenv("ELASTICSEARCH_INDEX", "images")

        self.mapping =   {
                        "mappings": {
                            "properties": {
                                'image_id':     {"type": "keyword"},  
                                'filename':     {"type": "keyword"},     
                                'format':       {"type": "keyword"}, 
                                'height':       {"type": "integer"}, 
                                'mode':         {"type": "keyword"},   
                                'width':        {"type": "integer"}, 
                                'raw_text':     {"type": "text"}, 
                                'clean_text':   {"type": "text"}, 
                            }
                        }
                    }


