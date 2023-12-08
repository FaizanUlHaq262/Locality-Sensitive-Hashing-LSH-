import pandas as pd
import numpy as np
import librosa
import glob
import os
import pickle
import sys
from tqdm import tqdm   #helps to draw a loading bar

class LHS:
    def __init__(self):
        with open(r'dataBaseBuckets.pickle', 'rb') as f:
            self.dbBuckets = pickle.load(f)       #file reading, reads the buckets files of the database stored as a pickle

        with open(r'audioFileNames.pickle', 'rb') as f:
            self.audioNames = pickle.load(f)       #file reading, reads the names of the files of the database stored as a pickle

        with open(r'LOP.pickle' , 'rb') as f:
            self.listOfPermutations = pickle.load(f)

    def fileReader(self,path):
        files = glob.glob(path+ r'\***\**\*', recursive = True)
        audioNames=list()
        mfccList=list()
        for fileName in tqdm(files):
            x , Sr = librosa.load(fileName)
            m = librosa.feature.mfcc(y=x , sr=Sr)
            mfccList.append(m)
            audioNames.append(fileName)        #appends the mp3 file name with extension
        return mfccList,audioNames

    def standerdizer(self,mfccList:list()):
        store=list()        #will store the list of standerdized mfcc list of each audio (for all folder it should be >3000 ) 
        for mfcc in mfccList:
            dotProd=list()
            for inner in mfcc:              #each mfcc has 20 lists of more or less than 1291 elements lists
                padedInner = np.pad(inner , (0, 1293-len(inner)) , 'constant' , constant_values=(0,0))      #pads 0's at the end so all the audios can be of same length, biggest length is 1293
                v = (padedInner - padedInner.mean()) / padedInner.std()
                ranVec=np.random.rand(1293)
                product = np.dot(v, ranVec)         #ranvec is random generated vectors
                if product >= 0:
                    dotProd.append(1)
                else:
                    dotProd.append(0)
            #print(dotProd)
            store.append(np.array(dotProd))
        return store

    def permute(self,store:list() , seedVal: int):   #CALL THE LISTOFPERMUTES FUNCTION INSTEAD OF THIS
        indexes = np.array(list(range(20)))         #makes a list of the indexes of an mfcc (20 in this case)
        np.random.seed(seed=seedVal)                #seed lets me control that a permutation isnt repeated when the function is called again
        # permutation = np.random.permutation(len(indexes))  # generate a random permutation index
        # indexes = [indexes[i] for i in permutation]  # permute list1 using the permutation index
        # audioNames = [audioNames[i] for i in permutation]  # permute list2 using the same permutation index    
        indexes = np.random.permutation(indexes)    #permutes the indexes only once for all of the mfccs (permutation changes when the function is called again with a different seed)
        # oneIndex = list()
        listOneIndex=list()
        for stdMfcc in store:                       #for every standardized mfcc in the list of mfccs
            oneIndex = list()
            oneIndex = [indexes[i] for i, num in enumerate(stdMfcc) if num == 1]        #appends the index of every '1' in the standardized mfcc, ignores all the '0's
            listOneIndex.append((min(oneIndex)))    #finds the minimum value in the list of indexes and apppends it 
        return(listOneIndex)    

    def listOfPermutes(self,store:list()):
        listOfPermutations = list()
        for i in range(20):
            listOfPermutations.append(self.permute(store ,i))
        return listOfPermutations

    def vertSum(self,BAND:list()):
        result = []
        for i in range(len(BAND[0])):
            index_sum = 0
            for j in range(len(BAND)):      # Add the element at this index in the jth list to the sum
                index_sum += BAND[j][i]
            result.append(index_sum)
        return result


    def bucket(self,permList:list() , names:list()):
        band1 = permList[ : int(len(permList)/2) ]          #divides the number of rows into 2 bands (we'll have 20 rows of permutations)
        band2 = permList[int(len(permList)/2) : ]

        sum1 = self.vertSum(band1) 
        sum2 = self.vertSum(band2)
        buckets = {}                #stores all the buckets created with their audio names
        for i in range(len(sum1)):
            if sum1[i] not in buckets:          #if the sum isnt in the dictionary 
                buckets[sum1[i]] = [names[i]]       #makes a new key value bucket inside the dictionary
            else:
                buckets[sum1[i]].append(names[i])       #else it appends the value inside the already available bucket
            
            if sum2[i] not in buckets:          #if the sum isnt in the dictionary
                buckets[sum2[i]] = [names[i]]       #makes a new key value bucket inside the dictionary
            elif sum2[i] != sum1[i]:                #else it checks if theres a bucket already available made by the first list
                buckets[sum2[i]].append(names[i])

        return buckets

    def query_Bucket_Perms(self,path):       #db==database , returns buckets and list of permutations 
        x , Sr = librosa.load(path)
        mfcc = (librosa.feature.mfcc(y=x , sr=Sr))
        mfccStore = list()
        mfccStore.append(mfcc)
        store = self.standerdizer(mfccList=mfccStore)
        listOfPermutations = self.listOfPermutes(store)
        buckets = self.bucket(listOfPermutations , path)
        return buckets , listOfPermutations

    def compare_dicts(self,QUERY:dict(), dataBase:dict(), audioNames:list() , dbLOP:list()):
        result_dict = dict()
        perms_of_results= dict()
        for key in QUERY.keys():        #checks the bucket number in the query buckets
            if key in dataBase:         #sees if key is in database keys too
                paths = dataBase[key]       #stores the value which is a list from database keys
                if paths not in result_dict.values():       #checks if such a list is already in our result dictionary or not
                    perms=list()
                    for name in paths:                  #loops helps us keep track of the permutations of the audio in the bucket, makes a list of all 20 permutation that were in a column into a 1d list
                        if name in audioNames:
                            index = audioNames.index(name)
                            column = [row[index] for row in dbLOP]
                            perms.append(column)        #stores the permutation in the list for later use
                    result_dict[key] = paths
                    perms_of_results[key] = perms
        return result_dict , perms_of_results

    def jaccard_similarity(self,qPerm, sPerm):
        set1 = set(np.array(qPerm).flatten())       #flattens the 2d list
        set2 = set(np.array(sPerm).flatten())       #flattens the 3d list
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        jaccard_similarity = len(intersection) / len(union)    
        return jaccard_similarity

    def sorterFunc(self,names , jaccard):
        data = list(zip(jaccard, names))       # Combine the two lists into a list
        data.sort(reverse=True)                 #sorts from largest to smallest
        name = [item[1] for item in data]     #creates a list of names by extracting the names from the zipped tuples
        jaccs = [jaccard[0] for jaccard in data]
            # Create a set of unique values in list2
        newJacc = set(jaccs)
        # Create a new list that contains elements from list1 where the corresponding element in list2 is a unique value
        newName = [x for x, y in zip(name, jaccs) if y in newJacc]
        data = list(zip(newJacc, newName))       # Combine the two lists into a list
        data.sort(reverse=True)                 #sorts from largest to smallest
        name = [item[1] for item in data]     #creates a list of names by extracting the names from the zipped tuples
        jaccs = [jaccard[0] for jaccard in data]
        return name , jaccs


