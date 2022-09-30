import sumy.summarizers.text_rank as TextRankSummarizer
import sumy.summarizers.lsa       as LsaSummarizer
import sumy.parsers.plaintext     as PlaintTextParser
import sumy.nlp.tokenizers        as Tokenizer
import pandas                     as pd
import textwrap
import nltk
nltk.download('punkt')
from rouge_score import rouge_scorer

def main():
    dataFrameEnglish = pd.read_csv("./datos/test.csv")

    entry = dataFrameEnglish.iloc[0]
    doc   = entry["article"]
    humanSummary = entry["highlights"]

    ## Prueba text rank
    summarizer = TextRankSummarizer.TextRankSummarizer()
    parser     = PlaintTextParser.PlaintextParser.from_string(
        doc,
        Tokenizer.Tokenizer("english")
    )
    summary = summarizer(parser.document, sentences_count=5)
    textRankSummary = ""
    for sentence in summary: 
        s = str(sentence)
        textRankSummary += s

    ## Prueba lsa
    summarizer = LsaSummarizer.LsaSummarizer()
    parser     = PlaintTextParser.PlaintextParser.from_string(
        doc,
        Tokenizer.Tokenizer("english")
    )
    summary = summarizer(parser.document, sentences_count=5)
    lsaSummary = ""
    for sentence in summary: 
        s = str(sentence)
        lsaSummary += s

    #Rouge
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'])

    scores = scorer.score(humanSummary, textRankSummary)
    print(scores)

    scores = scorer.score(humanSummary, lsaSummary)
    print(scores)
    print("*"*30,textwrap.fill(textRankSummary),sep="\n")
if __name__=="__main__":
    main()