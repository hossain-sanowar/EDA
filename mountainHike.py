#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 14:52:07 2022

@author: mdsanowarhossain
"""
#Approach 1: Brute Force. I will iterate the whole list and start from each item.
#Runtime: O(n^2)

def planHike(mountains,effort):
    ans = 0
    for i in range(len(mountains)):
        maxMountain = float('-inf')
        minMountain = float('inf')
        
        for j in range(i+1,len(mountains)):
            
            maxMountain = max(maxMountain,mountains[i],mountains[j])
            minMountain = min(minMountain,mountains[i], mountains[j])
            if maxMountain-mountains[j]<=effort and mountains[j]-minMountain<=effort:
                ans = max(ans,j-i+1)
            else:
                break
    return ans


#Test Cases:
    
#Case 1
height1 = [6,2,1,2,2,3,3,3,6]
eff1 = 0

print(planHike(height1,eff1))

#Case 2
height2 = [2,3,4,2,5]
eff2 = 2

print(planHike(height2,eff2))

#Case 3
height3 = [4,1,2,3,5,2,2,1,4]
eff3 = 3

print(planHike(height3,eff3))



