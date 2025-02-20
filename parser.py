import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP
NP -> N | Det NP | Adj NP | NP P NP
VP -> V | VP NP | VP PP | Adv VP | VP Adv | VP Conj VP
PP -> NP P NP | P NP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    token_list = nltk.tokenize.word_tokenize(sentence)
    word_list = []
    for token in token_list:
        if any(c.isalpha() for c in token):
            word_list.append(token.lower())
    
    return word_list

def recursive_np_chunk(np_chunk_list, ptree):
        # If leaf, return True if chunk 
        if len(ptree) == 1:
            if ptree.label() == "NP":
                np_chunk_list.append(ptree)
                return True
            return False

        chunk_counter = 0
        for sub_tree in ptree:
            if (recursive_np_chunk(np_chunk_list, sub_tree)):
                chunk_counter += 1
        
        if chunk_counter == 1 and ptree.label() == "NP":
            np_chunk_list.append(ptree)
            return True
        return False
            

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    ret_list = []
    recursive_np_chunk(ret_list, tree)
    
    return ret_list

if __name__ == "__main__":
    main()
