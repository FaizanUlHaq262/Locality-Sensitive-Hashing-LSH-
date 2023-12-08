import queryProcessing

handle = queryProcessing.LHS()

####----------MAIN----------####
mfccList , audioNames = handle.fileReader(r"E:\Faizan_Uniwork\Sem_4\BDA\A1\AudioFiles")
store = handle.standerdizer(mfccList=mfccList)
listOfPermutations = handle.listOfPermutes(store)
buckets = handle.bucket(listOfPermutations , audioNames)

import pickle
with open('dataBaseBuckets.pickle', 'wb') as f:
    pickle.dump(buckets, f)     #file writing

with open('audioFileNames.pickle', 'wb') as f:
    pickle.dump(buckets, f)     #file writing

with open('LOP.pickle', 'wb') as f:
    pickle.dump(listOfPermutations, f)     #file writing