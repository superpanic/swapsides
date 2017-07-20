# game: A game is won when a player wins four points.
#	But you must win by two.
# set: A set is won when a player has won six games.
# 	But you must win by two.
# match: A match is won then a player has won three out of five sets. Or two out of three sets.
#	But you must win by two.

# Example of set scores: 6-3, 4-6, 6-2

# Yes. So the score can be 5-7, 6-8, 7-9 etc, as long as you win by two points.
# When writing it, you write the losing score of the tiebreak in the parentheses: 7-6 (3) 
# When the number is less than or equal to five, you know that the winner had 7 points in the tiebreak. 
# If the set looked like this: 7-6 (11) then you have to add two points to see how many the winner had. 

# 6-1
# 6+1 = 7
# 7/2 = 3.5
# ceiling(3.5) = 4
# Changing sides = 4

# In a tiebreak game the players change ends every six points.
# 7-6
# 7+6 = 8
# 4-6, 7-6(11-9), 6-3
# A tiebreak (7-6) set can never be more than 6!
# ceiling( (11-9)/6 )
# 5, 6, 4, 5 = 20

import csv
import pandas
import math
import string

valid_chars = set("1234567890-() ")

def check_string(input_string):
	input_string = input_string.strip()
	if all(char in valid_chars for char in input_string):
		return True
	else:
		return False

def num_there(s):
    return any(i.isdigit() for i in s)

def changes_from_set_score(score):
	# parse the numbers a and b from score_string
	return int(math.ceil(float(score)/2))

def changes_from_tiebreak_score(score):
	# parse the numbers a and b from score_string
	if(score <= 5):
		score = score + 7
	else:
		score = score + (score+2)
	return int(math.ceil(float(score)/6))

def parse_score(score_string):
	return_total_changes = 0
	# returns the numer of times the players changes sides based in the set scores
	# there should be a - delimiter between set scores:
	if "-" not in score_string:
		return 0
	# make sure there are some digits to work with:
	if not num_there(score_string):
		return 0
	
	# does the set scores contain a parantheses?
	if "(" in score_string:
		# it's a tiebreak score
		# get the string within the paranthesis
		tiebreak_score = int(score_string.partition('(')[-1].rpartition(')')[0])
		return_total_changes = return_total_changes + changes_from_tiebreak_score(tiebreak_score)
		# strip the parathesis with the tiebreak score
		score_string = score_string.partition('(')[0]

	set_scores = score_string.split("-")
	# assume we got two values from the split
	if len(set_scores) == 2:
		# check that the set score strings are integer
		if set_scores[0].isdigit() and set_scores[1].isdigit():
			score_sum = int(set_scores[0]) + int(set_scores[1])
			return_total_changes = changes_from_set_score(score_sum)
		else:
			print("Warning, found a strange set score format that are not two integers:")
			print set_scores
			print("-------------------")
			return 0
	else:
		print("Warning, found a strange set score format that does not have exactly 2 scores:")
		print set_scores
		print("-------------------")
		return 0
	return return_total_changes

def parse_atp_data(files):
	file_count = len(files)
	
	super_data_count = 0
	super_side_change_count = 0

	max_changes_in_set = 0
	max_changes_in_match = 0
	min_found = 1000
	for f in files:
		print "DATA: " + f
		data_file = pandas.read_csv(f)
		# this will get only the column named 'score' from the csv:
		score_data = data_file.score
		winner_name_data = data_file.winner_name
		# length of data:
		# counter used for calculating average
		data_count = 0
		# counter for total numer of times the players change sides:
		total_change_side_count = 0
		# split the file into matches:
		c = 0
		for match_data in score_data:
			winner = winner_name_data[c]
			c=c+1
			if not isinstance(match_data, str):
				# throw out anything not a string
				continue
			if not check_string(match_data):
				# throw out data with RET, walkover and unknown data 
				#print match_data
				continue

			# total data counter for calculating average
			data_count = data_count + 1

			match_changes = 0
			set_data = match_data.split()
			for s in set_data:
				current_change_side_count = parse_score(s)
				if max_changes_in_set < current_change_side_count:
					max_changes_in_set = current_change_side_count
					print winner
				match_changes = match_changes + current_change_side_count
				total_change_side_count = total_change_side_count + current_change_side_count

			# find the maximum side changes in a match
			if max_changes_in_match < match_changes:
				max_changes_in_match = match_changes

		print "Total changes of end: " + str(total_change_side_count)
		print "Mean average total changes of end: " + str(total_change_side_count / data_count)

		super_side_change_count = super_side_change_count + total_change_side_count
		super_data_count = super_data_count + data_count

	print "-------------------------------------"
	print "Total mean average over all files: " + str(super_side_change_count / super_data_count)
	print "Maximum number of changes in a set: " + str(max_changes_in_set)
	print "Maximum number of changes in a match: " + str(max_changes_in_match)

parse_atp_data([
	'atp_matches_1968.csv',
	'atp_matches_1969.csv',
	'atp_matches_1970.csv',
	'atp_matches_1971.csv',
	'atp_matches_1972.csv',
	'atp_matches_1973.csv',
	'atp_matches_1974.csv',
	'atp_matches_1975.csv',
	'atp_matches_1976.csv',
	'atp_matches_1977.csv',
	'atp_matches_1978.csv',
	'atp_matches_1979.csv',
	'atp_matches_1980.csv',
	'atp_matches_1981.csv',
	'atp_matches_1982.csv',
	'atp_matches_1983.csv',
	'atp_matches_1984.csv',
	'atp_matches_1985.csv',
	'atp_matches_1986.csv',
	'atp_matches_1987.csv',
	'atp_matches_1988.csv',
	'atp_matches_1989.csv',
	'atp_matches_1990.csv',
	'atp_matches_1991.csv',
	'atp_matches_1992.csv',
	'atp_matches_1993.csv',
	'atp_matches_1994.csv',
	'atp_matches_1995.csv',
	'atp_matches_1996.csv',
	'atp_matches_1997.csv',
	'atp_matches_1998.csv',
	'atp_matches_1999.csv',
	'atp_matches_2000.csv',
	'atp_matches_2001.csv',
	'atp_matches_2002.csv',
	'atp_matches_2003.csv',
	'atp_matches_2004.csv',
	'atp_matches_2005.csv',
	'atp_matches_2006.csv',
	'atp_matches_2007.csv',
	'atp_matches_2008.csv',
	'atp_matches_2009.csv',
	'atp_matches_2010.csv',
	'atp_matches_2011.csv',
	'atp_matches_2012.csv',
	'atp_matches_2013.csv',
	'atp_matches_2014.csv',
	'atp_matches_2015.csv',
	'atp_matches_2016.csv',
	'atp_matches_2017.csv'
])


# run all matches not just ATP:

# parse_atp_data([
# 	'atp_matches_1968.csv',
# 	'atp_matches_1969.csv',
# 	'atp_matches_1970.csv',
# 	'atp_matches_1971.csv',
# 	'atp_matches_1972.csv',
# 	'atp_matches_1973.csv',
# 	'atp_matches_1974.csv',
# 	'atp_matches_1975.csv',
# 	'atp_matches_1976.csv',
# 	'atp_matches_1977.csv',
# 	'atp_matches_1978.csv',
# 	'atp_matches_1979.csv',
# 	'atp_matches_1980.csv',
# 	'atp_matches_1981.csv',
# 	'atp_matches_1982.csv',
# 	'atp_matches_1983.csv',
# 	'atp_matches_1984.csv',
# 	'atp_matches_1985.csv',
# 	'atp_matches_1986.csv',
# 	'atp_matches_1987.csv',
# 	'atp_matches_1988.csv',
# 	'atp_matches_1989.csv',
# 	'atp_matches_1990.csv',
# 	'atp_matches_1991.csv',
# 	'atp_matches_1992.csv',
# 	'atp_matches_1993.csv',
# 	'atp_matches_1994.csv',
# 	'atp_matches_1995.csv',
# 	'atp_matches_1996.csv',
# 	'atp_matches_1997.csv',
# 	'atp_matches_1998.csv',
# 	'atp_matches_1999.csv',
# 	'atp_matches_2000.csv',
# 	'atp_matches_2001.csv',
# 	'atp_matches_2002.csv',
# 	'atp_matches_2003.csv',
# 	'atp_matches_2004.csv',
# 	'atp_matches_2005.csv',
# 	'atp_matches_2006.csv',
# 	'atp_matches_2007.csv',
# 	'atp_matches_2008.csv',
# 	'atp_matches_2009.csv',
# 	'atp_matches_2010.csv',
# 	'atp_matches_2011.csv',
# 	'atp_matches_2012.csv',
# 	'atp_matches_2013.csv',
# 	'atp_matches_2014.csv',
# 	'atp_matches_2015.csv',
# 	'atp_matches_2016.csv',
# 	'atp_matches_2017.csv',
# 	'atp_matches_futures_1991.csv',
# 	'atp_matches_futures_1992.csv',
# 	'atp_matches_futures_1993.csv',
# 	'atp_matches_futures_1994.csv',
# 	'atp_matches_futures_1995.csv',
# 	'atp_matches_futures_1996.csv',
# 	'atp_matches_futures_1997.csv',
# 	'atp_matches_futures_1998.csv',
# 	'atp_matches_futures_1999.csv',
# 	'atp_matches_futures_2000.csv',
# 	'atp_matches_futures_2001.csv',
# 	'atp_matches_futures_2002.csv',
# 	'atp_matches_futures_2003.csv',
# 	'atp_matches_futures_2004.csv',
# 	'atp_matches_futures_2005.csv',
# 	'atp_matches_futures_2006.csv',
# 	'atp_matches_futures_2007.csv',
# 	'atp_matches_futures_2008.csv',
# 	'atp_matches_futures_2009.csv',
# 	'atp_matches_futures_2010.csv',
# 	'atp_matches_futures_2011.csv',
# 	'atp_matches_futures_2012.csv',
# 	'atp_matches_futures_2013.csv',
# 	'atp_matches_futures_2014.csv',
# 	'atp_matches_futures_2015.csv',
# 	'atp_matches_futures_2016.csv',
# 	'atp_matches_futures_2017.csv',
# 	'atp_matches_qual_chall_1991.csv',
# 	'atp_matches_qual_chall_1992.csv',
# 	'atp_matches_qual_chall_1993.csv',
# 	'atp_matches_qual_chall_1994.csv',
# 	'atp_matches_qual_chall_1995.csv',
# 	'atp_matches_qual_chall_1996.csv',
# 	'atp_matches_qual_chall_1997.csv',
# 	'atp_matches_qual_chall_1998.csv',
# 	'atp_matches_qual_chall_1999.csv',
# 	'atp_matches_qual_chall_2000.csv',
# 	'atp_matches_qual_chall_2001.csv',
# 	'atp_matches_qual_chall_2002.csv',
# 	'atp_matches_qual_chall_2003.csv',
# 	'atp_matches_qual_chall_2004.csv',
# 	'atp_matches_qual_chall_2005.csv',
# 	'atp_matches_qual_chall_2006.csv',
# 	'atp_matches_qual_chall_2007.csv',
# 	'atp_matches_qual_chall_2008.csv',
# 	'atp_matches_qual_chall_2009.csv',
# 	'atp_matches_qual_chall_2010.csv',
# 	'atp_matches_qual_chall_2011.csv',
# 	'atp_matches_qual_chall_2012.csv',
# 	'atp_matches_qual_chall_2013.csv',
# 	'atp_matches_qual_chall_2014.csv',
# 	'atp_matches_qual_chall_2015.csv',
# 	'atp_matches_qual_chall_2016.csv',
# 	'atp_matches_qual_chall_2017.csv'
# ])
