# General README  

This README file contains introductions to our data and model project along with a list of groups for which we have provided peer feedback. All projects are written in Python 3 language. 

## Data project 

This project aims to fetch, sort, adapt, visualize and describe data from Statistics Denmark.  We look into the Danish current account from 2005 until the newest available dataset from Statistics Denmark. Specifically, we examine the four subaccounts – primary income, secondary income, goods and services - which together sums up the Danish current account Our results are commented and presented in the 'Data_project.IPYNB' notebook. 

The notebook starts out by fetching data from Statistics Denmark through an API. After the data has been cleaned and sorted, we look at the descriptive statistics which we later plot in order to get a deeper understanding of the Danish current account. Lastly, we accumulate the Danish current account through the whole data set in order to see, how much it has amounted to since 2005. 

## Model project 

The aim with this project is to programme an economic model that describes the industry structure when two companies can either compete against each other ála Cournot or collude. The game is known from Industrial Organization and Game Theory e.g. from the Microeconomics III course. 

Our notebook is structured in the following way. First, we find the profits for when the two firms compete ála Cournot. Second, we find the optimal collusion profit i.e. the monopoly profits. Third, we find the optimal deviation profit along with the profit of the firm that has been cheated. Fourth, we write up our bimatrix and solve the game. At the end of the project, we solve the entire game in a single cell such that we can easily reproduce and solve the whole game with other values.     
