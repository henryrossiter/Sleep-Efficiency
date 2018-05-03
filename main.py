import pandas as pd
import methods
import data
import os
import sys

#to do - allow different paths to be entered
subject_file_path = ('.')
redcap_survey_path = ('.')

# create set of subject numbers
subject_nums = methods.get_subject_nums(subject_file_path)

#open redcap sleep survey as dataframe
try:
    survey_df = pd.DataFrame.from_csv('redcap_sleepsurvey.csv')
except:
    print('Error: the RedCap survey data could not be opened. Make sure the file is:\n  1) In the correct folder\n  2) Named redcap_sleepsurvey.csv\n  3) Not currently open in Excel')
    sys.exit(1)

### for each element in set of subject numbers
sleep_efficiencies = pd.DataFrame(columns=['subject_id','sleep_efficiency'])
subjects = set()
subject_files = [f for f in os.listdir('.') if f.find('analysis.csv')!=-1]
for sub in subject_nums:
    curr_subs_files = []
    for file in subject_files:
        #if files corresponds to subject number
        if file.find(str(sub))!=0:
            #add file name to curr_subs_files
            curr_subs_files.append(file)
        n_files = length(curr_subs_files)
        if n_files != 1:
            if n_files < 1:
                print("no subject data found for {}".format(sub))
                sys.exit(1)
            if n_files>1:
                #if sub has >1 actigraph file, handle duplicate actigraph file issues
                print("Multiple actigraph files found for subject {}. Attempting to condolidate data...".format(sub))

                #create dfs for each file
                dfs = []
                for file_name in curr_subs_files:
                    dfs.append(methods.create_df(filename))
                consoled_data = consolidate_data(dfs, sub)
                subjects.add(Subject(sub, survey_df, consoled_data))
            else:
                subjects.add(Subject(sub, survey_df, surr_subs_files[0]))



    #initialize sub's trial Days

    #add subject's average sleep efficiency to sleep_efficiencies df
