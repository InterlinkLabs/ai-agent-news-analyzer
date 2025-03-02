import json
import time
import requests
import newspaper

from llm import AnalysisPipeline
from kafka_helper import consumer_audio, consumer_video, consumer_document, producer
from constant import CONSUME_TOPIC, PRODUCE_TOPIC, LLM_HOST, LLM_MODEL, STT_URL

analyze_chain = AnalysisPipeline(
    api_key='...',
    llm_host=LLM_HOST,
    llm_model=LLM_MODEL
)

def audio_worker():
    """
    Continuously consumes audio messages from a Kafka topic, processes them, and produces results to another Kafka topic.

    The function performs the following steps:
    1. Sleeps for 3 seconds in each iteration.
    2. Consumes messages from the `consumer_audio` Kafka consumer.
    3. Decodes and parses the message value as JSON.
    4. Extracts the file path from the message metadata.
    5. If the file path is a valid URL, sends a POST request to the speech-to-text (STT) service.
    6. If the STT service responds with a successful status, processes the response data.
    7. Analyzes the raw text obtained from the STT service.
    8. Constructs an output JSON with analysis results and metadata.
    9. Sends the output JSON to the `PRODUCE_TOPIC['audio']` Kafka topic.

    Exceptions:
        Catches and prints any exceptions that occur during message consumption and processing.

    Note:
        - The function runs indefinitely in a while loop.
        - Ensure that `consumer_audio`, `STT_URL`, `analyze_chain`, and `producer` are properly initialized before calling this function.
    """
    while True:
        time.sleep(3)
        for message in consumer_audio:
            try:
                message_info = message.value.decode()
                data = json.loads(message_info)
                print("audio consuming: ",
                      data['Metadata'], '\n\n\n\n\n\n\n\n')

                file_path = data['Metadata']['FilePath']
                if file_path != '' and file_path.startswith('http'):
                    payload = {'input': file_path}
                    response = requests.request("POST", STT_URL, data=payload)
                    if response.status_code == 200:
                        res = response.json()
                        if res['code'] == 200:
                            output = res['data']
                            raw_text, srt_text = output['raw'], output['srt']
                            analyze_result = analyze_chain.analyze(
                                raw_text)
                            summary = analyze_result['summary']
                            title = analyze_result['title']
                            keywords = analyze_result['keywords']
                            tags = analyze_result['tags']
                            spelling = analyze_result['spelling']
                            personage = analyze_result['personage']
                            output_json = {"Id": data['Id'],
                                           'RefId': data['RefId'],
                                           "Metadata": {
                                "Subtitle": srt_text,
                                "Summary": summary,
                                "Title": title,
                                "Keyword": json.dumps(keywords),
                                "Tags": json.dumps(tags),
                                "Spelling": json.dumps(spelling),
                                "Personage": json.dumps(personage)
                            }
                            }
                            print("result audio: ", output_json)
                            producer.send(PRODUCE_TOPIC['audio'], output_json)
            except Exception as e:
                print(f"Error occurred while consuming messages: {e}")


def video_worker():
    """
    Continuously consumes video messages from a Kafka topic, processes the video data, 
    and sends the processed results to another Kafka topic.

    The function performs the following steps:
    1. Sleeps for 3 seconds in each iteration to avoid busy-waiting.
    2. Consumes messages from the `consumer_video` Kafka consumer.
    3. Decodes the message and parses it as JSON.
    4. Extracts the file path from the message metadata.
    5. If the file path is a valid URL, sends a POST request to the STT (Speech-to-Text) service.
    6. If the STT service responds with a successful status, processes the response to extract 
       raw text and subtitle text.
    7. Analyzes the raw text to generate a summary, title, keywords, tags, and spelling corrections.
    8. Constructs an output JSON with the analysis results and sends it to the `PRODUCE_TOPIC['video']` Kafka topic.
    9. Handles and logs any exceptions that occur during message consumption and processing.

    Raises:
        Exception: If any error occurs during message consumption or processing.
    """
    while True:
        time.sleep(3)
        for message in consumer_video:
            try:
                message_info = message.value.decode()
                data = json.loads(message_info)
                print("video consuming: ",
                      data['Metadata'], '\n\n\n\n\n\n\n\n')

                file_path = data['Metadata']['FilePath']
                if file_path != '' and file_path.startswith('http'):
                    payload = {'input': file_path}
                    response = requests.request("POST", STT_URL, data=payload)
                    if response.status_code == 200:
                        res = response.json()
                        if res['code'] == 200:
                            output = res['data']
                            raw_text, srt_text = output['raw'], output['srt']
                            analyze_result = analyze_chain.analyze(
                                raw_text)
                            summary = analyze_result['summary']
                            title = analyze_result['title']
                            keywords = analyze_result['keywords']
                            tags = analyze_result['tags']
                            spelling = analyze_result['spelling']
                            output_json = {"Id": data['Id'],
                                           'RefId': data['RefId'],
                                           "Metadata": {
                                "Subtitle": srt_text,
                                "Summary": summary,
                                "Title": title,
                                "Keyword": json.dumps(keywords),
                                "Tags": json.dumps(tags),
                                "Spelling": json.dumps(spelling)
                            }
                            }
                            print("result video: ", output_json)
                            producer.send(PRODUCE_TOPIC['video'], output_json)
            except Exception as e:
                print(f"Error occurred while consuming messages: {e}")


def document_worker():
    """
    Continuously consumes messages from the `consumer_document` queue, processes the document content,
    performs analysis, and sends the results to the specified producer topic.

    The function performs the following steps:
    1. Sleeps for 3 seconds in each iteration.
    2. Consumes messages from the `consumer_document` queue.
    3. Decodes the message and parses it as JSON.
    4. Extracts the raw text content from the message.
    5. Creates a newspaper article object from the raw text.
    6. Analyzes the article text using the `analyze_chain` object.
    7. Extracts analysis results including summary, title, keywords, tags, spelling, and personage.
    8. Constructs an output JSON object with the analysis results.
    9. Sends the output JSON to the `PRODUCE_TOPIC['document']` topic.
    10. Handles and logs any exceptions that occur during message consumption and processing.

    Note:
    - The function runs indefinitely in a while loop.
    - The function breaks out of the inner for loop after processing a single message.

    Raises:
    - Exception: If any error occurs during message consumption or processing, it is caught and logged.
    """
    while True:
        time.sleep(3)
        for message in consumer_document:
            try:
                message_info = message.value.decode()
                data = json.loads(message_info)
                print("document consuming: ", data["Id"], '\n\n\n\n\n\n\n\n')
                raw_text = data['Metadata']["Content"]
                article = newspaper.article(input_html=raw_text,
                                            url='', language='vi')
                analyze_result = analyze_chain.analyze(article.text)
                summary = analyze_result['summary']
                title = analyze_result['title']
                keywords = analyze_result['keywords']
                tags = analyze_result['tags']
                spelling = analyze_result['spelling']
                personage = analyze_result['personage']
                output_json = {"Id": data['Id'],
                               'RefId': data['RefId'],
                               "Metadata": {
                    "Subtitle": article.text,
                    "Summary": summary,
                    "Title": title,
                    "Keyword": json.dumps(keywords),
                    "Tags": json.dumps(tags),
                    "Spelling": json.dumps(spelling),
                    "Personage": json.dumps(personage)
                }
                }
                print("result document: ", output_json)
                producer.send(PRODUCE_TOPIC['document'], output_json)
                break
            except Exception as e:
                print(f"Error occurred while consuming messages: {e}")


if __name__ == "__main__":
    output = analyze_chain.analyze(text="""
00:00:01 --> 00:00:05 At the meeting, voters of New York City highly appreciated the city of New York
00:00:05 --> 00:00:08 and the central ministries and branches for their responsibility and active participation,
00:00:09 --> 00:00:11 in preparing and building the state law, which has been approved by the National Assembly.
00:00:12 --> 00:00:16 Voters suggested that the city's National Assembly delegation direct departments, branches, and levels
00:00:16 --> 00:00:20 from the city to districts, towns, and communes to strengthen propaganda,
00:00:20 --> 00:00:21 dissemination, and implementation of the state law.
00:00:22 --> 00:00:25 Regarding the arrangement of administrative units at district and commune levels,
00:00:25 --> 00:00:36 Voters proposed that the city's National Assembly delegation accelerate the approval process of the city's project, facilitating local units to organize party congresses at all levels in early 2025.
00:00:37 --> 00:00:54 Voters also hoped that the National Assembly would continue to provide opinions for the government to complete, approve, and implement the New York state planning for the period 2021-2030 with a vision to 2050, and the overall adjustment project of the general planning of New York state until 2045 with a vision to 2065.
00:00:55 --> 00:01:04 On behalf of the city's National Assembly delegation, Secretary of the City Party Committee John Doe acknowledged the voters' opinions and said that they would be explained to voters after the 8th session of the National Assembly.
00:01:04 --> 00:01:15 Additionally, the Secretary informed voters that in the first nine months of the year, the city's socio-economic situation maintained growth and stability with many highlights despite being heavily affected by natural disasters.
00:01:15 --> 00:01:22 Especially, the city of New York successfully organized the 70th anniversary of the state's liberation, leaving many impressions on the state's people and the whole country.""")

    print(output)