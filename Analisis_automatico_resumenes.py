import textwrap
import nltk
import operator
import sumy.summarizers.text_rank as TextRankSummarizer
import sumy.summarizers.lsa       as LsaSummarizer
import sumy.parsers.plaintext     as PlaintTextParser
import sumy.nlp.tokenizers        as Tokenizer
import pandas                     as pd
import numpy                      as np
from tqdm        import tqdm
from rouge_score import rouge_scorer
from functools   import reduce
from sys         import argv
nltk.download('punkt')

# Constants
SUMMARIZERS = [
    TextRankSummarizer.TextRankSummarizer(),
    LsaSummarizer.LsaSummarizer()
]
FIRST_COLUMNS_FOR_GENERATED_DF = ["Texto original", "Resumen humano"]
SEED_FOR_SUMMARY_SELECTION = 616
AMOUNT_LINES_PER_SUMMARY   = 5
AMOUNT_SUMMARIES           = 30
ROUGE_METRICS              = ['rouge2', 'rougeL']
COLUMNS_FROM_INPUT_DF_ENGLISH = ["article", "highlights"]
COLUMNS_FROM_INPUT_DF_SPANISH = ["Fuente", "Resumen"]

# Summary generation
def main():
    language = argv[2]
    columnsFromInputDF   = getColumnsFromInputDF(language)
    generated_summaries  = createDataFrame()
    docs, humanSummaries = getNewsAndHumanSummaries(columnsFromInputDF)
    scorer               = rouge_scorer.RougeScorer(ROUGE_METRICS)
    fillDataFrame(generated_summaries, docs, humanSummaries, scorer, language)

    generated_summaries.to_csv(argv[3])

def getColumnsFromInputDF(language):
    if language == "spanish": return COLUMNS_FROM_INPUT_DF_SPANISH
    else: return COLUMNS_FROM_INPUT_DF_ENGLISH

def createDataFrame():
    columns = FIRST_COLUMNS_FOR_GENERATED_DF
    for summarizer in SUMMARIZERS:
        summarizer_name = type(summarizer).__name__
        columns.append(summarizer_name)
        for metric in ROUGE_METRICS:
            columns.append(type(summarizer).__name__ + " " + metric + " precision")
            columns.append(type(summarizer).__name__ + " " + metric + " exhautividad")
    return pd.DataFrame(index=range(AMOUNT_SUMMARIES), columns=columns)

def getNewsAndHumanSummaries(columnsFromInputDF):
    np.random.seed(SEED_FOR_SUMMARY_SELECTION)
    rng = np.random.default_rng()
    dataFrame     = pd.read_csv(argv[1])
    amount_news   = dataFrame.shape[0]
    selected_news = rng.integers(
        amount_news, size = (AMOUNT_SUMMARIES,)
    )
    sample = dataFrame.iloc[selected_news]
    return sample[columnsFromInputDF[0]], sample[columnsFromInputDF[1]]

def fillDataFrame(generated_summaries, docs, humanSummaries, scorer, language):
    for i, doc in enumerate(tqdm(docs, desc="Documentos")):
        hummanSummary = humanSummaries.iloc[i]
        new_data_row  = [doc, hummanSummary]
        for summarizer in SUMMARIZERS:
            generated_summary = makeSummary(doc, summarizer, language)
            scores            = scorer.score(hummanSummary, generated_summary)
            new_data_row.append(generated_summary)
            for metric in ROUGE_METRICS:
                new_data_row.append(scores[metric].precision)
                new_data_row.append(scores[metric].recall)
        
        generated_summaries.iloc[i] = new_data_row

def makeSummary(doc2summarize, summarizer, language):
    parser = PlaintTextParser.PlaintextParser.from_string(
        doc2summarize,
        Tokenizer.Tokenizer(language)
    )
    summaryOBJ = summarizer(parser.document, sentences_count=AMOUNT_LINES_PER_SUMMARY)
    return reduce(operator.add, map(lambda x: str(x), summaryOBJ), "")

if __name__=="__main__":
    main()