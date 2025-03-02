ANALYZE_PROMPT = """
<input>{text}</input>
###TASK
- You are an assistant that analyzes news article and provides the following information:
1. Summary: You must summary base on the news content, write in semantic way
2. Title: The title that sum up the news content. Not exceed 50 characters
3. Keywords
4. Tags
5. Spelling: Check wrong pronunciation word and promote an alter word
6. Personage: Person name in <input>
- Input is in <input> tag

###CONSTRAIN
- Return in json only with the following format:
{{"summary": "text summary", "title": "the title", "keywords": ["kw1", "kw2"], "tags": ["tag1", "tag2"], "spelling": {{"wrong": "alter"}}, "personage": ["name1", "name2"]}}
- Language: Multilingual

###OUTPUT
```json
"""

SEO_PROMPT = """
###TASK
- You are search engine optimize(SEO) score analyzer, help me to scoring my article base on SEO criteria:
1. Keyword Usage
2. Readability
3. Content Length
4. Content Quality
- Input is in <input> tag

###CONSTRAIN
- Return in json only with the following format:
{{"seo_score": {{"keyword_use": 50, "readability": 50, "content_length": 50, "content_quality": 50}}}}
- Score Range: 0-100

<input>{text}</input>

###OUTPUT
```json
"""


SEGMENTATION_PROMPT = """
Act as a text analyzer to review, summarize, and segment the provided text, which is a subtitle from a reading article in .srt format.
- Where possible, merge shorter segments to create unified, complete ideas without losing meaning.
- Summary: Summarize each segment succinctly, capturing key points and ideas in a clear and concise manner.
Ensure the resulting segments retain the meaning and flow of the original text while improving readability.

Input Text:
{text}

{format_instructions}
"""


GRAMMAR_CHECK_PROMPT = """
Act as a grammar and spelling corrector. Read the input text and identify grammar and spelling errors.
Only indentify grammar and spelling errors for single words not multiple words.

Input text:
{text}

{format_instructions}
"""
