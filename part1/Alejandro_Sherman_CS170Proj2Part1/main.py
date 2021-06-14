import sys
import random
import copy

#---------Driver-----------
def driver():
  random.seed()
  print("Welcome to Alejandro Sherman's Feature Selection Algorithm.\n")

  feature_num = int(input("Please enter total number of features: "))
  if (feature_num < 0):
    print("Please try again and select a valid feature number")
    sys.exit(0)

  #print (feature_num)

  algorithm_prompt = "Type the number of the algorithm you want to run.\n"
  algorithm_prompt += "\t1\tForward Selection\n"
  algorithm_prompt += "\t2\tBackwards Elimination\n"
  algorithm_prompt += "\t3\tAlejandro's Special Algorithm\n"
  print(algorithm_prompt)

  algorithm_choice = int(input()) #remember that this is an int!!

  #print(algorithm_choice)

  if algorithm_choice == 1:
    print("\nUsing no features and \"random\" evaluation, I get an accuracy of " +  str(evaluation_function()) + "%\n")
    print("Beginning search.\n")
    forward_selection(feature_num)
  elif algorithm_choice == 2:
    print("\nUsing all features and \"random\" evaluation, I get an accuracy of " +  str(evaluation_function()) + "%\n")
    print("Beginning search.\n")
    backward_elimination(feature_num)
  elif algorithm_choice == 3:
    print("Special algorithm not implemented yet")
  else:
    print("Please try again and select an a valid algorithm option")
    sys.exit(0)

  return 0;
#--------------------------

#---Evaluation function----
def evaluation_function(): #current evaluation function is simply a stub that returns a random value
  raw_random_accuracy = random.random() * 100
  random_accuracy = round(raw_random_accuracy, 1)
  return random_accuracy
#--------------------------

#----Forward selection-----
def forward_selection(feature_num): #current forward selection search simply uses the given number of features and uses the random evauluation function
  best_accuracy = 0 #save the highest accuracy
  best_features = [] #save the best combination of features
  current_saved_features = [] #hold the current saved features
  immediate_features = [] #hold the features we are testing immediately

  for i in range(1, feature_num + 1): #so 1 - 4 in the simple case
    new_feature = 0 #default
    temp_best_accuracy = 0 #hold the temp best accuracy

    for j in range(1, feature_num + 1):
      if j in current_saved_features: #don't want to consider a feature we already have i.e {1,1}
        continue

      immediate_features = [] #clear
      immediate_features = list(current_saved_features) + [j] #display new feature at the end since I'll be appending later
      accuracy = evaluation_function()
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
      print("\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
      print("Feature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

  print("Finished search!! The best feature subset is " + str(best_features) + ", which has an accuracy of " + str(best_accuracy) + "%\n")
#--------------------------

#---Backward elmination----
def backward_elimination(feature_num): #current backward elimination search simply uses the given number of features and uses the random evauluation function - acts somewhat as a mirror of forward selection
  best_accuracy = 0 #save the highest accuracy
  best_features = [] #save the best combination of features
  current_saved_features = list(range(1, feature_num + 1)) #hold the current saved features - initialize to be the full set and keep removing
  immediate_features = [] #hold the features we are testing immediately

  for i in range(1, feature_num + 1): #so 1 - 4 in the simple case
    delete_feature = 0 #default
    temp_best_accuracy = 0 #hold the temp best accuracy

    for j in range(1, feature_num + 1):
      if j not in current_saved_features: #don't want to consider a feature we already removed
        continue

      immediate_features = copy.deepcopy(current_saved_features) #copy the current features
      immediate_features.remove(j)
      accuracy = evaluation_function()
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
      print("\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
      print("Feature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

  print("Finished search!! The best feature subset is "+ str(best_features) + ", which has an accuracy of " + str(best_accuracy) + "%\n")
#--------------------------

if __name__ == "__main__":

  driver() #run driver
