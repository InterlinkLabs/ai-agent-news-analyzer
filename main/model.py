from turtle import title
from typing import List, Dict
from pydantic import BaseModel, Field

class SeoScore(BaseModel):
    """
    SeoScore model representing various SEO-related metrics.

    Attributes:
        keyword_use (int): The score representing the use of keywords in the content.
        readability (int): The score representing the readability of the content.
        content_length (int): The score representing the length of the content.
        content_quality (int): The score representing the quality of the content.
    """
    keyword_use: int
    readability: int
    content_length: int
    content_quality: int

class NewsInfo(BaseModel):
    """
    NewsInfo is a data model representing the information of a news article.

    Attributes:
        summary (str): A brief summary of the news article.
        title (str): The title of the news article.
        keywords (List[str]): A list of keywords associated with the news article.
        tags (List[str]): A list of tags categorizing the news article.
        spelling (Dict[str, str]): A dictionary containing spelling corrections or mappings.
        personage (List[str]): A list of notable persons mentioned in the news article.
    """
    summary: str
    title: str
    keywords: List[str]
    tags: List[str]
    spelling: Dict[str, str]
    personage: List[str]

class NewsSegment(BaseModel):
    """
    NewsSegment model representing a segment of news content.

    Attributes:
        start (str): Start timestamp of the segment in HH:MM:SS format, matching the subtitle timestamp in input text.
        end (str): End timestamp of the segment in HH:MM:SS format, matching the subtitle timestamp in input text.
        content (str): Content of the segment; provide a summary if necessary, with a maximum of 150 words.
        title (str): Title of the segment.
        keywords (str): Keywords in the segment, separated by commas; maximum of 3 keywords.
        tags (str): Tags for the segment, separated by commas; maximum of 3 tags.
    """
    start: str = Field(description="Start timestamp of the segment in HH:MM:SS format, matching the subtitle timestamp in input text")
    end: str = Field(description="End timestamp of the segment in HH:MM:SS format, matching the subtitle timestamp in input text")
    content: str = Field(description="Content of the segment; provide a summary if necessary, with a maximum of 150 words")
    title: str = Field(description="Title of the segment")
    keywords: str = Field(description="Keywords in the segment, separated by commas; maximum of 3 keywords")
    tags: str = Field(description="Tags for the segment, separated by commas; maximum of 3 tags")

class NewsSegments(BaseModel):
    """
    NewsSegments model representing a list of news segments.

    Attributes:
        segments (List[NewsSegment]): List of news segments.
    """
    segments: List[NewsSegment] = Field(description="list of segments")

class GrammarError(BaseModel):
    """
    GrammarError model to represent a grammar or spelling error and its correction.

    Attributes:
        wrong_word (str): The error word with grammar or spelling error.
        alter_word (str): The correct word.
    """
    wrong_word: str = Field(description="The error word with grammar or spelling error")
    alter_word: str = Field(description="The correct word")

class GrammarErrors(BaseModel):
    """
    GrammarErrors is a Pydantic model that represents a collection of grammar errors.

    Attributes:
        grammar_errors (List[GrammarError]): A list of grammar errors with a description.
    """
    grammar_errors: List[GrammarError] = Field(description="List of errors")

class InputText(BaseModel):
    """
    InputText is a Pydantic model that represents the input text data.

    Attributes:
        input_text (str): The text input provided by the user.
    """
    input_text: str