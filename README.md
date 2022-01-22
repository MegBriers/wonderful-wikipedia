# wonderful-wikipedia
＊*•̩̩͙✩•̩̩͙*˚　HOW TO USE THE CODE ˚*•̩̩͙✩•̩̩͙*˚＊

Please use Mary Somerville as the person whose Wikipedia page we will be analysing. 
I do have another manual file done, but testing is still in early stages.

You can write Mary Somerville with a variety of capitalisation choices, but please ensure there is a space between Mary and Somerville.

When looking for the output of the evaluation of methods, it will be found in the log.txt file in the output folder. 

✨enjoy✨

restart.pygeneral usage:
usage : [desired mathematician] [options : specified NER method]
if desired NER method left out then a comparison of all three methods will be performed (warning : longer running time)
options : 
   option1 = normal spacy method
   option2 = using NTLK
   option3 = retrained spacy models

For each of the tasks mentioned, go to the correpsonding letter's option to find code command on how to do the task : 
(A) Evaluate Spacy performance in identifying people in Wikipedia article 
(B) Evaluate NTLK performance in identifying people in Wikipedia article 
(C) Evaluate retrained Spacy performance in identifying people in Wikipedia article 
(D) Retrain spacy on 19th century mathematicians Wikipedia articles 
(E) Analyse the correspondences of Mary Somerville 
(F) Evaluate all of the methods performances in identifying people in Wikipedia article 


Option A : 
restart.py "Mary Somerville" option1

Option B :
restart.py "Mary Somerville" option2

Option C : 
restart.py "Mary Somerville" option3

Option D : 
retrainingSpacy.py 

Option E : 
letterExtraction.py

Option F : 
restart.py "Mary Somerville" 

