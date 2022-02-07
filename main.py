# import statements
import argparse
from square_dictionary import SquareDictionary

# main
def main():

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a-terms', '-a', type=str, default="./data/full_test_data/a_terms.txt", help="path to a text file containing a list of a-terms")
    parser.add_argument('-b-terms', '-b', type=str, default="./data/full_test_data/b_terms.txt", help="path to a text file containing a list of b-terms")
    parser.add_argument('-c-counts', '-c', type=str, default="./data/full_test_data/c_counts.txt", help="path to a text file containing a list of co-occurrence counts")
    parser.add_argument('-linking-term-count', '-ltc', action='store_true', default=True, help="use flag to run linking term count")
    parser.add_argument('-minimum_weight_count', '-mwc', action='store_true', help="use flag to run minimum weight count")
    parser.add_argument('-filter-concepts', '-f', action='store_true', default=True, help="use flag to run concept filtering")
    parser.add_argument('-mrsty', type=str, default="./data/metathesaurus/MRSTY.RRF", help="path to a MRSTY.RRF metathesaurus file")
    parser.add_argument('-mrconso', type=str, default="./data/metathesaurus/MRCONSO.RRF", help="path to a MRCONSO.RRF metathesaurus file")
    parser.add_argument('-association', action='store_true', default=True, help="use flag to run association measures")
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


# filter concepts
def filter_concepts(cooc_dict, a_terms, b_terms, mrsty, desired_concept_type="T047"):

    # initialize filtered concepts set
    filtered_concepts = set()
    
    # add a-terms to filtered concepts
    for a_term in a_terms:
        filtered_concepts.add(a_term)
    
    # add b-terms to filtered concepts
    for b_term in b_terms:
        filtered_concepts.add(b_term)

    # open MRSTY metathesaurus file
    with open(mrsty, "r", encoding="UTF-8") as f:

        # iterate through file
        for line in f:

            # gather current cui, current tui
            current_cui = line.split("|")[0]
            current_tui = line.split("|")[1]

            # check if concept is both in co-occurrence dictionary and is of desired concept type
            if current_cui in cooc_dict.keys() and current_tui == desired_concept_type:

                # add to filtered concepts set
                filtered_concepts.add(current_cui)
    
    # remove undesired concepts from co-occurrence dictionary
    keys = list(cooc_dict.keys())
    for key in keys:
        if key not in filtered_concepts:
            cooc_dict.remove(key)

    # return filtered co-occurrence dictionary
    return cooc_dict


# name concepts
def name_concepts(cooc_dict, mrconso):

    # initialize named concepts dictionary
    named_concepts = {}

    # for all seen concepts
    for key in cooc_dict.keys():

        # initialize named concepts dictionary keys
        named_concepts[key] = ""
    
    # open MRCONSO metathesaurus file
    with open(mrconso, "r", encoding="UTF-8") as f:

        # iterate through file
        for line in f:

            # populate named concepts dictionary values
            if line.split("|")[0] in named_concepts.keys() and line.split("|")[1] == "ENG" and line.split("|")[2] == "P":
                named_concepts[line.split("|")[0]] = line.split("|")[14]
    
    # return named concepts
    return named_concepts


# linking term count
def linking_term_count(a_terms, b_terms, cooc_dict):

    # initialize output string
    output = ""

    # initialize linking term count dictionary
    ltc_dict = {}

    # for each a-term
    for a_term in a_terms:

        # initialize linking term count dictionary
        ltc_dict[a_term] = {}

        # add a-term category to output string
        output += a_term + "\n"

        # gather co-occurring b-terms as a set
        ab_set = set()
        for key in cooc_dict[a_term].keys():
            if key in b_terms:
                ab_set.add(key)

        # for key in dictionary
        for key in cooc_dict.keys():

            # if key is not yet in linking term count dictionary
            if key not in ltc_dict[a_term].keys():

                # if key is not a b-term
                if key not in b_terms:

                    # gather co-occurring b-terms as a set
                    cb_set = set()
                    for subkey in cooc_dict[key].keys():
                        if subkey in b_terms:
                            cb_set.add(subkey)
                    ltc_dict[a_term][key] = cb_set & ab_set

    # sort linking term count dictionary and format output
    for a_term in ltc_dict.keys():
        output += a_term + "\n"
        for c_term in sorted(ltc_dict[a_term].keys(), key=lambda c_term: len(ltc_dict[a_term][c_term]), reverse=True):
            output += "\t" + str(len(list(ltc_dict[a_term][c_term]))) + " - " + c_term + "\n"
            for b_term in sorted(ltc_dict[a_term][c_term], key=lambda b_term: cooc_dict.get(c_term, b_term), reverse=True):
                count = cooc_dict.get(c_term, b_term)
                output += "\t\t" + str(count) + " - " + str(b_term) + "\n"
        
    # construct generalized association measure dictionary
    association_dict = {}
    for key in ltc_dict.keys():
        if key not in association_dict.keys():
            association_dict[key] = {}
        for subkey in ltc_dict[key].keys():
            association_dict[key][subkey] = len(ltc_dict[key][subkey])

    # return output, association dictionary
    return output, association_dict


# minimum weight count
def minimum_weight_count(a_terms, b_terms, cooc_dict):

    # initialize output string
    output = ""

    # initialize minimum weight count dictionary
    mwc_dict = {}

    # for each a-term
    for a_term in a_terms:

        # if a-term is not yet in minimum weight count dictionary
        if a_term not in mwc_dict.keys():

            # initialize a-term in dictionary
            mwc_dict[a_term] = {}

        # for c-term
        for c_term in cooc_dict.keys():
            if c_term not in b_terms:

                # if c-term is not yet in minimum weight count dictionary
                if c_term not in mwc_dict[a_term].keys():

                    # if c-term shares b-terms with a-term
                    if set(cooc_dict[a_term].keys()) & set(cooc_dict[c_term].keys()) & set(b_terms):

                        # initialize c-term in dictionary
                        mwc_dict[a_term][c_term] = {}
                    
                    # else, skip
                    else:
                        continue

                # for b-term connecting a-term and c-term
                for b_term in list(set(cooc_dict[a_term].keys()) & set(cooc_dict[c_term].keys()) & set(b_terms)):
                    
                    # if b-term is not yet in minimum weight count dictionary
                    if b_term not in mwc_dict[a_term][c_term].keys():

                        # initialize b-term in dictionary
                        mwc_dict[a_term][c_term][b_term] = 0
                    
                    # determine and assign minimum weight count
                    mwc_dict[a_term][c_term][b_term] = min(mwc_dict[a_term][c_term][b_term], cooc_dict[a_term][b_term], cooc_dict[c_term][b_term])

    # sort minimum weight count dictionary and format output    
    for a_term in mwc_dict.keys():
        output += a_term + "\n"
        for c_term in sorted(mwc_dict[a_term].keys(), key=lambda c_term: sum(mwc_dict[a_term][c_term].values()), reverse=True):
            output += "\t" + str(sum(mwc_dict[a_term][c_term].values())) + " - " + c_term + "\n"
            for b_term in sorted(mwc_dict[a_term][c_term], key=lambda b_term: mwc_dict[a_term][c_term][b_term], reverse=True):
                output += "\t\t" + str(mwc_dict[a_term][c_term][b_term]) + " - " + b_term + "\n"
    
    # construct generalized association measure dictionary
    association_dict = {}
    for key in mwc_dict.keys():
        if key not in association_dict.keys():
            association_dict[key] = {}
        for subkey in mwc_dict[key].keys():
            association_dict[key][subkey] = sum(mwc_dict[key][subkey].values())

    # return output, association dictionary
    return output

# association
def association(cooc_dict, association_dict, equation_string="pcs"):

    # initialize score dictionary
    score_dict = {}

    # for each a-term
    for a_term in association_dict.keys():

        # determine n1p
        n1p = len(cooc_dict[a_term].values())
        # determine npp
        npp = cooc_dict.sum_counts()
        # determine n2p
        n2p = npp - n1p

        # for each c-term
        for c_term in association_dict[a_term].keys():

            # determine n11
            n11 = association_dict[a_term][c_term]
            # determine np1
            np1 = len(cooc_dict[c_term].values())
            # determine np2
            np2 = npp - np1
            # determine n12
            n12 = len(list(key for key in cooc_dict[a_term].keys() if key is not c_term))
            # determine n21
            n21 = len(list(key for key in cooc_dict[c_term].keys() if key is not a_term))
            # determine n22
            n22 = len(list(item for item in cooc_dict.unique_pairs() if a_term not in item and c_term not in item))
            # determine m11
            m11 = (n1p * np1) / npp
            # determine m12
            m12 = (n1p * np2) / npp
            # determine m21
            m21 = (np1 * n2p) / npp
            # determine m22
            m22 = (np1 * n2p) / npp

        # pearson's chi squared
        if equation_string == "pcs":

            # initialize score
            score = 0
            # m11
            score += (n11 - m11) / m11
            # m12
            score += (n12 - m12) / m12
            # m21
            score += (n21 - m21) / m21
            # m22
            score += (n22 - m22) / m22
            # multiply by two
            score *= 2
            # store score
            score_dict[frozenset([a_term, c_term])] = score

    # return score dictionary
    return score_dict

# script usage
if __name__ == "__main__":
    main()