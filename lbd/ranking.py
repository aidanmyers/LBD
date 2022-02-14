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
    return output, association_dict