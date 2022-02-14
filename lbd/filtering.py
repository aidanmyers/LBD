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