import pandas as pd

def comparison_of_nodes(method, person):
    """

    A method to give statistics on how accurate the
    method passed in is performing on the wikipedia page

    Parameters
    ----------
    method : string
        how the list of names has been generated
    person : string
        the person whose wikipedia article we are looking at

    Returns
    -------
    None.

    """
    print(":)")

    filename = method + "_" + person

    df = pd.read_csv(filename + ".txt")

    df2 = pd.read_csv("marySomerville_manual.txt")

    columnManual = []

    manualLinked = []
    manualUnLinked = []

    columnMethod = []

    for index, row in df2.iterrows():
        columnManual.append(row["Target"])
        actualRow = row["link"].replace(' ', '')
        if actualRow == "linked":
            manualLinked.append(row["Target"])
        else:
            manualUnLinked.append(row["Target"])

    for index, row in df.iterrows():
        columnMethod.append(row["Target"])

    columnManual = list(set(columnManual))

    columnMethod = list(set(columnMethod))

    manualLinked = list(set(manualLinked))

    manualUnLinked = list(set(manualUnLinked))

    com = list(set(columnManual).intersection(columnMethod))

    print("")

    print("Overall proportion of people picked up")
    print("%.2f" % ((len(com) / len(columnManual)) * 100))

    print("Proportion of unlinked people picked up")
    comUnlinked = list(set(manualUnLinked).intersection(columnMethod))
    print("%.2f" % ((len(comUnlinked) / len(manualUnLinked)) * 100))

    if method == "spacyText":
        print("Proportion of linked people picked up")
        comLinked = list(set(manualLinked).intersection(columnMethod))
        print("%.2f" % ((len(comLinked) / len(manualLinked)) * 100))

    print("")
    print("Additional ones by the method")
    print(list(set(columnMethod).difference(set(columnManual))))
    print("")