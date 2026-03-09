"""
RAW event processor
this is the format consumed from kafka

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
from clean_orchestrator import orchestrator, _config

orchestrator.start_cleaning(_config.kafka_topic_raw)
