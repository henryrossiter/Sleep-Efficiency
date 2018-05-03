import datetime
import methods

class Day(object):
    """A unique day in which a unique subject wore an actigraph"""

    def __init__(self, sub_id, day_num, rep_sleep, rep_wake, day_data_df):
        self.id = sub_id
        self.day_num = day_num
        self.reported_sleep = rep_sleep
        self.reported_wake = rep_wake
        self.data = day_data_df

    #set self.adjusted_sleep to first instance of five minutes with at least 60% sleep values after reported sleep
    def get_adjusted_sleep_start(self):
        i = 0
        [hr, min] = [int(x) for x in self.reported_sleep.split(':')]
        while methods.get_time_from_df(self.data, i) != datetime.time(hour = hr, minute = min):
            i += 1
        j = i
        while self.data.iloc[j:j+10, 2].sum() >= 6 and j < i+60:
            j += 1
        return j # position of adjusted sleep

    #set self.adjusted_wake to last instance before reported wake with five minutes with at least 60% wake values
    def get_adjusted_wake_start(self):
        i = self.data.shape[0] -1
        [hr, min] = [int(x) for x in self.reported_wake.split(':')]
        while methods.get_time_from_df(self.data, i) != datetime.time(hour = hr, minute = min):
            i -= 1
        j = i
        while self.data.iloc[j-10:j, 2].sum() <= 4 and j > i-60:
            j -= 1
        return j #position of adjusted wake

    def get_efficiency(self):
        start_ind = self.get_adjusted_sleep_start()
        stop_ind = self.get_adjusted_wake_start()
        len = stop_ind-start_ind
        tot_act = self.data.iloc[start_ind:stop_ind, 2].sum()
        eff = (len-tot_act)/(len)
        return eff

class Subject(object):
    """a unique subject"""

    def __init__(self, subject_id, redcap_data_df, subject_data_df):
        self.id = subject_id
        self.reported_data_df = redcap_data_df.loc[redcap_data_df['record_id'] == subject_id]
        self.num_days = self.reported_data_df.shape[0]
        self.actigraph_data_df = subject_data_df
        self.days = []

    #create a list of Days, corresponding to the days in self's trial
    #self.actigraph_data_df should be broken into n parts, where n is the trial length in days
    def init_days(self):
        #each 'day' should start at the same time
        start_time = self.actigraph_data_df.iloc[0,1]
        print("start time: "+start_time)
        actigraph_df_copy = self.actigraph_data_df
        curr_day = 0
        while curr_day < self.reported_data_df.shape[0] and actigraph_df_copy.shape[0] != 0:
            i = 1
            while i < actigraph_df_copy.shape[0] and actigraph_df_copy.iloc[i,1] != start_time:
                i += 1
            day_data = actigraph_df_copy[0:i]
            print(i)
            reported_day_data = self.reported_data_df.iloc[curr_day]
            self.days.append(Day(id, curr_day, reported_day_data['sleep_time'], reported_day_data['wakeup_time'], day_data))
            actigraph_df_copy = actigraph_df_copy[i:]
            curr_day += 1
        print("Subject {}\'s {} days have been initialized".format(self.id, curr_day))


    #calculates sleep efficincy for
    def average_efficiencies(self):
        if len(self.days) == self.num_days:
            tot = 0
            for day in self.days:
                tot += day.get_efficiency()
            return tot/self.num_days
        else:
            print('inconsistent amount of efficiencies obtained')
    #returns sleep efficiency values in a user friendly format
    def print_efficiencies(self):
        for d in self.days:
            print()
