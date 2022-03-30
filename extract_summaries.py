import re
import random

def extract_summaries(file):
	"""
	Extracts paragraphs and their corresponding summaries from an AMR proxy report,
	and outputs the results into a list of tuples
	"""

	# Open proxy file and save contents as a string
	with open(file, "r", encoding="utf-8") as f:
		contents = f.read()

	# Split contents into string of separate AMRs
	AMRs = contents.split("\n\n")

	# Define important variables
	output = []
	current_id = ""
	summary = ""
	paragraph = ""
	final_index = len(AMRs)

	# For each AMR in the file...
	for index, AMR in enumerate(AMRs):

		# Get the id of the paragraph this AMR pertains to
		# (that is, the id minus the digits after the decimal)
		id_match = re.search(r"""# ::id .*?\.""", AMR)
		if not id_match:
			continue
		id = id_match.group()

		# Ignore the metadata AMRs (date, country, and topic)
		if not re.search(r"""::snt-type summary""", AMR) and not re.search(r"""::snt-type body""", AMR):
			continue

		# If there is not a current id, make this id equal the current id
		if not current_id:
			current_id = id

		# If there is already a current id, and this id does not match it,
		# then the previous paragraph is finished. Add the paragraph and
 		# summary to the output in a tuple, and reset the current_id,
		# summary, and paragraph variables
		elif id != current_id:
			output.append((paragraph.strip(), summary))
			current_id = ""
			summary = ""
			paragraph = ""

		# Isolate sentence from AMR, remove sentence tag ("# ::snt "), and remove all punctuation besides
		# spaces, periods, question marks, exclamation points, commas, apostrophes, quotes, and hyphens.
		sentence_match = re.search(r"""# ::snt.*?\n""", AMR)
		sentence = re.sub(r"""# ::snt """, r"""""", sentence_match.group())

		# Replace "--" with "." in sentence
		sentence = re.sub(r""" --""", r""".""", sentence)

		# If the AMR is the summary, store the sentence in the summary variable
		if re.search(r"""::snt-type summary""", AMR):
			summary = sentence

		# Otherwise, the sentence is part of the paragraph; add to the paragraph
		else:
			paragraph += sentence + " "

		# If this is the final AMR in the proxy report, add final paragraph and summary
		if index + 1 == final_index:
			output.append((paragraph.strip(), summary))

	return output

def sample_human_eval(num_of_texts=5, out_file="human_eval_gold.txt"):
	output = extract_summaries("amr-release-3.0-amrs-test-proxy.txt")
	sample = random.sample(output, k=num_of_texts)
	with open(out_file, "w", encoding="utf-8") as of:
		for item in sample:
			of.write("::"+str(output.index(item) + 1) + "\n")
			of.write(item[0]+"\n")
			of.write("::summary\n")
			of.write(item[1]+"\n")

output = extract_summaries('amr-release-3.0-amrs-proxy.txt')
