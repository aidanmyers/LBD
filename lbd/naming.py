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