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