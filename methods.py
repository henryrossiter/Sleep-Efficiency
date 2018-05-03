import pandas
import csv
import datetime
import sys
import data
#returns a set containing all subject numbers with data files in path
def get_subject_nums(path):
    subject_files = os.listdir(path)
    subjects = set()
    for f in subject_files:
        loc = f.find('_')
        if loc == 5 or loc == 6 and f.endswith('.csv'):
            subjects.add(f[:loc])
#takes subject actigraphy csv, trims metadata, and ouputs dataframe
def create_df(raw_csv):
    df = pandas.DataFrame(columns  =['time','sleep_wake'])
    ind = 0
    with open(raw_csv, 'r') as inp:
        for row in csv.reader(inp):
            if len(row)>0 and row[0].isdigit() and int(row[0])==1:
                break
            ind += 1
    df = pandas.read_csv(raw_csv, header=None, names= ["date", "time", "sleep_wake"], skiprows = ind, usecols = [1,2,6], skip_blank_lines=True)
    return(df)



#returns datetime object from data time & date from specified row
def get_datetime_from_df(df, row):
    #print(df.iloc[0,0])
    try:
        [year, month, day] = [int(x) for x in df.iloc[row,0].split('-')]
        [hr, min, sec] = [int(x) for x in df.iloc[row,1].split(':')]
        #print("year:{} month:{} day:{} hour:{} minute:{} second:{}".format(year, month, day, hr, min, sec))
    except:
        print("Couldn't locate data start time and date")
        sys.exit(1)
    t = datetime.datetime(year, month, day, hour = hr, minute = min, second = sec)
    return t

def get_time_from_df(df, row):
    #print(df.iloc[0,0])
    try:
        [hr, min, sec] = [int(x) for x in df.iloc[row,1].split(':')]
        #print("year:{} month:{} day:{} hour:{} minute:{} second:{}".format(year, month, day, hr, min, sec))
    except:
        print("Couldn't locate data start time and date")
        sys.exit(1)
    t = datetime.time(hour = hr, minute = min, second = sec)
    return t



#handles cases of multiple data files for one participant
def consolidate_data(dfs, sub_num):
    print('\nattempting to consolidate multiple data files for subject {}'.format(sub_num))
    #handle unexpected inputs
    if type(dfs) == type(pandas.DataFrame()) or (type(dfs) == type([0]) and len(dfs) == 1):
        print("no consolidation necessary")
        return dfs
    #if subject has more than one data file
    if type(dfs) == type([0]):
        #order data files by start dates
        #insertion sort
        i = 1
        while i< len(dfs):
            j = i
            while j>0 and get_datetime_from_df(dfs[j-1], 0) > get_datetime_from_df(dfs[j], 0):
                temp = dfs[j]
                dfs[j] = dfs[j-1]
                dfs[j-1] = temp
                j= j-1
            i = i+1

        #check all files for duplicates
        for i in range(len(dfs)-1, 0, -1):
            df1 = dfs[i-1]
            df2 = dfs[i]
            #if both files have same start date, remove longer one
            if df1.iloc[0, 0] == df2.iloc[0, 0]:
                print("dataframes had identical start dates")
                if df1.shape[1]<df2.shape[0]:
                    print("df2 had extra data and was removed")
                    dfs.remove(df2)
                else:
                    print("df2 did not have extra data, so df1 was removed")
                    dfs[i-1] = df2
                    dfs.remove(df2)

        if len(dfs) == 1:
            print("after duplicate files were removed, the subject's unique data was found")
            return dfs[0]
        #append discontinuous data
        #e.g: someone wears actigraph for a week, gets new actigraph, wears new actigraph for another week.
        #all data should be appended to create one continuous actigraphy data per participant
        for i in range(len(dfs)-1, 0, -1):
            dt1 = get_datetime_from_df(dfs[i-1],dfs[i-1].shape[0]-1)
            dt2 = get_datetime_from_df(dfs[i],0)
            gap_length = dt2 - dt1
            #print(gap_length)
            #maximum amount of missing data to be ignored (in seconds)
            threshold = datetime.timedelta(0, 3600)
            if gap_length < threshold:
                dfs[i-1] = dfs[i-1].append(dfs[i])
                dfs = dfs[:-1]
            else:
                print("too large of a gap exists between to of the data files for subject {}".format(sub_num))
            if len(dfs) == 1:
                print("after files were appended, the subject's unique data was found")
            else:
                print("!!!WARNING!!! something is wrong with subject {}\'s data. data for subject {} should be checked manually.".format(sub_num, sub_num))
            return dfs[0]




        print("finished! - dfs were removed")
