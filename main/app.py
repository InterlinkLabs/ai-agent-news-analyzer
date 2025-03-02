from kafka_helper import consumer_audio, consumer_video, consumer_document
"""
This script initializes and starts three separate threads to handle audio, video, and document processing using 
Kafka consumers. The threads run continuously until a KeyboardInterrupt is received, at which point the Kafka 
consumers are closed and the threads are joined with a timeout.

Modules:
    kafka_helper: Contains Kafka consumer instances for audio, video, and document processing.
    workers: Contains worker functions for processing audio, video, and documents.

Functions:
    audio_worker: Function to process audio data.
    video_worker: Function to process video data.
    document_worker: Function to process document data.

Threads:
    thread1: Thread to run the audio_worker function.
    thread2: Thread to run the video_worker function.
    thread3: Thread to run the document_worker function.

Execution:
    The script starts the threads and keeps the main program running with an infinite loop. 
    On receiving a KeyboardInterrupt, it closes the Kafka consumers and joins the threads with a timeout.
"""
from workers import audio_worker, video_worker, document_worker
import threading
import time

thread1 = threading.Thread(target=audio_worker)
thread2 = threading.Thread(target=video_worker)
thread3 = threading.Thread(target=document_worker)

# Start the threads
thread1.start()
thread2.start()
thread3.start()

try:
    # Keep the main program running to allow threads to continue working
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    consumer_audio.close()
    consumer_video.close()
    consumer_document.close()
    # Optionally, join threads if you want to wait for them to finish after cleanup
    thread1.join(timeout=1)
    thread2.join(timeout=1)
    thread3.join(timeout=1)

    print("All functions have been terminated.")