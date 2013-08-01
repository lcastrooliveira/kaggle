import csv as csv
import numpy as np

#open up the csv file in to a python object

csv_file_object = csv.reader(open('train.csv','rb'))
header = csv_file_object.next(); #to skip the first line, which is the reader


data = []
for row in csv_file_object:
  data.append(row)
data = np.array(data)

number_passengers = np.size(data[0::,1].astype(np.float))
number_survived = np.sum(data[0::,1].astype(np.float))
proportion_survivors = number_survived / number_passengers

women_only_stats = data[0::,4] == "female"
men_only_stats = data[0::,4] != "female"

women_onboard = data[women_only_stats,1].astype(np.float)
men_onboard = data[men_only_stats,1].astype(np.float)

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print "proportion of women who survived is %s" % proportion_women_survived
print "proportion of men who survived is %s" % proportion_men_survived

print "number_passengers "+str(number_passengers)
print "number_survived "+str(number_survived)
print "proportion_survivors "+str(proportion_survivors)

test_file_object = csv.reader(open('test.csv','rb'))
header = test_file_object.next()

open_file_object = csv.writer(open('genderbasedmodelpy.csv','wb'))

predictions = []

	
for row in test_file_object:
	if row[3] == 'female':		
		predictions.append((row[0],'1'))
		
	else:
		predictions.append((row[0],'0'))

open_file_object.writerow(('PassengerId','Survived'))
for row in predictions:
	open_file_object.writerow(row)

print predictions


fare_ceiling = 40
# makes everything with values superior to 40 equals to 39
data[data[0::,9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling -1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling/fare_bracket_size
number_of_classes = 3 # the 1st 2nd and 3rd class on board
#define the survival table [2x3x4] dimension "sex" "class" "price_ticket"
survival_table = np.zeros((2,number_of_classes,number_of_price_brackets))


for i in xrange(number_of_classes): #search through each class
	for j in xrange(number_of_price_brackets): #search through each price
		woman_only_stats = data[(data[0::,4] == "female") & (data[0::,2].astype(np.float) == i+1) & (data[0::,9].astype(np.float) >= j*fare_bracket_size) & (data[0::,9].astype(np.float) < (j+1)*fare_bracket_size),0]
		
		men_only_stats = data[(data[0::,4] != "female") & (data[0::,2].astype(np.float) == i+1) & (data[0::,9].astype(np.float) >= j*fare_bracket_size) & (data[0::,9].astype(np.float) < (j+1)*fare_bracket_size),0]
		
		survival_table[0,i,j] = np.mean(woman_only_stats.astype(np.float))
		survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))

survival_table[survival_table != survival_table] = 0.0

survival_table[survival_table < 0.5] = 0
survival_table [ survival_table >= 0.5] = 1

test_file_object = csv.reader(open('test.csv','rb'))
fname = "genderclasspricebaseadmodelpy.csv"
open_file_object = csv.writer(open(fname,'wb'))
header = test_file_object.next()

for row in test_file_object: #loop through each passenger
	for j in xrange(number_of_price_brackets):
		try:
			row[8] = float(row[8])
		except:
			bin_fare = 3-float(row[1])
			break
		if row[8] > fare_ceiling:
			bin_fare = number_of_price_brackets-1
			break
		if row[8] >= j*fare_bracket_size and row[8] < (j+1)*fare_bracket_size:
			bin_fare = j
			break
		
		if row[2] == "female":
			row.insert(0,int(survival_table[0,float(row[1])-1,bin_fare]))			
			open_file_object.writerow(row)
		else:
			row.insert(0,int(survival_table[1,float(row[1])-1,bin_fare]))			
			open_file_object.writerow(row)
