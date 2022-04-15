import cProfile, pstats
import os
import re
import time

import amrlib
import random
import sys

from extract_summaries import extract_summaries
from rouge_score import rouge_scorer


def eval(corpus):

     # Load the parser.
     p = './model_parse_spring-v0_1_0'
     stog = amrlib.load_stog_model(model_dir=p)
     print("Loaded parser.")

     # Load the generator.
     g = './model_generate_t5wtense-v0_1_0'
     gtos = amrlib.load_gtos_model(model_dir=g, )
     print("Loaded generator.")

     # Baseline summarizer with options random/first and number of sentences.
     # The query appears in the terminal.
     select = input("Choose: random or first?")
     n = int(input("How many sentences should the summary have?"))

     # Extracts the paragraphs and summaries from the AMR bank corpus.
     p_s_pair_list = extract_summaries(corpus)

     # Initialize counters for calculating corpus average ROUGE scores
     total_summary_count = len(p_s_pair_list)
     total_rouge_1 = {"precision": 0, "recall": 0, "fscore": 0}
     total_rouge_2 = {"precision": 0, "recall": 0, "fscore": 0}
     total_rouge_l = {"precision": 0, "recall": 0, "fscore": 0}

     for (paragraph, gold_summary) in p_s_pair_list:
          sentences = paragraph.split("\n")

          # Choose AMRs for summary.
          if select == 'random':
               amrs = random.sample(sentences,k=n)
          elif select == 'first':
               amrs = sentences[:int(n)]

          # Parse the AMRs.
          summary_AMRs = stog.parse_sents(amrs)

          # Generate sentences from the AMRs.
          sents, _ = gtos.generate(summary_AMRs, disable_progress=False, use_tense=False)
          generated_summary = ' '.join(sents)

          # Create a rouge scorer for rouge1, rouge2 and rougeL.
          scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
          scores = scorer.score(generated_summary, gold_summary)
          print("Generated summary:",generated_summary)
          print("Gold summary:", gold_summary)
          print(scores)

          # Add the scores to the counters for the corpus average.
          for rouge, metrics in scores.items():
               if rouge == 'rouge1':
                    total_rouge_1["precision"] += metrics[0]
                    total_rouge_1["recall"] += metrics[1]
                    total_rouge_1["fscore"] += metrics[2]
               elif rouge == 'rouge2':
                    total_rouge_2["precision"] += metrics[0]
                    total_rouge_2["recall"] += metrics[1]
                    total_rouge_2["fscore"] += metrics[2]
               elif rouge == 'rougeL':
                    total_rouge_l["precision"] += metrics[0]
                    total_rouge_l["recall"] += metrics[1]
                    total_rouge_l["fscore"] += metrics[2]

     # Calculate the averages.
     total_rouge_1["precision"] = total_rouge_1["precision"]/total_summary_count
     total_rouge_1["recall"] = total_rouge_1["recall"]/total_summary_count
     total_rouge_1["fscore"] = total_rouge_1["fscore"]/total_summary_count
     total_rouge_2["precision"] = total_rouge_2["precision"] / total_summary_count
     total_rouge_2["recall"] = total_rouge_2["recall"] / total_summary_count
     total_rouge_2["fscore"] = total_rouge_2["fscore"] / total_summary_count
     total_rouge_l["precision"] = total_rouge_l["precision"] / total_summary_count
     total_rouge_l["recall"] = total_rouge_l["recall"] / total_summary_count
     total_rouge_l["fscore"] = total_rouge_l["fscore"] / total_summary_count


     # Print the average ROUGE scores for the entire AMR corpus
     print("\n")
     print("-- AVERAGE ROUGE SCORES FOR THE CORPUS --")
     print("Average ROUGE1 scores:", "precision:", total_rouge_1["precision"], "recall:", total_rouge_1["recall"], "fscore:", total_rouge_1["fscore"])
     print("Average ROUGE2 scores:", "precision:", total_rouge_2["precision"],"recall:", total_rouge_2["recall"], "fscore:", total_rouge_2["fscore"])
     print("Average ROUGEL scores:", "precision:", total_rouge_l["precision"],"recall:", total_rouge_l["recall"],"fscore:", total_rouge_l["fscore"])



eval(sys.argv[1])


