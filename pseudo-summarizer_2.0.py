import os
import re
import amrlib
import random

def pseudo_summarizer(file):
	"""
	Takes a file of sentences as input, converts each sentence to a single-line AMR,
	randomly selects four AMRs, and from these creates a pseudo-multi-sentence AMR.
	"""

	# Open file and save each sentence to a different line
	with open(file) as f:
		sentences = [sentence.rstrip() for sentence in f.readlines()]

	# Load AMR parser
	p = '/Users/jackweyen/Desktop/Saarland/Semester I/AMR/Summarization Nation/model_parse_spring-v0_1_0'
	stog = amrlib.load_stog_model(model_dir=p)

	# Convert each sentence to a list of multi-line AMRs
	parser_output = stog.parse_sents(sentences)

	# Remove original sentence and tabs and new lines,
	# converting multi-line AMRs into single-line AMRs
	AMRs = []
	for AMR in parser_output:
		AMR = re.sub(r"""# ::snt .*?\n""", r"""""", AMR)
		AMR = re.sub(r""" {6}""", r"""""", AMR)
		AMR = re.sub(r"""\n""", r""" """, AMR)
		AMRs.append(AMR)

	# If number of AMRs greater than four, select four AMRs at random
	# otherwise, pass on list of AMRs unchanged
	if len(AMRs) > 4:
		random_AMRs = random.choices(AMRs, k = 4)
	else:
		random_ARMs = AMRs

	# Convert to multi-sentence AMR
	# TODO
	MSAMR = "\n".join(AMRs)

	# Create output file
	with open("output.txt", "w") as o:
		o.write(MSAMR)

pseudo_summarizer("input.txt")
