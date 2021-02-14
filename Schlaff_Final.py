# -*- coding: utf-8 -*-
"""
Created on Sun May 17 16:47:32 2020

@author: brian
"""

### Brian Schlaff
### Comp Sci 450.2 Final 


#Import Packages 
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# Load CSV data for 2017 income and 2014 Tree canopy cover into dataframes
TreeDF = pd.read_csv (r'C:\Users\brian\OneDrive\Desktop\Exploratory Data Analysis and Visualization\Final\Tree_Canopy_in_Urban_and_Non-Urban_LA_County__2014.csv')

IncomeDF = pd.read_csv (r'C:\Users\brian\OneDrive\Desktop\Exploratory Data Analysis and Visualization\Final\Living_Wage__2017_.csv')


#establish empty dataframe with columns for census tract number, medium income, and canopy area, in order to store data that is linked through common tract numbers

column_names = ["Census Tract","Medium Income","Can_P"]

CombinedDF = pd.DataFrame(columns = column_names)

# Loop through the census tract column of each datasets, link them, and append to empty dataframe

total = (len(TreeDF))*(len(IncomeDF))
count = 0

for i in range(0,len(IncomeDF),1):
    IncID = IncomeDF.iloc[i]['CENSUS_TRACT']
    
     #nested for loop to match data of the same census tract data
    for j in range(0,len(TreeDF),1):
        TreeID = TreeDF.iloc[j]['CENSUS_TRACT']
        
        count += 1
        percent = 100*(count/(total))
        percent = round(percent,3)
        print (count, 'Completion:',percent,'%')
        
        if  IncID == TreeID:
            
            newRow = {"Census Tract":(IncomeDF.iloc[i]['CENSUS_TRACT']),"Medium Income":(IncomeDF.iloc[i]['MedIncome']),"Can_P":(TreeDF.iloc[j]['Can_P'])}
            
            CombinedDF = CombinedDF.append(newRow,ignore_index=True)
           

# Export dataframe to csv
CombinedDF.to_csv('Combined.csv')
        
# Reload CombinedDF so you don't need to rerun nested for loop after closing program
Combined = pd.read_csv(r'C:\Users\brian\OneDrive\Desktop\Exploratory Data Analysis and Visualization\Final\Combined.csv')

column_names = ["Census Tract","Medium Income","Can_P"]

CombinedDF = pd.DataFrame(columns = column_names)

# Remove extra index column
Combined = Combined.drop('Unnamed: 0', axis = 1)

#Create a dictionary to reduce repeated Medium Income Values and average their corresponding canopy area percentages.

dict = {}  
 
for k in range(0,len(Combined),1):
    
    key = Combined.iloc[k]['Medium Income']
    
    
    if key not in dict.keys():
        
        ttl = 0
        cnt = 0
        
        for ii in range(k,len(Combined),1):
            
            if Combined.iloc[ii]['Medium Income'] == key:
                ttl += Combined.iloc[ii]['Can_P']
                cnt += 1
            
                Avg_Can  = ttl/cnt   
    
        dict.update({key:Avg_Can})

    
#Create a new dataframe with averaged canopy area
DictDF = pd.DataFrame.from_dict(dict, orient= 'index')

#Convert dictionary to csv, and reimport it as a dataframe inorder to change keys from index position to column position.
DictDF.to_csv('DictDF.csv')

# reimport Dictionary csv and load it into a dataframe
UpdateDF = pd.read_csv(r'C:\Users\brian\OneDrive\Desktop\Exploratory Data Analysis and Visualization\Final\DictDF.csv')

UpdateDF.rename(columns={"Unnamed: 0":"Medium Income ($)", "0":"Canopy Area (%)"}, inplace= True)

# Add a new column Income Bracket to the dataframe to by examing the Medium income value and assigning a bracket value to it

# Empty Brackets to count the amount of values in each income bracket
Brckt1 = 0
Brckt2 = 0
Brckt3 = 0
Brckt4 = 0
Brckt5 = 0
Brckt6 = 0
Brckt7 = 0

#Empty dataframe to store the new column
IncomeBracket = pd.DataFrame()

#loop through medium income column and add an income bracket to the data
for III in range(0,len(UpdateDF),1):
    
    Income = UpdateDF.iloc[III]['Medium Income ($)']
    
    if Income <= 25000:
        
        Brckt1 += 1
        AddRow = {'Income Bracket':'0 - 25K ($)'}
        IncomeBracket = IncomeBracket.append( AddRow, ignore_index=True)
        
    
    elif 25001 < Income <= 50000:
        
        Brckt2 += 1
        AddRow = {"Income Bracket":"25K - 50K ($)"}
        IncomeBracket = IncomeBracket.append( AddRow, ignore_index=True)
        
    elif 50001 < Income <= 75000:
        
        Brckt3 += 1
        AddRow = {"Income Bracket":"50K - 75K ($)"}
        IncomeBracket = IncomeBracket.append( AddRow,ignore_index=True)
        
    elif 75001 < Income <= 100000:
        
        Brckt4 += 1
        AddRow = {"Income Bracket":"75K - 100K ($)"}
        IncomeBracket = IncomeBracket.append( AddRow,ignore_index=True)
    
    elif 100001 < Income <= 125000:
        
         Brckt5 += 1
         AddRow = {"Income Bracket":"100K - 125K ($)"}
         IncomeBracket = IncomeBracket.append( AddRow,ignore_index=True)
        
    elif 125000 < Income <= 150000:
        
         Brckt6 += 1
         AddRow = {"Income Bracket":"125K to 150K ($)"}
         IncomeBracket = IncomeBracket.append( AddRow,ignore_index=True)
        
    else:
        
         Brckt7 += 1
         AddRow = {"Income Bracket":"150K + ($)"}
         IncomeBracket = IncomeBracket.append( AddRow,ignore_index=True)

# Append IncomeBracket Column to UpdateDF
UpdateDF = pd.concat([UpdateDF,IncomeBracket], axis=1)

#Export dataframe to csv file for Visualization in Tableau
UpdateDF.to_csv('Schlaff_Final.csv')




##### Analyze and plot the data

#convert data frame rows into arrays to be used in numpy
X = UpdateDF.iloc[:, 0].values
Y = UpdateDF.iloc[:, 1].values 

#run a least squares regression.

#Find the mean of X and Y
MeanX = np.mean(X)
MeanY = np.mean(Y)

#establish and set the numerator and denomenator equal to 0
numer =  0
denomer = 0

for ix in range(0,len(X),1):
    numer += (X[ix] - MeanX)*(Y[ix] - MeanY)
    denomer += (X[ix] - MeanX)**2
    
#Calculate the slope of line of best fit (m), the Y intercept (c), and establish the equation
m = numer / denomer
c = MeanY - (m*MeanX)

Y_Predicted = c + X*m

# Equation to calculate the r^2 value of the line of best fit
num = 0
den = 0
for iy in range(0,len(Y),1):
    den += (Y[iy] - MeanY)**2
    num += (Y_Predicted[iy] - MeanY)**2
    
R2 = num/den
print(R2)

#Plot the data 
plt.xlabel('Medium Income ($)')
plt.ylabel('Canopy Area (%)')
plt.title('Scatter Plot')
plt.scatter(X, Y, marker='x')
plt.plot([min(X),max(X)],[min(Y_Predicted),max(Y_Predicted)], color = 'red')





            
            
        
        

            
            


    


            
        
    




