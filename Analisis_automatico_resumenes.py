import sumy.summarizers.text_rank as TextRankSummarizer
import sumy.summarizers.lsa       as LsaSummarizer
import sumy.parsers.plaintext     as PlaintTextParser
import sumy.nlp.tokenizers        as Tokenizer
import pandas                     as pd
import numpy                      as np
import textwrap
import nltk
import operator
from rouge_score import rouge_scorer
from functools   import reduce

nltk.download('punkt')

AMOUNT_LINES_PER_SUMMARY = 5
AMOUNT_SUMMARIES = 30
SUMMARIZERS = [
    TextRankSummarizer.TextRankSummarizer(),
    LsaSummarizer.LsaSummarizer()
]

def makeSummary(doc2summarize, summarizer, language):
    parser = PlaintTextParser.PlaintextParser.from_string(
        doc2summarize,
        Tokenizer.Tokenizer(language)
    )
    summaryOBJ = summarizer(parser.document, sentences_count=AMOUNT_LINES_PER_SUMMARY)
    return reduce(operator.add, map(lambda x: str(x)+"\n", summaryOBJ), "")

def main():
    dataFrame = pd.read_csv("./datos/test.csv")
    language  = "english"

    rng = np.random.default_rng()
    amount_news   = dataFrame.shape[0]
    selected_news = rng.integers(
        amount_news, size = (AMOUNT_SUMMARIES,)
    )
    entry = dataFrame.iloc[selected_news]
    docs  = entry["article"]
    humanSummaries = entry["highlights"]

    for summarizer in SUMMARIZERS:
        for doc in docs:
            makeSummary(doc, summarizer, language)
    
    #Rouge
    #scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'])

    #scores = scorer.score(humanSummary, textRankSummary)
    #print(scores)

    #scores = scorer.score(humanSummary, lsaSummary)
    #print(scores)

if __name__=="__main__":
    main()