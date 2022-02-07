import argparse
# reduces a file of co-occurrence counts down to a size suitable for testing purposes
# filters by two terms, an a-term and a c-term
# these two terms should have a recognized indirect connection within the dataset in order to produce a suitable testing set
# this tool can also be used in conjunction with the rest of the package in order to quickly identify if a link between two specified terms exists

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-term-1', '-t1', type=str, default="C0018790") # cardiac arrest
parser.add_argument('-term-2', '-t2', type=str, default="C0342895") # fish eye disease
parser.add_argument('-co-occurrences', '-c', type=str, default="co_occurrence_counts.txt") # co-occurrence counts
args = parser.parse_args()

# initialize reduced counts
reduced_counts = ""

# read and reduce counts
with open(args.co_occurrences) as f:
    for line in f:
        if args.term_1 in line:
            reduced_counts += line
        elif args.term_2 in line:
            reduced_counts += line
f.close()

# write reduced counts
with open("./reduced_counts.txt", 'w') as f:
    f.write(reduced_counts)
f.close()