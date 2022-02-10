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
	p = os.path.abspath("model_parse_spring-v0_1_0")
	stog = amrlib.load_stog_model(model_dir=p)

	# Convert each sentence to an AMR
	parser_output = stog.parse_sents(sentences)

	# Remove original sentence and mark each new AMR with an initial '###',
	# and then split into list of multi-line AMRs
	parser_output = re.sub(r"""^#.*\r\n""", r"""###""", parser_output)
	AMRs = parser_output.split("###")

	# Remove tabs and new lines, converting multi-line AMRs into single-line AMRs
	for AMR in AMRs:
		AMR = re.sub(r""" {6}""", r"""""", AMR)
		AMR = re.sub(r"""\n""", r""" """, AMR)

	# If number of AMRs greater than four, select four AMRs at random
	# otherwise, pass on list of AMRs unchanged
	if len(AMRs) > 4:
		random_AMRs = random.select(AMRs, 4)
	else:
		random_ARMs = AMRs

	# Convert to multi-sentence AMR
	# TODO
	MSAMR = "\n".join(AMRs)

	# Create output file
	with open("output.txt", "w") as o:
		o.write(MSAMR)

pseudo_summarizer("input.txt")
