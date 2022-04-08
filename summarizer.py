import re

def summarizer(amr_file, coreferences, n):
	"""
	Outputs a summary given an article in MSAMR format and its
	resolved coreferences.
	"""
	with open(amr_file, encoding='utf-8') as f:
		full_AMR_text = f.read()

	# Create dictionary to store each AMR and its score
	AMR_scores = {}

	# Iterate through each concept in the coreferences dictionary
	for concept, variables in coreferences.items():

		# Save each AMR that references that concept to a list,
		# and iterate through that list
		AMRs = [AMR for AMR, variable in variables]
		for AMR in AMRs:

			# Every time that AMR mentions that concept, add the number of reentrancies that
			# concept has to the AMR score (this weights the score by frequency, and therefore
			# importance, of the concept)
			AMR_scores[AMR] = AMR_scores.get(AMR, 0) + len(variables)

	# Convert dictionary of AMR scores into list sorted from highest to lowest scores,
	# then remove scores from list
	AMR_scores = [(AMR, score) for AMR, score in AMR_scores.items()]
	AMR_scores.sort(reverse=True, key=lambda x: x[1])
	AMRs_sorted = [AMR for AMR, score in AMR_scores]

	# Create a list of full AMRs from the full AMR text string
	full_AMRs = full_AMR_text.split("\n\n")

	# Pick the foremost AMRs in the list for the summary, as these
	# will have the highest scores. Size of the summary is scaled
	# based on n, such that every n full AMRs (i.e. sentences in
	# the text) will result in 1 additional sentence in the summary
	summary_AMRs = AMRs_sorted[:len(full_AMRs)//n]

	# Sort summary AMRs based on position in article
	# and create output using indexes from summary AMRs
	# on the full AMRs,
	summary_AMRs.sort()
	output = [full_AMRs[index] for index in summary_AMRs]

	# Return selected AMRs as the summary
	return output
