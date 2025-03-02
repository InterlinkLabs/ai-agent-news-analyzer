from math import gamma
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from concurrent.futures import ThreadPoolExecutor
from langchain_core.output_parsers import JsonOutputParser
from prompt import (
    ANALYZE_PROMPT,
    SEO_PROMPT,
    SEGMENTATION_PROMPT,
    GRAMMAR_CHECK_PROMPT
)
from model import (
    NewsInfo,
    InputText,
    SeoScore,
    NewsSegments,
    GrammarErrors
)

class AnalysisPipeline:
    """
    A class to handle the analysis pipeline for text using OpenAI's language model.
    Attributes:
        api_key (str): The API key for accessing the OpenAI service.
        llm_model (str): The language model to be used.
        llm_host (str): The host URL for the language model.
    Methods:
        segment_text(text: str) -> NewsSegments:
            Segments the input text into news segments.
        grammar_check(text: str) -> GrammarErrors:
            Checks the input text for grammar errors.
        analyze_text(text: str) -> NewsInfo:
            Analyzes the input text to extract news information.
        analyze(text: str) -> dict:
            Performs text analysis, grammar check, and segmentation concurrently and returns the combined result.
    """
    def __init__(
        self,
        api_key, 
        llm_model, 
        llm_host
    ):
        self.api_key = api_key
        self.llm_model = llm_model
        self.llm_host = llm_host

        # Initialize the OpenAI ChatCompletion instance
        self.openai_llm = ChatOpenAI(
            model=llm_model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key,
            base_url=llm_host,
        )

        # Define the prompt templates
        self.seo_prompt = PromptTemplate(
            input_variables=["text"],
            template=SEO_PROMPT
        )

    def segment_text(self, text: str) -> NewsSegments:
        """
        Segments the given text into news segments using a predefined prompt template and OpenAI language model.

        Args:
            text (str): The input text to be segmented.

        Returns:
            NewsSegments: The segmented news content as a NewsSegments object.
        """
        parser = JsonOutputParser(pydantic_object=NewsSegments)
        prompt = PromptTemplate(
            template=SEGMENTATION_PROMPT,
            input_variables=['text'],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = prompt | self.openai_llm | parser
        result = chain.invoke({"text": text})
        return result

    def grammar_check(self, text: str) -> GrammarErrors:
        """
        Checks the grammar of the given text using a language model.

        Args:
            text (str): The text to be checked for grammar errors.

        Returns:
            GrammarErrors: An object containing the grammar errors found in the text.
        """
        parser = JsonOutputParser(pydantic_object=GrammarErrors)
        prompt = PromptTemplate(
            template=GRAMMAR_CHECK_PROMPT,
            input_variables=['text'],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = prompt | self.openai_llm | parser
        result = chain.invoke({"text": text})
        return result
    
    def analyze_text(self, text: str) -> NewsInfo:
        """
        Analyzes the given text and extracts news information.

        Args:
            text (str): The text to be analyzed.

        Returns:
            NewsInfo: The extracted news information as a NewsInfo object.
        """
        prompt = PromptTemplate(
            input_variables=["text"],
            template=ANALYZE_PROMPT
        )
        parser = JsonOutputParser(pydantic_object=NewsInfo)
        chain = prompt | self.openai_llm | parser
        result = chain.invoke({"text": text})
        return result
    
    def analyze(self, text: str) -> dict:
        """
        Analyzes the given text using multiple concurrent tasks.
        This method performs text analysis, grammar checking, and text segmentation
        concurrently using a ThreadPoolExecutor. The results from these tasks are
        then combined into a single dictionary and returned.
        Args:
            text (str): The text to be analyzed.
        Returns:
            dict: A dictionary containing the combined results of the text analysis,
                  grammar check, and text segmentation.
        """
        with ThreadPoolExecutor() as executor:
            analyze_future = executor.submit(self.analyze_text, text)
            grammar_future = executor.submit(self.grammar_check, text)
            segments_future = executor.submit(self.segment_text, text)

            analyze_result = analyze_future.result()
            grammar_errors = grammar_future.result()
            segments = segments_future.result()
            
            result = {
                **analyze_result,
                **segments,
                **grammar_errors
            }

            return result

