# import statements
from collections import UserDict

# square dictionary
# custom dictionary subclass created for the purpose of maintaining a square dictionary
class SquareDictionary(UserDict):
    def __init__(self):
        UserDict.__init__(self)
    
    # add
    # adds a given value to the square dictionary at the given indices, as well as at the reversed indices
    # handles addition at diagonals as to not duplicate values
    def add(self, key_1, key_2, value):

        # if not on diagonal
        # add to both key_1, key_2, count and key_2, key_1, count
        if key_1 != key_2:

            # add key_1, key_2, count
            if key_1 not in self.data:
                self.data[key_1] = {key_2: value}
            elif key_2 not in self.data[key_1]:
                self.data[key_1][key_2] = value
            else:
                self.data[key_1][key_2] += value

            # add key_2, key_1, count
            if key_2 not in  self.data:
                self.data[key_2] = {key_1: value}
            elif key_1 not in self.data[key_2]:
                self.data[key_2][key_1] = value
            else:
                self.data[key_2][key_1] += value

        # else if on diagonal
        # add only once, to key_1, key_2, count
        else:

            # add key_1, key_2, count
            if key_1 not in self.data:
                self.data[key_1] = {key_2: value}
            elif key_2 not in self.data[key_1]:
                self.data[key_1][key_2] = value
            else:
                self.data[key_1][key_2] += value
    
    # get
    # returns any non-zero value stored in the square dictionary at the given indices if it exists, otherwise returns zero
    def get(self, key_1, key_2):

        # handling for non-existent entries
        # return count if exists
        if key_1 in self.data:
            if key_2 in self.data[key_1]:
                return self.data[key_1][key_2]

        # else return zero
        return 0

    # remove
    # removes indices matching removed_key on both axes
    def remove(self, removed_key):

        # handling for non-existent entries on primary axis
        if removed_key in self.data:

            # remove from primary axis
            del self.data[removed_key]

            # for each index on primary axis
            for key in self.data.keys():

                # handling for non-existent entries on second axis
                if removed_key in self.data[key]:

                    # remove from secondary axis
                    del self.data[key][removed_key]

    # cardinality
    # returns the number of non-zero entries across all sub-dictionaries of a given key
    # if the key does not exist in the dictionary, returns zero
    def cardinality(self, key):

        # if key exists
        if self.data[key]:

            # return cardinality of key's sub-dictionary
            return len(self.data.keys())

        # else if key does not exist
        else:

            # return 0
            return 0

    # unique pairs
    # returns all unique pairs present in the square dictionary
    def unique_pairs(self):

        # initialize unique pairs
        unique_pairs = []

        # gather unique pairs
        for key in self.data.keys():
            for subkey in self.data[key].keys():
                if frozenset([key, subkey]) not in unique_pairs:
                    unique_pairs.append(frozenset([key, subkey]))

        # return unique pairs
        return unique_pairs

    # sum counts
    # sums all counts in the square dictionary, excluding duplicates
    def sum_counts(self):
        sum = 0
        summed_sets = []

        # sum all counts
        for key in self.data.keys():
            for subkey in self.data[key].keys():
                if frozenset([key, subkey]) not in summed_sets:
                    summed_sets.append(frozenset([key, subkey]))
                    sum += self.data[key][subkey]
        
        # return sum
        return sum