# Bundestagswahl-2017-Election-

Task1:
Computes the percentage of Zweitstimmen for each political party in the 2017 Bundestagswahlen, using ergebnisse.csv as data source. 
Output format is:

Party;Percentage

Filename: result1.csv



Task2:
Displays a bar chart of the Zweitstimmen result of the elections. Uses pyplot to draw the diagram.

The diagram looks similar to https://www.bundeswahlleiter.de/bundestagswahlen/2017/ergebnisse.html.
Uses color codes for the parties, and combines every party below 5% into Sonstige.
Displays the numeric values at the top of the bar.


Filename: Diagram.png



Task3:
For this and the next exercise, familiarize yourself with the procedure for seat distribution in the Bundestag.

* Method of Sainte-Laguë/Schepers
* Computation of Mindestsitzzahl

For this assignment, compute the Mindestsitzzahl for each party and each state.

Implement the method of Saint-Lesque/Schepers in a reusable manner
For each constituency, compute the winning party of the direct seat (Direktmandat). For each state, compute the number of direct seats per party
Compute a distribution of 598 seats to the states, according to the population count in population.csv (source: bundeswahlleiter.de)
For each state, compute the assignment of seats to the parties according to the share of Zweitstimmen.
Print out a list of states (by name) and parties with number of direct seats and list seats, as well as the number of seats by  which the direct seats are larger than the list seats (Überhangmandate) (0 if the number is not larger). 

Produce a CSV output of the form
state;party;direct_seats;list_seats;ueberhang

Filename: result3.csv

