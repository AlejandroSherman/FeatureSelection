import sys
import copy
import math
from math import floor
from sys import maxsize

#---------Driver-----------
def driver():
  print("Welcome to Alejandro Sherman's Feature Selection Algorithm.\n")

  file_name = input("Type the name of the file to test: ") #get name of file

  try: #try to open
	  dataset = open(file_name, "r")
  except: #fails if not found
	  raise IOError(file_name + " Not found. Try again")

  algorithm_prompt = "Type the number of the algorithm you want to run.\n"
  algorithm_prompt += "\t1\tForward Selection\n"
  algorithm_prompt += "\t2\tBackwards Elimination\n"
  algorithm_prompt += "\t3\tAlejandro's Special Algorithm\n"
  print(algorithm_prompt)

  algorithm_choice = int(input()) #remember that this is an int!!

  #print(algorithm_choice)

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

  print("Please wait while I normalize the data...")
  #normal_instances = original_instances
  normal_instances = z_score_normalize(original_instances, total_features, total_instances)
  print("Done!\n")

  if algorithm_choice == 1:
    test_features = []
    print("\nRunning nearest neighbor with no features (default rate), using \"leaving-one-out\" evaluation, I get an accuracy of " +  str(default_evaluation_function(normal_instances, total_features, total_instances)) + "%\n")
    print("Beginning search.\n")
    forward_selection(normal_instances, total_features, total_instances)
  elif algorithm_choice == 2:
    test_features = []
    for i in range(0, total_features):
      test_features.append(i)
    print("\nRunning nearest neighbor with all features, using \"leaving-one-out\" evaluation, I get an accuracy of " +  str(evaluation_function(normal_instances, test_features, total_features, total_instances)) + "%\n")
    print("Beginning search.\n")
    backward_elimination(normal_instances, total_features, total_instances)
  elif algorithm_choice == 3:
    print("Special algorithm was never implemented")
  else:
    print("Please try again and select an a valid algorithm option")
    sys.exit(0)

  return 0;
#--------------------------

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

#---Default Evaluation function----
def default_evaluation_function(data, features, instances):
  #Simply returns the odds of the most likely choice of the two classes.
  class_one_hits = 0
  class_two_hits = 0
  for i in range(instances):
    if data[i][0] == 1:
      class_one_hits += 1
    else:
      class_two_hits += 1

  if class_one_hits > class_two_hits:
    accuracy = (class_one_hits / instances) * 100.0
  else:
    accuracy = (class_two_hits / instances) * 100.0

  return accuracy
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

#----Forward selection-----
def forward_selection(data, features, instances): #current forward selection search simply uses the given number of features and uses the random evauluation function
  best_accuracy = 0 #save the highest accuracy
  best_features = [] #save the best combination of features
  current_saved_features = [] #hold the current saved features
  immediate_features = [] #hold the features we are testing immediately

  for i in range(1, features + 1): #so 1 - 4 in the simple case
    new_feature = 0 #default
    temp_best_accuracy = 0 #hold the temp best accuracy

    for j in range(1, features + 1):
      if j in current_saved_features: #don't want to consider a feature we already have i.e {1,1}
        continue

      immediate_features = [] #clear
      immediate_features = list(current_saved_features) + [j] #display new feature at the end since I'll be appending later
      accuracy = evaluation_function(data, immediate_features, features, instances)
      print("Using feature(s) " + str(immediate_features) + " accuracy is " + str(accuracy) + "%")

      if accuracy > temp_best_accuracy:
        temp_best_accuracy = accuracy
        new_feature = j #save the best feature to append


    current_saved_features.append(new_feature)

    if temp_best_accuracy > best_accuracy:
      best_accuracy = temp_best_accuracy
      best_features = [] #clear
      best_features = list(current_saved_features)
      print("\nFeature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

    else:
      #if (features <= 10):
      print("\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
      print("Feature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")
      #else:
        #print("\nFinished search!! The best feature subset is "+ str(best_features) + ", which has an accuracy of " + str(floor(best_accuracy*10)/10) + "%\n")
        #return

  print("Finished search!! The best feature subset is "+ str(best_features) + ", which has an accuracy of " + str(floor(best_accuracy*10)/10) + "%\n")
#--------------------------

#---Backward elmination----
def backward_elimination(data, features, instances): #current backward elimination search simply uses the given number of features and uses the random evauluation function - acts somewhat as a mirror of forward selection
  best_accuracy = 0 #save the highest accuracy
  best_features = [] #save the best combination of features
  current_saved_features = list(range(1, features + 1)) #hold the current saved features - initialize to be the full set and keep removing
  immediate_features = [] #hold the features we are testing immediately

  for i in range(1, features + 1): #so 1 - 4 in the simple case
    delete_feature = 0 #default
    temp_best_accuracy = 0 #hold the temp best accuracy

    for j in range(1, features + 1):
      if j not in current_saved_features: #don't want to consider a feature we already removed
        continue

      immediate_features = copy.deepcopy(current_saved_features) #copy the current features
      immediate_features.remove(j)
      accuracy = evaluation_function(data, immediate_features, features, instances)
      print("Using feature(s) " + str(immediate_features) + " accuracy is " + str(accuracy) + "%")

      if accuracy > temp_best_accuracy:
        temp_best_accuracy = accuracy
        delete_feature = j #save the best feature to delete


    current_saved_features.remove(delete_feature)

    if temp_best_accuracy > best_accuracy:
      best_accuracy = temp_best_accuracy
      best_features = [] #clear
      best_features = list(current_saved_features)
      print("\nFeature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

    else:
      #if (features <= 10):
      print("\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
      print("Feature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")
      #else:
        #print("\nFinished search!! The best feature subset is "+ str(best_features) + ", which has an accuracy of " + str(floor(best_accuracy*10)/10) + "%\n")
        #return

  print("Finished search!! The best feature subset is "+ str(best_features) + ", which has an accuracy of " + str(floor(best_accuracy*10)/10) + "%\n")
#--------------------------

if __name__ == "__main__":

  driver() #run driver
