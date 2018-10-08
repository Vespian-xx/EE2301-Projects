#Paul Warmuth
#EE2301 XNF Solver
#Created to return cleaned XNF form with a given input.
#Expects input to be in SOP form. ie. A' B C' D + A B C' D etc.
# 'denotes NOT, spaces denote multiplication and + denotes OR

from pip._vendor.distlib.compat import raw_input

# a generalized algebraic expander ie. (a+b)(a+b)=aa+ab+bb. Cleans 1a, a1 to a.
def expand(a, b):
    a = str(a).split("+")
    b = str(b).split("+")
    c = []
    for index1, item1 in enumerate(a):
        for index2, item2 in enumerate(b):
            if "1" not in a[index1]:
                if "1" not in b[index2]:  # (a+x)(b+x)
                    c.extend([item1 + item2])
                else:
                    c.extend([item1])  # (a+x)(1+x)
            if "1" in a[index1]:  # (1+x)(b+x)
                c.extend([item2])
    return "+".join(c)


# this functions looks for and removes duplicate pairs.
def removeduplicates(SOParray):
    for index1, value1 in enumerate(SOParray):
        if len(SOParray) - 1 <= index1:  # happens only if it's gone through the entire list and found no duplicates
            SOParray[:] = ["+".join(i) for i in SOParray]
            SOParray = "+".join(SOParray)
            SOParray = SOParray.split("+") #Some final formatting for the list
            return SOParray
        for index2, value2 in enumerate(SOParray):
            if index2 <= index1:  # prevents it from matching the first item in the list to itself.
                continue
            if value1 == value2:  # removes duplicates in pairs.
                del SOParray[index2]
                del SOParray[index1]
                removeduplicates(SOParray)  # recursively calls the function again with the new partially cleaned list.


# this functions looks for things that need to be expanded, expands them and then removes extraneous list elements
def cleanup(SOParray):  # SOParray is a multilevel array
    for index1, value1 in enumerate(SOParray):
        if len(SOParray[index1]) > 1:
            for index2, value1 in enumerate(SOParray[index1]):
                SOParray[index1][index2] = expand(value1, SOParray[index1][index2 + 1])
                del SOParray[index1][index2 + 1]
                if len(SOParray[index1]) > 1:  # checks to see if each array within the multilevel array has only one element
                                            # This will happen when the subarray has been fully expanded and cleaned.
                    cleanup(SOParray)
    return SOParray


def main():
    while(1):
        raw = raw_input("Enter in SOP form: ")
        SOParray = raw.split(" + ")  # splits the user input into a list of elements that are OR'd together
        SOParray[:] = [x.split(" ") for x in
                       SOParray]  # splits each element into a list of items that are going to be ANDed together
        for index1, value1 in enumerate(SOParray):
            for index2, value2 in enumerate(value1):
                SOParray[index1][index2] = value2.replace("'", "+1")
                # some initial cleanup of the input. Removing all negations and replacing with XOR
            SOParray = cleanup(SOParray)
        SOParray = removeduplicates(SOParray)
        print("^".join(sorted(SOParray, key=len)))


main()
