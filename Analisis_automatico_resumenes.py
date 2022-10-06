from pyrfc3339 import generate
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

    columns = ["Original Text", "Human summary"]
    for summarizer in SUMMARIZERS:
        summarizer_name = type(summarizer).__name__
        columns.append(summarizer_name)
        columns.append(type(summarizer).__name__ + "Rouge precition")
        columns.append(type(summarizer).__name__ + "Rouge recall")

    generated_summaries = pd.DataFrame(index=range(30), columns=columns)
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'])

    for i, doc in enumerate(docs):
        hummanSummary = humanSummaries.iloc[i]
        new_data_row = [doc, hummanSummary]
        for summarizer in SUMMARIZERS:
            generated_summary = makeSummary(doc, summarizer, language)
            scores = scorer.score(hummanSummary, generated_summary)
            new_data_row.append(generated_summary)
            new_data_row.append(scores[0])
            new_data_row.append(scores[1])
        
        generated_summaries.iloc[i] = new_data_row

    
    print(generated_summaries)

if __name__=="__main__":
    main()