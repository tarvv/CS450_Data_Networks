/*
 * caravandelay.cpp will calculate the time it takes for a caravan of cars to
 * make it through a journey, mimicking the analogy presented in ch1 of Computer
 * Networking: A Top-Down Approach. Queries standard output for data, then
 * displays results after calculating time.
 *
 * Created for week 1 class assignment in CS450 at Regis University.
 *
 * @date 1/15/21
 * @author: Travis Suggitt
 */

#include <string>
#include <iostream>
#include <limits>
#include <ios>
using namespace std;

//Constant definitions
#define MININHOUR 60
#define SECINMIN 60

//Caravan structure definition
struct Caravan {
	int numTolls;
	int speedLimit;
	int numCars;
	int numLinks;
};

//Function declarations
int calcTotalDelay(Caravan c, int *delays, int *distances);
int queryNumTolls();
int queryDelay(int i);
int queryDist(int i);
int querySpeed();
int queryNumCars();
void dispData(Caravan c, int totalTime, int *delays, int *distances);

/*
 * Main function calls other functions, modifies Caravan struct, and loops
 * delays and distances arrays to calculate the time to complete the journey.
 */
int main()
{
	struct Caravan c;
	int totalTime;

	c.numTolls = queryNumTolls();
	int delays[c.numTolls];
	c.numLinks = c.numTolls-1;
	int distances[c.numLinks];

	cout << "Enter each toll's processing delay in seconds per car\n";
	for (int i = 0; i < c.numTolls; i++) {
		delays[i] = queryDelay(i);
	}

	cout << "Enter the distance between tolls in km\n";
	for (int i = 0; i < c.numLinks; i++) {
		distances[i] = queryDist(i);
	}
	c.speedLimit = querySpeed();
	c.numCars = queryNumCars();

	totalTime = calcTotalDelay(c, delays, distances);
	dispData(c, totalTime, delays, distances);

	return 0;
}

/*
 * Calculates the total delay time of caravan through final toll gate in seconds.
 * Time is calculated by iteratively summing the time a toll gate takes to get
 * all cars through (transmission delay) plus the time a car takes to get to the
 * succeeding toll gate (propagation delay). Then the final toll gates time is
 * added to the total.
 *
 * @param c - struct holding Caravan values
 * @param delays - pointer to int array of delays
 * @param distances - pointer to int array of distances
 * @return totalDelay - int total delay time in seconds
 */
int calcTotalDelay(Caravan c, int *delays, int *distances) {
	int totalDelay = 0;
	for (int i = 0; i < c.numLinks; i++) {
		totalDelay += (delays[i] * c.numCars) +
				(float(distances[i]) / c.speedLimit * MININHOUR * SECINMIN);
	}
	totalDelay += delays[c.numTolls-1] * c.numCars;
	return totalDelay;
}

/*
 * Queries standard output for the number of tolls on route. Checks for integer
 * input.
 *
 * @return numTolls - number of tolls on route
 */
int queryNumTolls() {
	int numTolls;
	cout << "Enter the number of toll gates (include initial and final tolls): ";
	while(1) {
		cin >> numTolls;
		if(!cin.fail()) {
			break;
		}
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "Must be an integer, try again\n";
	}
	return numTolls;
}

/*
 * Queries standard output for the time that a toll booth takes to service a
 * car in seconds. Checks for integer input.
 *
 * @param i - ith toll on route, used for display purposes only
 * @return tollDelay - seconds to service a car
 */
int queryDelay(int i) {
	int tollDelay;
	cout << "Toll " << i+1 << ": ";
	while(1) {
		cin >> tollDelay;
		if(!cin.fail()){
			break;
		}
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "must be an integer, try again\n";
	}
	return tollDelay;
}

/*
 * Queries standard output for the distance from a toll booth to the next in km.
 * Checks for integer input.
 *
 * @param i - ith toll on route, used for display purposes only
 * @return dist - distance between toll booths
 */
int queryDist(int i) {
	int dist;
	cout << "Toll " << i+1 << " to " << i+2 << ": ";
	while(1) {
		cin >> dist;
		if(!cin.fail()){
			break;
		}
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "must be an integer, try again\n";
	}
	return dist;
}

/*
 * Queries standard output for the speed of cars in the caravan in kph. Checks
 * for integer input.
 *
 * @return speedLimit - Speed that the cars travel
 */
int querySpeed() {
	int speedLimit;
	cout << "Enter the speed limit in kph: ";
	while(1) {
		cin >> speedLimit;
		if(!cin.fail()){
			break;
		}
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "must be an integer, try again\n";
	}
	return speedLimit;
}

/*
 * Queries standard output for the number of cars in the caravan. Checks for
 * integer input.
 *
 * @return numCars - number of cars in caravan
 */
int queryNumCars() {
	int numCars;
	cout << "Enter the number of cars in the caravan: ";
	while(1) {
		cin >> numCars;
		if(!cin.fail()){
			break;
		}
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "must be an integer, try again\n";
	}
	return numCars;
}

/*
 * Displays the results of caravan problem to standard output.
 *
 * @param c - struct holding Caravan values
 * @param delays - pointer to int array of delays
 * @param distances - pointer to int array of distances
 * @param totalTime - int total delay time in seconds
 */
void dispData(Caravan c, int totalTime, int *delays, int *distances) {
	cout << "\nENTERED DATA\n";
	cout << "Number of tolls:\t" << c.numTolls << '\n';
	cout << "Car travel speed:\t" << c.speedLimit << " kph\n";
	cout << "Caravan size:\t\t" << c.numCars << " cars\n";
	for (int i = 0; i < c.numTolls; i++) {
		cout << "Toll " << i+1 << " delay:\t\t" << delays[i] << " seconds\n";
	}
	for (int i = 0; i < c.numLinks; i++) {
		cout << "Toll " << i+1 << " to " << i+2 << " distance:\t";
		cout << distances[i] << " km\n";
	}
	cout << "\nTOTAL TIME\n";
	if (totalTime < SECINMIN) {
		cout << totalTime << " seconds\n";
	} else if (totalTime % SECINMIN == 0) {
		cout << totalTime / SECINMIN <<" minutes\n";
	} else {
		int seconds = totalTime % SECINMIN;
		int minutes = int(totalTime / SECINMIN);
		cout << minutes << " minutes and " << seconds << " seconds\n";
	}

}
