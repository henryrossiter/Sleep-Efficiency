import methods
import pandas
import data

f1 = "duplicate_testing/30091_1_18_2018_2_12_12_PM_New_Analysis.csv"
f2 = "duplicate_testing/30091_1_6_2018_2_30_00_PM_New_Analysis.csv"
f = "duplicate_testing/redcap_sleepsurvey.csv"
df1 = methods.create_df(f1)
df2 = methods.create_df(f2)
#df = methods.consolidate_data([df1, df2], 22)
redcap_df = pandas.read_csv(f)
test_sub = data.Subject(192, redcap_df, df1)
test_sub.init_days()
for d in test_sub.days:
    print(str(d.get_adjusted_sleep_start())+"  "+ str(d.get_adjusted_wake_start()))
    print("efficiency: "+str(d.get_efficiency()))
print(test_sub.average_efficiencies())
