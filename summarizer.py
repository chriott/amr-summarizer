import re

def summarizer(full_AMR_text, coreferences, n):
	"""
	Outputs a summary given an article in MSAMR format and its
	resolved coreferences.
	"""

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

# Test input
AMRs = """
# ::id 1
# ::snt George RR Martin to team up with Marvel for new comic book series
(z0 / team-up-02
      :ARG0 (z1 / person
            :name (z2 / name
                  :op1 "George"
                  :op2 "RR"
                  :op3 "Martin"))
      :ARG1 (z3 / company
            :name (z4 / name
                  :op1 "Marvel"))
      :ARG2 (z5 / series
            :ARG1-of (z6 / new-01)
            :mod (z7 / comic-book)))

# ::id 2
# ::snt Game Of Thrones writer says opportunity to produce comics based on his superhero series Wild Cards is a 'privilege'
(z0 / say-01
      :ARG0 (z1 / person
            :ARG0-of (z2 / write-01
                  :ARG1 (z3 / broadcast-program
                        :name (z4 / name
                              :op1 "Game"
                              :op2 "Of"
                              :op3 "Thrones"))))
      :ARG1 (z5 / privilege
            :domain (z6 / opportunity
                  :topic (z7 / produce-01
                        :ARG0 z1
                        :ARG1 (z8 / comic
                              :ARG1-of (z9 / base-02
                                    :ARG2 (z10 / broadcast-program
                                          :name (z11 / name
                                                :op1 "Wild"
                                                :op2 "Cards")
                                          :mod (z12 / superhero)
                                          :poss z1)))))))

# ::id 3
# ::snt George RR Martin will team up with Marvel to produce a new series of comic books, it has been announced.
(z0 / announce-01
      :ARG1 (z1 / team-up-02
            :ARG0 (z2 / person
                  :name (z3 / name
                        :op1 "George"
                        :op2 "RR"
                        :op3 "Martin"))
            :ARG1 (z4 / company
                  :name (z5 / name
                        :op1 "Marvel"))
            :ARG2 (z6 / produce-01
                  :ARG0 z2
                  :ARG1 (z7 / series
                        :mod (z8 / comic)
                        :ARG1-of (z9 / new-01)))))

# ::id 4
# ::snt The Game of Thrones writer said working with the superhero franchise titan was a "privilege" and brought him "no end of joy".
(z0 / say-01
      :ARG0 (z1 / person
            :ARG0-of (z2 / write-01
                  :ARG1 (z3 / broadcast-program
                        :name (z4 / name
                              :op1 "Game"
                              :op2 "of"
                              :op3 "Thrones"))))
      :ARG1 (z5 / and
            :op1 (z6 / privilege
                  :domain (z7 / work-01
                        :ARG0 z1
                        :ARG3 (z8 / titan
                              :mod (z9 / franchise
                                    :mod (z10 / superhero)))))
            :op2 (z11 / end-01
                  :polarity -
                  :ARG0 z7
                  :ARG1 (z12 / joy))))

# ::id 5
# ::snt The comics will be based on the superhero anthology series Wild Cards, which was masterminded and edited by Martin.
(z0 / base-02
      :ARG1 (z1 / comic)
      :ARG2 (z2 / broadcast-program
            :name (z3 / name
                  :op1 "Wild"
                  :op2 "Cards")
            :mod (z4 / anthology)
            :mod (z5 / superhero)
            :ARG1-of (z6 / mastermind-01
                  :ARG0 (z7 / person
                        :name (z8 / name
                              :op1 "Martin")))
            :ARG1-of (z9 / edit-01
                  :ARG0 z7)))

# ::id 6
# ::snt Wild Cards tells the story of an alternate history where Earth is home to super-powered individuals and spans more than 25 novels and 20 short stories.
(z0 / and
      :op1 (z1 / tell-01
            :ARG0 (z2 / broadcast-program
                  :name (z3 / name
                        :op1 "Wild"
                        :op2 "Cards"))
            :ARG1 (z4 / history
                  :ARG1-of (z5 / alternate-01)
                  :time-of (z6 / planet
                        :name (z7 / name
                              :op1 "Earth")
                        :mod (z8 / home
                              :poss (z9 / individual
                                    :ARG1-of (z10 / power-01
                                          :degree (z11 / super)))))))
      :op2 (z12 / span-01
            :ARG0 z2
            :ARG1 (z13 / and
                  :op1 (z14 / novel
                        :quant 25)
                  :op2 (z15 / story
                        :quant 20
                        :ARG1-of (z16 / short-07)))))

# ::id 7
# ::snt It was written by more than 40 authors over three decades, and the limited series, Wild Cards: Drawing Of The Cards, will arrive later this year.
(z0 / and
      :op1 (z1 / write-01
            :ARG0 (z2 / person
                  :quant (z3 / more-than
                        :op1 40)
                  :ARG0-of (z4 / author-01))
            :ARG1 (z5 / it)
            :duration (z6 / temporal-quantity
                  :quant 3
                  :unit (z7 / decade)))
      :op2 (z8 / arrive-01
            :ARG1 (z9 / series
                  :name (z10 / name
                        :op1 "Wild"
                        :op2 "Cards"
                        :op3 "Drawing"
                        :op4 "Of"
                        :op5 "The"
                        :op6 "Cards")
                  :ARG1-of (z11 / limit-01))
            :time (z12 / late
                  :op1 (z13 / year
                        :mod (z14 / this))
                  :degree (z15 / somewhat))))

# ::id 8
# ::snt "As my fans may already know, the Wild Cards World holds a special place in my heart," said Martin.
(z0 / say-01
      :ARG0 (z1 / person
            :name (z2 / name
                  :op1 "Martin"))
      :ARG1 (z3 / hold-01
            :ARG0 (z4 / broadcast-program
                  :name (z5 / name
                        :op1 "Wild"
                        :op2 "Cards"
                        :op3 "World"))
            :ARG1 (z6 / place
                  :ARG1-of (z7 / special-02)
                  :location (z8 / heart
                        :part-of z1))
            :ARG1-of (z9 / know-01
                  :ARG0 (z10 / fan
                        :poss z1)
                  :time (z11 / already)
                  :ARG1-of (z12 / possible-01))))

# ::id 9
# ::snt "So to have the privilege of announcing that an industry titan like Marvel is going to produce the narrative from the beginning as a comic book brings me no end of joy."
(z0 / cause-01
      :ARG1 (z1 / bring-01
            :polarity -
            :ARG0 (z2 / privilege-01
                  :ARG1 (z3 / announce-01
                        :ARG1 (z4 / produce-01
                              :ARG0 (z5 / titan
                                    :mod (z6 / industry)
                                    :example (z7 / company
                                          :name (z8 / name
                                                :op1 "Marvel")))
                              :ARG1 (z9 / narrative)
                              :time (z10 / from
                                    :op1 (z11 / begin-01))
                              :prep-as (z12 / comic-book))))
            :ARG1 (z13 / end-01
                  :ARG1 (z14 / joy))
            :ARG2 (z15 / i)))

# ::id 10
# ::snt Martin's most well-known work, Game Of Thrones, ended its hugely successful run in 2019 and HBO is currently developing spin-offs, including a prequel series set to air next year.
(z0 / and
      :op1 (z1 / end-01
            :ARG0 (z2 / work-of-art
                  :name (z3 / name
                        :op1 "Game"
                        :op2 "Of"
                        :op3 "Thrones")
                  :ARG1-of (z4 / have-degree-91
                        :ARG2 (z5 / know-02
                              :ARG1 z2
                              :ARG1-of (z6 / well-09))
                        :ARG3 (z7 / most))
                  :poss (z8 / person
                        :name (z9 / name
                              :op1 "Martin")))
            :ARG1 (z10 / run-13
                  :ARG1 z2
                  :ARG1-of (z11 / succeed-01
                        :degree (z12 / huge)))
            :time (z13 / date-entity
                  :year 2019))
      :op2 (z14 / develop-02
            :ARG0 (z15 / network
                  :name (z16 / name
                        :op1 "HBO"))
            :ARG1 (z17 / spin-off
                  :ARG2-of (z18 / include-01
                        :ARG1 (z19 / series
                              :mod (z20 / prequel)
                              :ARG1-of (z21 / set-08
                                    :ARG2 (z22 / air-01
                                          :time (z23 / year
                                                :mod (z24 / next)))))))
            :time (z25 / current)))
"""
coreferences = {'rel-0': [(0, 'z1'), (1, 'z1'), (3, 'z1')], 'rel-1': [(2, 'z2'), (3, 'z1'), (4, 'z7')], 'rel-2': [(0, 'z5'), (2, 'z7')], 'rel-3': [(1, 'z10'), (3, 'z3'), (5, 'z2'), (6, 'z5')]}

n = 2

summary_AMRs = summarizer(AMRs, coreferences, n)

for AMR in summary_AMRs:
	print(AMR)
