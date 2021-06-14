import sys
import math
from math import floor
import time
from sys import maxsize

#---Z Score Normalize function---
def z_score_normalize(data, features, instances):
  mean = [] #hold mean for each row
  for instance in data: #for each row, save the mean of that row
    mean.append(sum(instance)/instances)

  std = [] #hold std
  for instance in data:
    sum1 = 0;
    for i in range(0, features):
      sum1 += pow((instance[i+1] - mean[i]), 2) #need to add one to instances as we skip the classifier in each row
    var = sum1 / instances #get variance
    std.append(math.sqrt(var)) #get and store standard deviation

  #update dataset values in place
  for i in range(0, instances):
	  for j in range(0, features):
		  data[i][j+1] = ((data[i][j+1] - mean[j]) / std[j]) #formula
      #we add 1 to j as we want to skip the first value of the features, as it's the classifier

  return data
#--------------------------

#---------Driver-----------
def driver():
  print("Welcome to Alejandro Sherman's Feature Selection Algorithm.\n")

  file_name = input("Type the name of the file to test: ") #get name of file

  try: #try to open
	  dataset = open(file_name, "r")
  except: #fails if not found
	  raise IOError(file_name + " Not found. Try again")

  #read the first full line of the data to get total size information
  row1 = dataset.readline()

  #the number of features is equal to the number of entries spearated by space -1 (the classifer)
  total_features = len(row1.split()) - 1

  #total number of instances = number of rows (plus row1)
  total_instances = sum(1 for row in dataset) + 1

  dataset.seek(0) #reset position back to the top of the file

  #save un-normalized instances in an array format
  original_instances = [] #create blank instance array
  for i in range(total_instances):
    original_instances.append([]) #create slots for each number of rows

  for i in range(total_instances):
    for j in dataset.readline().split(): #for every column
      original_instances[i].append(float(j)) #fill each slot with row data

  #print("The full original data is:" + str(original_instances))

  print("\nThis dataset has " + str(total_features) + " features (not including the class attribute), with " + str(total_instances) + " instances.\n")

  #Begin normalizing
  start1 = time.time()
  print("Please wait while I normalize the data...")
  normal_instances = z_score_normalize(original_instances, total_features, total_instances)
  print("Done!\n")
  end1 = time.time()
  print("Time to normalize is " + str(end1-start1) + " seconds\n")

  #Hardcode which features to test depending on the file passed in
  test_features = []

  #Test features for small dataset: [3, 5, 7]
  if (total_instances == 100):
    test_features.append(3)
    test_features.append(5)
    test_features.append(7)

  #Test features for large dataset: [1, 15, 27]
  elif (total_instances == 1000):
    test_features.append(1)
    test_features.append(15)
    test_features.append(27)

  else:
    print ("Please try again and select an a valid option")
    sys.exit(0)

  start2 = time.time()
  accuracy = evaluation_function(normal_instances, test_features, total_features, total_instances)
  end2 = time.time()

  print("Time to evaluate (including finding nearest neighbor) is " + str(end2-start2) + " seconds\n")

  print("Running nearest neighbor with the hardcoded features: " +  str(test_features) + " using leave one out evaluation, I get an accuracy of " + str(floor(accuracy*10)/10) + "%.")

  return 0;
#--------------------------

#---Nearest Neighbor function------------
def nearest_neighbor(data, row_to_skip, test_features, features, instances):
  nearest_neighbor = 0
  closest_dist = maxsize

  for i in range(instances): #go through each row
    if row_to_skip == i: #if row to skip? do nothing.
      continue
    else:
      current_distance = 0 #temp distance
      for j in range(len(test_features)): #length of feature subset to test
        #euclidean distance formula
        current_distance = current_distance + pow((data[i][test_features[j]] - data[row_to_skip][test_features[j]]), 2)

      current_distance = math.sqrt(current_distance)

      if current_distance < closest_dist: #nearest so far! set the values
        nearest_neighbor = i #row = the closest instance
        closest_dist = current_distance #new shortest distance

  return nearest_neighbor
#--------------------------

#---Evaluation function----
def evaluation_function(data, test_features, features, instances):
  hits = 0.0 #declare the number of hits as a float
  for i in range(instances):
    row_to_skip = i #iterate on which row to skip
    prediction = nearest_neighbor(data, row_to_skip, test_features, features, instances)

    if data[prediction][0] == data[row_to_skip][0]: #check if the prediction matches the actual value
      hits += 1 #increment hits

  accuracy = (hits / instances) * 100.0 #accuracy formula
  return accuracy
#--------------------------

if __name__ == "__main__":

  driver() #run driver
