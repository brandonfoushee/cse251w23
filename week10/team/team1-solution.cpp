#include <iostream>
#include <cstdlib>
#include <pthread.h>

#ifdef _WIN32
#include <io.h>
#else
#include <unistd.h>
#endif

#include <time.h>

using namespace std;

#define NUMBERS  1000
#define NUM_THREADS 5

struct args {
	int *array;
	int start;
	int end;
};

// ----------------------------------------------------------------------------
int isPrime(int number) {
	if (number <= 3 && number > 1)
		return 1;            // as 2 and 3 are prime
	else if (number % 2 == 0 || number % 3 == 0)
		return 0;     // check if number is divisible by 2 or 3
	else {
		for (int i = 5; i * i <= number; i += 6) {
			if (number % i == 0 || number % (i + 2) == 0)
				return 0;
		}
		return 1;
	}
}

// ----------------------------------------------------------------------------
void* findPrimes1(void* record) {
	//cout << "\nStarting findPrimes\n";

	// Get the structure used to pass arguments
	struct args *arguments = (struct args*) record;

	// Loop through the array looking for prime numbers
	for (int i = arguments->start; i < arguments->end; i++) {
		//cout << "i=" << i << ", start=" << arguments->start << ", end=" << arguments->end << "\n";
		if (isPrime(arguments->array[i]) == 1) {
			cout << "found prime = " << arguments->array[i] << "\n";
		}
	}

	return NULL;
}

int main() {

	srand(time(0));

	// Create the array of numbers and assign random values to them
	int arrayValues[NUMBERS];
	for (int i = 0; i < NUMBERS; i++) {
		arrayValues[i] = rand() % 1000000000;
		cout << arrayValues[i] << ", ";
	}

	cout << endl;

	// Create structure that will be used to pass the array and the
	// start of end of the array to another function
	struct args records[NUMBERS];
	int start = 0;
	int end = 0;
	int range = NUMBERS / NUM_THREADS;

	for (int i = 0; i < NUM_THREADS; i++) {
		start = range * i;
		end = start + range - 1;
		cout << "start=" << start << ", end=" << end << ", range=" << range
				<< endl;
		records[i].array = arrayValues;
		records[i].start = start;
		records[i].end = end;
	}

	cout << "done setting up records" << endl;

	// Find the primes in the array
	//findPrimes(&rec);

	pthread_t threads[NUM_THREADS];

	cout << "creating " << NUM_THREADS << " threads" << endl;

	for (int i = 0; i < NUM_THREADS; i++) {
		args rec = records[i];
		int rc = pthread_create(&threads[i], NULL, findPrimes1, &rec);

		if (rc) {
			cout << "Error:unable to create thread," << rc << endl;
			exit(-1);
		}
	}

	cout << "done creating threads" << endl;

	for (int i = 0; i < NUM_THREADS; i++) {
		pthread_join(threads[i], NULL);
	}

	pthread_exit(NULL);

}
