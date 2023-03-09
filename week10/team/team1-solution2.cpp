#include <pthread.h>
#include <sys/_pthreadtypes.h>
#include <cstdlib>
#include <iostream>
#include <thread>

#ifdef _WIN32
#include <io.h>
#else
#include <unistd.h>
#endif

#include <time.h>

using namespace std;

#define RANGE 100000
#define START 10000000000
#define NUM_THREADS 10
//static std::atomic<int> threadCounter(0);

struct args {
	long long start;
	long long end;
	int result;
};

// ----------------------------------------------------------------------------
int isPrime(long long number) {
	//cout << "number=" << number << "\n";
	if (number <= 3 && number > 1)
		return 1;            // as 2 and 3 are prime
	else if (number % 2 == 0 || number % 3 == 0)
		return 0;     // check if number is divisible by 2 or 3
	else {
		for (long long i = 5; i * i <= number; i += 6) {
			if (number % i == 0 || number % (i + 2) == 0)
				return 0;
		}
		return 1;
	}
}

// ----------------------------------------------------------------------------
void* findPrimes(void *record) {
	//cout << "\nStarting findPrimes\n";

	// Get the structure used to pass arguments
	struct args *arguments = (struct args*) record;

	int *total = (int*) malloc(sizeof(int));
	*total = 0;

	cout << "first number is " << arguments->start << ", last number is "
			<< arguments->end << endl;

	// Loop through the array looking for prime numbers
	for (long long i = arguments->start; i < arguments->end; i++) {
		//cout << "i=" << i << "\n";
		if (isPrime(i) == 1) {
			//cout << "found prime = " << arguments->array[i] << "\n";
			(*total)++;
			//threadCounter++;
		}
	}
	cout << "total=" << *total << endl;
	return total;
}

int main() {

	srand(time(0));

	// Create the array of numbers and assign random values to them
//	long *arrayValues = new long[RANGE];
//
//	int index = 0;
//	for (long i = START; i < START + RANGE; i++) {
//		arrayValues[index++] = i;
//	}

	// Create structure that will be used to pass the array and the
	// start of end of the array to another function
	struct args records[NUM_THREADS];
	int partitionSize = RANGE / NUM_THREADS;

	int index = 0;
	for (long long i = START; i < START + RANGE; i += partitionSize) {
		long long end = i + partitionSize - 1;
		cout << "start=" << i << ", end=" << end << ", part=" << partitionSize
				<< endl;
		records[index].start = i;
		records[index].end = end;
		index++;
	}

	cout << "done setting up records" << endl;

	pthread_t threads[NUM_THREADS];

	cout << "creating " << NUM_THREADS << " threads" << endl;

	for (int i = 0; i < NUM_THREADS; i++) {
		args rec = records[i];
		int rc = pthread_create(&threads[i], NULL, findPrimes, &rec);

		if (rc) {
			cout << "Error:unable to create thread," << rc << endl;
			exit(-1);
		}
	}

	cout << "done creating threads" << endl;

	int total = 0;

	for (int i = 0; i < NUM_THREADS; i++) {
		void *result;
		pthread_join(threads[i], &result);
		int t = *((int*) (result));
		total += t;
		cout << "total primes found in thread " << i << " was " << t << endl;
	}

	cout << "total primes found = " << total << endl;
	//cout << "total primes found = " << threadCounter << endl;

	pthread_exit(NULL);

	return 0;
}
