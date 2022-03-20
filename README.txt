✨welcome to the code submission of my CS4796 project✨

the code is full of many moving pieces, so this will attempt to give a brief description of how they
all fit together and how to make the code do what you want it to do. 

as well as this document, the guides folder contains
- usage.txt : more detailed breakdown of how to run the code (specifically restart.py) 
- filestructure.txt : detailed description of what is stored where
- extrarequirements.txt : a detailed explanation of external data required to be installed 
- requirements.txt : a pipreqs generated list of required libraries for the code to work 

this should be read in conjuction with the report, specifically appendix A, to understand what 
each file does. 

data (which stores who is mentioned on each wikipedia article) from the most previous run of the code on the 
network will be uploaded with submission.

this means that restart.py can be used to quickly analyse the statistics/methods used to extract the names
without requiring anyone to run the code across the network or the test figures.

if data is regenerated, please delete mentions.csv as well as evaluation.csv for the analysis folder to
get the updated statistics. 

there are three files that can possibly be run 
- restart.py (driver code) 
- retrainingSpacy.py (generates the retraining spacy NER model) 
- results_analysis.R (performs the statistical analysis) 

RETRAININGSPACY
❗❗❗all of the following runs of restart.py requires the maths_ner_model to have been generated❗❗❗
this requires you to run retrainingSpacy.py (warning : generating a new NER model so will 
take a considerable time). no arguments are needed to run this file. 

RESTART
restart.py is the main driver file, and can perform the runs on the test set of figures
as well as the whole network. example runs of restart.py are detailed below, and a more detailed 
usage of the file is given in guides/usage.txt. 

although some of the various options for running take a long time, the data is then permenantly stored
so it is not required to reaccess the articles each time. unless major changes have occurred in any of
the given articles, there is no need to recollect the data at any regular interval. 

example runs of the restart.py 
(A) want to evaluate the performance of all the NER methods on the test set of figures?
benefits : quick run to demo code working

	restart.py test all 

(B) want to run spacy and wikidata extraction methods across the whole network? 
disadvantages : will take a LONG time to run 

	restart.py network 


(C) want to evaluate the epsilon data and assess the most popular figures across the articles?
requires the code to have been run on the network (or the files from previous runs to be present in the output folder)

	restart.py evaluation 

the epsilon results will be found in epsilon.txt in the main folder, and the graphs will generate during running of file

RESULTS_ANALYSIS
the R code also does not require any arguments. it requires mentions.csv to be present in the correct folder,
but the project will be uploaded with this file from a previous run of the code, so it can be run straight away.
the graphs present in section 8 are generated with a run of this code. 