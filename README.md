#### Thomas Ernste - 10/31/2018

## Insight Data Engineering Coding Project:

# Processing H1B Statistics from the US Department of Labor's Office of Foreign Labor Certification

# Introduction/Approach

This repository contains a project that processes performance data from the Office of Foreign Labor Certification  (OFLC), which processes immigration applications. The source code, written in Python 3, reads an input .txt file, processes and transforms the data in the file, and generates two output .txt files: one containing statistics for the top occupations among certified H1B applications and a second containing statistics for the top states where certified H1B applicants are working.

# The Problem

The OFLC provides large files each year containing data about the status of various types of immigration applications in the United States. Because each line contains dozens of attributes about the applicant and potentially hundreds of thousands of applications are processed in a given quarter or year, the data files are both very large and also not useful by themselves for analysis. Further, although many of the columns in the data have limited value, a small number of the columns are very useful for analyzing and better understanding statistics regarding immigration in the United States. These files are much too large to be efficiently processed using standard software such as Microsoft Excel. These issues mean that data engineering and data science can be useful for processing these files, selecting relevant features for analysis, and presenting the data in ways that are illuminating of immigration trends.

# Input Dataset

The original input dataset (h1b_input.txt, in the input directory) came from the OFLC Performance Data. It includes over 50 data fields for a sample of H1B immigration applications in the United States. The pertinent columns in the data include the case status of the applicant (whether or not their application was certified), the applicant's occupational category (their Standard Occupational Classification), and the state where they are working.

# Libraries used

The Python libraries used in the source code include:

- **islice** - (imported from itertools, this library enables skipping the header line in the process of reading in the input file and writing the data to a dict)

- **csv** - (needed for writing final array to .txt file)

- **sys** - (enables reading the function arguments)

- **re** - (enables use of regular expressions)


# Output Datasets

Each line of the first 'occupations' output file contains the following fields in a in a semicolon separated format with semicolons the delimiters:

- **TOP_OCCUPATIONS**: the 'Standard Occupational Classification (SOC) code' of the application.
- **NUMBER_CERTIFIED_APPLICATIONS**: the number of certified applicants with the SOC code from the first column.
- **PERCENTAGE**: the percentage of applicants with the specified SOC code among all applications in the original sample.


This 'occupational' data file is sorted, first, in reverse order by the number of certified applications for each occupational category, and secondly alphabetically by occupational category if the occupational categories have the same number of certified applications.


Each line of the second 'states' output file contains the following fields in a semicolon separated format with semicolons the delimiters:

- **TOP_STATES**: the US state where the applicant is working.
- **NUMBER_CERTIFIED_APPLICATIONS**: the number of certified applicants working in the state from the first column.
- **PERCENTAGE**: the percentage of applicants working in the specified US state among all applications in the original sample.


This 'states' data file is sorted, first, in reverse order by the number of certified applicants working in each state, and secondly alphabetically by state name if the state names have the same number of certified applications.

# Code

The code is documented in detail and has been tested for scalability to work on both small and large datasets of varying file structure that appear on the website for the OFLC, found [here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis).

**Note: This respository was successfully tested to process a large 245 MB file from the Office of Foreign Labor Certification Performance Data website. However, Github does not allow updloading of excessively large files. My input test file in the my_h1b_test/input directory is an an abridged version of an OFLC H1B file with a size of approximately 57 MB.

# Running the data

This code can be run from the Command Line or Terminal on any machine with Python 3 using only basic built-in modules. To run the code, the user should fork and clone the repository to their machine. Then, they should enter the h1b_statistics_data_engineering/insight_testsuite/ directory. And finally, within this directory, the user should type the command ./run_tests.sh to run this project. This will test the code using the input files in two tests: test_1, which contains a small input.csv sample data file for testing, and my_h1b_test, which contains a much larger input.csv sample data file for a second test.
