#! /usr/bin/python3

from Bio import Entrez
import os
import re
import csv

Entrez.email = "YOUR EMAIL HERE"
filename = "YOUR FILENAME HERE"		# Note: file must be in same directory as script

# Todo: Don't assume a fixed file format and ids in column two
# Get the ids from file
ids = []
path = os.getcwd()
with open(path + "/" + filename) as tsvfile:
	tsvreader = csv.reader(tsvfile, delimiter="\t")
	for line in tsvreader:
		tmp = []
		tmp.append(line[0])
		tmp.append(line[1])
		ids.append(tmp)

# Prepare stuff
info_fail = 0
info_success = 0
header = "id\tdate\tlocation\thost\n"

# Search for info and write to file
# Todo: Error handling
with open("output.tsv", mode="w") as out:
	out.write(header)
	for id in ids:
		# Get info from server
		print("Getting info for ", id[1])
		tmp = ""
		handle = Entrez.efetch(db="biosample", id=id[1], retmode="text")
		for line in handle:
			tmp = tmp + line

		# Search info
		m = re.search('(?:\/collection date=\")(\d+)[\s\S]*(?:\/geographic location=\")([a-zA-Z\s]*)[\s\S]*(?:\/host=\")([a-zA-Z\s]*)', tmp)	

		# Save to file
		# Todo: check for specific capturing groups
		if m:
			print("Writing info --- Date: %s, Location: %s, Host: %s" % (m.group(1), m.group(2), m.group(3)))
			out.write(id[1] + "\t" + m.group(1) + "\t" + m.group(2) + "\t" + m.group(3) + "\n")
			info_success = info_success + 1
		else:
			print("Did not find any info")
			out.write(id[1] + "\t missing \t missing \t missing")
			info_fail = info_fail + 1
		handle.close()

print("There were %d ids where information could be retrieved and %d ids with missing information" % (info_success, info_fail))
