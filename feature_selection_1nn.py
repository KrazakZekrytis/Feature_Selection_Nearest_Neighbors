# -*- coding: utf-8 -*-
"""feature_selection_1nn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z9shCTv0VqP5_yIhQOn-48hq6FiGE8nl
"""

import numpy as np
import copy as cp

#Support Functions

def nearest_neighbors(x, data):

  #calculate Euclidean distance
  distance = np.linalg.norm(x - data)
  return distance

def cross_validation(labels, data):
  distance = []
  prediction = []

  #Begin Loop
  for x in range(len(data)):
    for i in range(len(data)):

      #If x is the data itself, skip
      if np.all(data[x] == data[i]):
        distance.append(float("inf"))
        continue

      #calculate distance
      distance.append(nearest_neighbors(data[x], data[i]))
    
    #retrieve the indice of the nearest data and fetch the label
    nearest_ind = np.argmin(distance)
    prediction.append(labels[nearest_ind])
    distance.clear()

  #calculate accuracy
  accuracy = (np.sum(labels == prediction) / len(data))
  return accuracy

def forward_selection(labels, features, default_rate):
  
  selected_features = []
  accuracy = []
  best_accuracy = 0
  best_features = 0
 
  print('Level [ 0 ] : Default Rate with accuracy: ', default_rate)

  #find first feature to add

  #calculate accuracies per feature
  for i in range(len(features[0])):
    print('Considering selecting feature: ', i + 1)
    accuracy.append(cross_validation(labels, features[:, i]))
    
  #retrieve max indice of the feature with greatest accuravy
  ind_max = np.argmax(accuracy)
  selected_features.append(ind_max)
  print('Level [ 1 ] : Select features:', ind_max + 1, ', with accuracy: ', accuracy[ind_max])
  print('Current Set:', np.array(selected_features) + 1)
  accuracy.clear()

  counter = 2
  #Begin loop with set initialized with first feature found
  while (1):
    for i in range(len(features[0])):
      temp = cp.deepcopy(selected_features)
      if i in temp:

        #if feature is already in set, set accuracy to 0
        accuracy.append(0)
        continue
      temp.append(i)
      print('Considering selecting feature: ', i + 1)
      accuracy.append(cross_validation(labels, features[:, temp]))

    #retrieve max indice to feature with greatest accuracy
    ind_max = np.argmax(accuracy)
    selected_features.append(ind_max)
    print('Level [', counter, '] : Select features:', ind_max + 1, ', with accuracy: ', accuracy[ind_max])
    print('Current Set:', np.array(selected_features) + 1)

    #compare current best feature to overall best feature
    if accuracy[ind_max] >= best_accuracy:
      best_accuracy = accuracy[ind_max]
      best_features = [np.array(cp.deepcopy(selected_features)) + 1, accuracy[ind_max]]
    accuracy.clear()

    #if search reaches the end, break
    if(len(selected_features) == len(features[0])):
      break
    counter += 1

  return best_features
  
def backward_elimination(labels, features, default_rate):

  accuracy = []
  feature = 0
  best_accuracy = 0
  best_features = 0

  #initialize first set with all possible features
  initial = np.arange(len(features[0]))

  print('Level [ 0 ] : Initial features:', initial + 1, ', with accuracy: ', cross_validation(labels, features[:, initial]))
  
  temp = cp.deepcopy(initial)

  counter = 1
  while (1):

    #if search reaches end, break
    if len(temp) == 0:
      break

    #iterate through all elements in temp
    for i in temp:

      #delete an element one by one and calculate accuracy
      temp = np.delete(temp, np.argwhere(temp == i))
      print('Considering eliminating feature: ', i + 1)
      accuracy.append(cross_validation(labels, features[:, temp]))
      temp = cp.deepcopy(initial)

    #retrieve max indice of set with maximum accuracy
    ind_max = np.argmax(accuracy)
    feature = initial[ind_max]

    #delete feature that result in set with max accuracy from initial set
    initial = np.delete(initial, ind_max)
    print('Level [', counter, '] : Eliminate feature:', feature + 1)
    print('Current Set:', initial + 1, ', with accuracy: ', cross_validation(labels, features[:, initial]))

    #compare current best accuracy to overall best accuracy
    if cross_validation(labels, features[:, initial]) >= best_accuracy:
      best_accuracy = cross_validation(labels, features[:, initial])
      best_features = [initial + 1, best_accuracy]
    accuracy.clear()
    temp = cp.deepcopy(initial)
    counter += 1
    
  return best_features

# main program
def main():
  small_data = np.loadtxt('Ver_2_CS170_Fall_2021_Small_data__12.txt')
  small_labels = small_data[:, 0]
  small_features = small_data[:, 1:]
  small_default = np.sum(small_labels == max(small_labels)) / len(small_labels)

  large_data = np.loadtxt('Ver_2_CS170_Fall_2021_LARGE_data__56.txt')
  large_labels = large_data[:, 0]
  large_features = large_data[:, 1:]
  large_default = np.sum(large_labels == max(large_labels)) / len(large_labels)

  print('Feature Selection Using Nearest Neighbors')
  searchInput = input('Pick Search Algorithm (1: Forward Selection, 2: Backward Elimination) : ')
  dataInput = input('Pick Type of Data (1: Small Data, 2: Large Data) : ')

  if(searchInput == '1'): 
    if(dataInput == '1'):
      best_feature = forward_selection(small_labels, small_features, small_default)
      print('Best Feature Set:', best_feature)
    elif(dataInput == '2'):
      best_feature = forward_selection(large_labels, large_features, large_default)
      print('Best Feature Set:', best_feature)
    else:
      print('Invalid Input')
      return
  elif(searchInput == '2'):
    if(dataInput == '1'):
      best_feature = backward_elimination(small_labels, small_features, small_default)
      print('Best Feature Set:', best_feature)
    elif(dataInput == '2'):
      best_feature = backward_elimination(large_labels, large_features, large_default)
      print('Best Feature Set:', best_feature)
    else:
      print('Invalid Data Input')
      return
  else:
    print('Invalid Search Input')
    return

if __name__ == "__main__":
    main()