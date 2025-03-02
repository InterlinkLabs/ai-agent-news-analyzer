import os
from pydantic import BaseSettings, validator, ValidationError

class Settings(BaseSettings):
    """
    Settings class for configuring the application.

    Attributes:
        KAFKA_SERVER (str): The Kafka server URL.
        CONSUME_TOPIC (dict): Dictionary of topics to consume from.
        PRODUCE_TOPIC (dict): Dictionary of topics to produce to.
        LLM_HOST (str): The host URL for the language model.
        LLM_MODEL (str): The specific language model to use.
        STT_URL (str): The URL for the speech-to-text service.

    Methods:
        validate_url(cls, v):
            Validates that the given URL starts with 'http://' or 'https://'.
            Raises:
                ValueError: If the URL does not start with 'http://' or 'https://'.

        validate_topics(cls, v):
            Validates that the given value is a dictionary.
            Raises:
                ValueError: If the value is not a dictionary.
    """
    KAFKA_SERVER: str
    CONSUME_TOPIC: dict
    PRODUCE_TOPIC: dict
    LLM_HOST: str
    LLM_MODEL: str
    STT_URL: str

    @validator('KAFKA_SERVER', 'LLM_HOST', 'STT_URL')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('must be a valid URL')
        return v

    @validator('CONSUME_TOPIC', 'PRODUCE_TOPIC')
    def validate_topics(cls, v):
        if not isinstance(v, dict):
            raise ValueError('must be a dictionary')
        return v

try:
    settings = Settings(
        KAFKA_SERVER=os.getenv('KAFKA_SERVER'),
        CONSUME_TOPIC={
            'audio': os.getenv('CONSUME_TOPIC_AUDIO'),
            'video': os.getenv('CONSUME_TOPIC_VIDEO'),
            'document': os.getenv('CONSUME_TOPIC_DOCUMENT')
        },
        PRODUCE_TOPIC={
            'audio': os.getenv('PRODUCE_TOPIC_AUDIO'),
            'video': os.getenv('PRODUCE_TOPIC_VIDEO'),
            'document': os.getenv('PRODUCE_TOPIC_DOCUMENT')
        },
        LLM_HOST=os.getenv('LLM_HOST'),
        LLM_MODEL=os.getenv('LLM_MODEL'),
        STT_URL=os.getenv('STT_URL')
    )
except ValidationError as e:
    print(f"Configuration error: {e}")

# Example usage with added print text
print(f"KAFKA_SERVER: {settings.KAFKA_SERVER}")
print(f"CONSUME_TOPIC: {settings.CONSUME_TOPIC}")
print(f"PRODUCE_TOPIC: {settings.PRODUCE_TOPIC}")
print(f"LLM_HOST: {settings.LLM_HOST}")
print(f"LLM_MODEL: {settings.LLM_MODEL}")
print(f"STT_URL: {settings.STT_URL}")