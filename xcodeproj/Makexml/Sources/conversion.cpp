#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <stdlib.h>

using namespace std;

static ifstream inputFile;
static ofstream outputFile;

static const string inputFileName = "conversion.xml";
static const string outputFileName = "conversion.txt";

static const string tagTecajnica = "tecajnica datum";	// Defines new date
static const string tagTecaj = "USD";			// Defines USD rate

int main()
{
	string line, dateStr, currStr;

	// Open both files
	inputFile.open(inputFileName.c_str(), ifstream::in);
	outputFile.open(outputFileName.c_str(), ifstream::out);

	if (!inputFile.is_open())
	{
		cout << __FUNCTION__ << ":" << __LINE__ << ": "
				<< "Cannot open input file!" << endl;
		return 1;
	}
	else if (!outputFile.is_open())
	{
		cout << __FUNCTION__ << ":" << __LINE__ << ": "
				<< "Cannot open output file!" << endl;
		return 1;
	}

	// The main loop -
	// Read input file line by line
	while(getline(inputFile, line))
	{
		if (line.find(tagTecajnica) != std::string::npos)
		{
			// New date
			outputFile << line.substr(line.find("\"")+1, 10) << " ";
		}
		else if (line.find(tagTecaj) != std::string::npos)
		{
			// New rate
			outputFile << line.substr(line.find(">")+1, 6) << endl;
		}
	}

	// Close all files
	inputFile.close();
	outputFile.close();

	return 0;
}
