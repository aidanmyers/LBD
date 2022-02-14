# import statements
import argparse
from pathlib import Path

from association import association
from filtering import filter_concepts
from naming import name_concepts
from ranking import linking_term_count, minimum_weight_count
from square_dictionary import SquareDictionary


# main
def main():

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a-terms', '-a', type=str, default=Path.resolve(Path(__file__).parent / "/data/full_test_data/a_terms.txt"), help="path to a text file containing a list of a-terms")
    parser.add_argument('-b-terms', '-b', type=str, default=Path.resolve(Path(__file__).parent / "/data/full_test_data/b_terms.txt"), help="path to a text file containing a list of b-terms")
    parser.add_argument('-c-counts', '-c', type=str, default=Path.resolve(Path(__file__).parent / "/data/full_test_data/c_counts.txt"), help="path to a text file containing a list of co-occurrence counts")
    parser.add_argument('-linking-term-count', '-ltc', action='store_true', default=True, help="use flag to run linking term count")
    parser.add_argument('-minimum_weight_count', '-mwc', action='store_true', help="use flag to run minimum weight count")
    parser.add_argument('-filter-concepts', '-f', action='store_true', default=True, help="use flag to run concept filtering")
    parser.add_argument('-mrsty', type=str, default=Path.resolve(Path(__file__).parent / "/data/metathesaurus/MRCONSO.RRF"), help="path to a MRSTY.RRF metathesaurus file")
    parser.add_argument('-mrconso', type=str, default=Path.resolve(Path(__file__).parent / "/data/metathesaurus/MRSTY.RRF"), help="path to a MRCONSO.RRF metathesaurus file")
    parser.add_argument('-association', action='store_true', default=False, help="use flag to run association measures")
    args = parser.parse_args()

    # gather a-terms, b-terms
    a_terms = open(args.a_terms, 'r').read().splitlines()
    b_terms = open(args.b_terms, 'r').read().splitlines()

    # initialize co-occurrence dictionary
    cooc_dict = SquareDictionary()

    # open co-occurrence file
    with open(args.c_counts) as f:

        # for line in counts
        for line in f:

            # gather term_1, term_2, count
            term_1, term_2, count = line.split('\t')
            count = int(count)

            # if line contains a b-term
            if term_1 in b_terms or term_2 in b_terms:

                # add contents to dictionary
                cooc_dict.add(term_1, term_2, count)

    # concept filtering
    if args.filter_concepts:
        cooc_dict = filter_concepts(cooc_dict, a_terms, b_terms, args.mrsty)

    # initialize output
    output = ""

    # initialize association dictionary
    association_dict = []

    # linking term count
    if args.linking_term_count:
        output, association_dict = linking_term_count(a_terms, b_terms, cooc_dict)

    # minimum weight count
    elif args.minimum_weight_count:
        output, association_dict = minimum_weight_count(a_terms, b_terms, dict)

    # association measures
    if args.association:
        association_output = association(cooc_dict, association_dict)

    # concept naming
    named_output = ""
    named_concepts = name_concepts(cooc_dict, args.mrconso)
    for line in output.splitlines():
        if line.split()[-1] in named_concepts:
            named_line = line + " - " + named_concepts[line.split()[-1]] + "\n"
        else:
            named_line = line + "\n"
        named_output += named_line

    # write ranking output
    with open("ranking_output.txt", "w") as f:
        f.write(named_output)

    # write association output
    with open("association_output.txt", "w") as f:
        f.write(association_output)

# script usage
if __name__ == "__main__":
    main()