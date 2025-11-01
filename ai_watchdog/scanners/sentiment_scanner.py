from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel, Field
from typing import Optional

class SentimentAanalysisOutput(BaseModel):
    result: bool = Field(..., description='Returns true if sentiment is positive, false if the sentiment is negative')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "sentiment_scanner"
DEFAULT_MODE = "logic"
SCANNER_TYPE = ["input", "output"]
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = SentimentAanalysisOutput

def run_logic_based_scan(
    text: str
) :
    sid_object = SentimentIntensityAnalyzer()
    sentiment_dict = sid_object.polarity_scores(text)
    if sentiment_dict['compound'] >= 0.05:
        return SentimentAanalysisOutput(
            result=True,
            details="The overall sentiment of the text is positive."
        )

    elif sentiment_dict['compound'] <= -0.05:
        return SentimentAanalysisOutput(
            result=False,
            details="The overall sentiment of the text is negative."
        )
    else:
        return SentimentAanalysisOutput(
            result=True,
            details="The overall sentiment of the text is neutral."
        )
