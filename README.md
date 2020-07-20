the file exact_mean calculates the mean scores for two cases deterministically. However, it gets really tedious 
to calculate the standard deviation and the conditional probability.
to get the output of the calculation please change the cursor pointer ( in the command shell) to the CardGame folder 
and then run the following command to printout the results:
python exact_mean.py

Because of that I change my approach to Monte-Carlo simulation.
In order to run the code,change the cursor pointer ( in the command shell) to the CardGame folder 
and then run the following command 

python monte_carlo_solution.py

which asks you to enter an integer number as the number of iteration in the monte-carlo simulation. 
Please enter an integer number and the stat results asked in the quiz will be printed.
the performance is pretty descent for input number less than 100K.
the result will be like this:
"

please set an integer for number of sample in monte-carlo simulation.
1000
--------------------------------
the stats for the case N=26 and M=2 are :
the mean score:  12.003
the standard deviation:  2.531993483403937
the conditional probability:  0.41446028513238287
--------------------------------
the stats for the case N=52 and M = 4 are :
the mean score:  11.947
the standard deviation:  3.002364235065426
the conditional probability:  0.453416149068323
--------------------------------
"
