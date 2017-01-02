import numpy as np
import itertools
import os

'''Ulrik Soderstrom
CSC 440
10/24/16
Apriori Algorithm with Improvement'''

#Opening Data File 

Min_Sup = input("Please enter an integer value support count: ")

path = input("Enter path to a folder with data ")
os.chdir(path)

filename = input("Enter a filename of data set in folder ")

Data_File = open(path + "/" + filename, "r")


Data_Set = []

Data_File = open("/Users/Ulrik/Desktop/data.txt", "r")

for line in Data_File:
        line_list = [x.strip(",") for x in line.lower().split()]
        Data_Set.append(line_list)

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#Min_Sup = 150
print("\n")

#Generates Candidate from Data File
def Generate_Ci(Item_Set):
    Ci = []
    for i in range(0, len(Item_Set)):
        for item in Item_Set[i]:
            Ci.append(item)
    return Ci

#Prunes first set of candidates
def Prune_Ci(Ci): 
    Pruned_Ci = []
    for item in Ci:
        if(Ci.count(item) >= Min_Sup):
            if item not in Pruned_Ci:
                Pruned_Ci.append(item)
    return Pruned_Ci

#Prunes candidates at each new item set length
def Prune_Can_Pass(Ci):
    Pruned_Ci = []
    for item in Ci:
        if item not in Pruned_Ci:
            Pruned_Ci.append(item)
    return Pruned_Ci

#Generates candidate sets and subsets of all pruned candidates
def Generate_Candidate_Sets(Candidate_items, Set_Length):
    Candidate_item_sets = {}
    for L in range(Set_Length, Set_Length+1):
        for subset in itertools.combinations(Candidate_items, L):
            Candidate_item_sets[subset] = 0
    return Candidate_item_sets

#Find occurences of candidate itemsets in database at a given item set length
def Compare_Candidate_Sets_to_DataBase (Data_base, Candidate_item_sets, Set_Length, min_sup):
    Frequent_Item_Sets = []
    PossibleSets = [] 
    for item in Data_base:
        for L in range(Set_Length, Set_Length+1):
            for subset in itertools.combinations(item, L):
                if subset in Candidate_item_sets:
                    Candidate_item_sets[subset] = (Candidate_item_sets[subset] + 1)
    return Candidate_item_sets

#generate list from dictionary
def Generate_Candidate_Set_From_Dict (Dictionary):
    Next_Candidate_Set = []
    for item in Dictionary:
        for i in range(0, len(item)):
            Next_Candidate_Set.append(item[i])
    return Next_Candidate_Set

#Prune candidate itemsets that occured in dictionary based on minimum support
def prune_frequent_sets (Dictionary, min_sup):
    New_Dictionary = {}
    for item in Dictionary:
        if Dictionary[item] >= min_sup:
            if Dictionary[item] not in New_Dictionary:
                New_Dictionary[item] = Dictionary[item]
            else: 
                New_Dictionary[item] = (New_Dictionary[item] + Dictionary[item])
    return New_Dictionary

#IMPROVEMENT :: Prune dataebase at each level of rows that have no frequent items
def prune_database (Database, Candidate_set):
    New_Database = []
    for i in range(0,len(Database)):
        for item in Database[i]:
            if item in Candidate_set:
                New_Database.append(Database[i])
                break
    return New_Database

print("Apriori Initiating")
print("\n")
print("Please allow ~2.5 minutes to complete")

C1 = Generate_Ci(Data_Set)
C1_Pruned = C1

print("\n")

def Apriori_Main(Data_base, min_sup, Candidate_set, Set_Length, Frequent_Items):
    print("Discovering frequent items at length of: ")
    print(Set_Length)
    Candidate_set = Prune_Can_Pass(Candidate_set)
    if Set_Length > 2:
        Data_base = prune_database(Data_base, Candidate_set)
    Cn_Candidate_Sets = Generate_Candidate_Sets(Candidate_set, Set_Length)
    Candidate_item_sets_n = Compare_Candidate_Sets_to_DataBase(Data_Set, Cn_Candidate_Sets, Set_Length, min_sup)
    Candidate_item_sets_n = prune_frequent_sets(Candidate_item_sets_n, min_sup)
    Candidate_set = Generate_Candidate_Set_From_Dict(Candidate_item_sets_n)
    Frequent_Items.append(Candidate_item_sets_n)
    print("Frequent item sets discovered! Continuing to next set length")
    if len(Candidate_set) == 0:
        return Frequent_Items
    else: 
        print("\n")
        Set_Length += 1
        return Apriori_Main(Data_base, min_sup, Candidate_set, Set_Length, Frequent_Items)


Frequent_Items = []
Frequent_Items_Total = Apriori_Main(Data_Set, Min_Sup, C1_Pruned, 2, Frequent_Items)

length = 2
for item in Frequent_Items_Total:
    if len(item) == 0:
        break
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Frequent Item Sets of length: ")
    print(length)
    print("\n")
    print("Below are items sets and support counts:")
    print(item)
    print("\n")
    length += 1

print("Apriori Complete")
    
