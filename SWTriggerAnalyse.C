// Program that loads in a ttree and then calculates the ratio number of entries after a cut and the number of entries in the ttree

#include "TFile.h"
#include "TH1F.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TEfficiency.h"

#include <iostream>
#include <fstream>

ofstream myfile;


// Calulates the fraction of events passed SW trigger and their errors
void SWTriggerAnalyse_Function(TString infile) {
	// Open the file
	TFile *fileIN = TFile::Open(infile);
	if (fileIN == 0) {
	  // if we cannot open the file, print an error message and return immediatly
	  printf("Error: cannot open swtrigger_hist.root!\n");
	  return;
	}

	// Create the tree reader and its data containers
	TTreeReader myReader("swtrigger/swtrigdata", fileIN);

	TTreeReaderValue<std::vector<int>> algopassRV(myReader, "algopass"); 					// Load in the algopass variable
	TTreeReaderValue<std::vector<unsigned short>> PHMAXRV(myReader, "PHMAX"); 				// Load in the PHMAX variable
	TTreeReaderValue<std::vector<unsigned short>> multiplicityRV(myReader, "multiplicity"); // Load in the PHMAX variable

	double Total_events = 0;
	double Passed_Events = 0;

	// Loop over all entries of the TTree or TChain.
	while (myReader.Next()) {
		if ( (*multiplicityRV)[0] >= 1  ) Total_events++; 	// Count total events under multiplicty >= 1 condition

		if ( (*algopassRV)[0] == 1 &&  (*multiplicityRV)[0] >= 1  ) Passed_Events++; // Count total events under multiplicty >= 1 and passes swtrigger condition

	}

	// Calculate the errors on the values
	TEfficiency *k = new TEfficiency();
	k->SetStatisticOption(TEfficiency::kFFC);

	// get +/- 1 sigma interval from Feldman Cousins statistics
	double eff = Passed_Events/Total_events;
	double eff_upper = k->FeldmanCousins(Total_events,Passed_Events,0.6827,true);
	double eff_lower = k->FeldmanCousins(Total_events,Passed_Events,0.6827,false);

	// Print results
	std::cout << "\nFraction of events passed [Multiplicity >= 1]: " << eff << std::endl;
	std::cout << "1-sigma interval: " << "[ "<< eff_lower << ", "<< eff_upper << " ]\n" << std::endl;

	// Write the data to a file in csv format
	myfile << eff << "," << eff_upper << "," << eff_lower << "\n";

}

// Function to call the analyse function and loop over file names
void SWTriggerAnalyse(){
	
	// Open the file and add header line
	myfile.open("SWTrigger_Analyze_Output.txt");
	myfile << "Eff,Eff_upper,Eff_lower\n";
	
	// Vector of file names
	std::vector<TString> infiles;

	// Create list of files here.
	infiles.push_back("swtrigger_hist.root");

	for (int k = 0; k<infiles.size(); k++) SWTriggerAnalyse_Function(infiles[k]);

	myfile.close();

}



