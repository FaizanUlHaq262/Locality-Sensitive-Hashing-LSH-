from flask import Flask
from flask import render_template
from flask import request , redirect
import queryProcessing

handleQuery = queryProcessing.LHS()

app=Flask(__name__)

@app.route('/' , methods=['GET'])
def template():
    return render_template('webpage.html')

@app.route('/' , methods=['POST' , 'GET'])
def predict():
    audioFile = request.files['musicFile']    #will request for the audio being uploaded by user in the html
    if audioFile.filename=='':
        print("Invalid File!")
        return redirect(request.url)
    else:
        storing_Path = "./QUERY/" + audioFile.filename   #stores the audio in the uploads folder + the file is stored with the name of audio that was uploaded
        audioFile.save(storing_Path)  #saves the audio on the given path

        queryBucket , queryPerm = handleQuery.query_Bucket_Perms(storing_Path)
        similarDict , simPerms = handleQuery.compare_dicts(queryBucket , handleQuery.dbBuckets ,handleQuery.audioNames , handleQuery.listOfPermutations)
        names=list()
        for i in similarDict.keys():
            for j in similarDict[i]:
                names.append(j[46:])        #seperates the names from the paths

        jaccs=list()                    #stores all the jaccards
        for i in simPerms.keys():
            for j in simPerms[i]:
                jaccs.append(handleQuery.jaccard_similarity(queryPerm , j))

        namesList , jacList = handleQuery.sorterFunc(names , jaccs)

        outputValue = namesList
        return render_template('outputPage.html' , output=outputValue)    #outputs the html page written in the html file

    
if __name__ == '__main__':
    app.run(port=5000 , debug=True)