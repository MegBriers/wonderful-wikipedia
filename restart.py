import sys
import os
import re

# code needs to

# methods : [option 1] [option 2] [option 3] [comparison option]

# for a specified wikipedia page and method
    # check we have the comparison data for that specified page ✓
        # if not then reject name ✓
        # if we have the comparison data ✓
            # if not comparison
                # get all the names using that specified method
                    # linked
                    # unlinked
                # give a statistical summary of how well it has performed
            # if no second argument given
                # do all three methods
                # provide individual statistical summary of how well each performed
                # do statistics for the comparison of methods


def validateName(name):
    print("hello")
    # reformat the names
    pattern = re.compile(r'\s+')
    name = re.sub(pattern, '', name.lower())
    filePath = './people/' + name + '.txt'
    return os.path.isfile(filePath)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        print("usage : [desired mathematician] [options : specified NER method]")
        print("if desired NER method left out then a comparison of all three methods will be performed (warning : longer running time)")
        print("options : ")
        print("option1 = normal spacy methods")
        print("option2 = using wikidata")
        print("option3 = retrained spacy model")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        exit(0)

    if (validateName(sys.argv[1])):
        print("yay")
        if len(sys.argv) > 3:
            # perform the specific method
        else:
            # do all three methods
    else:
        print("error message")