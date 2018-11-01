# itertools module used for skipping the header line when initially reading file to dict
from itertools import islice

# csv module used for writing final array to the output .txt file
import csv

# sys module enables reading arguments used in Python function
import sys

# re module enables the use of regular expressions
import re


def process_h1b_statistics(input_data_txt, output_occupations_txt,
                           output_states_txt):
    # The input file is eventually read in to these two dictionaries.
    occup_dict = {}
    states_dict = {}
    # The counter value counts all rows and represents the denominator in
    # calculating the PERCENTAGE column
    counter = 0

    # Although the input files have differing file structures, the columns
    # of interest (occupational category and state of the applicant's work
    # site) across the files have similar names. These regular expression
    # patterns are used in my code below to identify the index location of
    # my columns of interest regardless of the index location of the given
    # columns.
    occup_pattern = "(.*)SOC_NAME"
    state_pattern = "(.*)WORK(.*)_STATE"


    # These lists are used to store the index locations of the case
    # status location column plus the occupational category and worksite
    # state of the applicant.
    occup_header_indices = []
    state_header_indices = []


    # This instantiates a csv reader
    reader = csv.reader(open(input_data_txt), delimiter=';')


    # Gets and stores only the first row, allowing for the identification of
    # the column index for my columns of interest within any given file
    # structure.
    input_header = next(reader)
    for i, top_line in enumerate(input_header):
        if 'STATUS' in top_line or re.match(occup_pattern, top_line):
            occup_header_indices.append(i)
        if 'STATUS' in top_line or re.match(state_pattern, top_line):
            state_header_indices.append(i)

    # Because many of the input files contained a semicolon within the
    # column strings, these semicolons within columns can create problems for
    # sorting a semicolon-separated file. This block of code removes all of
    # the semicolons from within any column string in any file.
    interim_string = ' '
    with open(input_data_txt, 'r', newline='') as infile, \
            open(interim_string, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=';')
        for row in csv.reader(infile, delimiter=';'):
            for e, col in enumerate(row):
                if ';' in col:
                    row[e] = row[e].replace(';', '')
            writer.writerow(row)


    with open(interim_string, "r") as file:
        # This enables skipping the header line.
        skipped = islice(file, 1, None)

        for i, line in enumerate(skipped, 2):
            counter += 1

            # This code writes the string data to list that will be used to
            # write the data to dictionaries below.

            my_data = line.split(";")

            # These if/else blocks below read the data into two dictionaries,
            # one for the Top 10 occupations data and one from the Top 10
            # states data. The Standard Occupational Code (SOC) name (
            # soc_name) is the key in the occupations dictionary and the
            # worksite state name (worksite_state) is the key in the states
            # dictionary. In both cases, the value in these dictionaries is
            # a count of those lines that hold data for a person with a
            # CERTIFIED H1B visa case_status.


            # Because some of the soc_name input data had quotation marks in
            # on them in the input file, this line strips those quotes from
            # the data to standardize all of the soc_name values for my
            # output data.

            case_status = my_data[occup_header_indices[0]]
            soc_name = my_data[occup_header_indices[1]].strip('"')


            worksite_state = my_data[state_header_indices[1]]

            # This if clause specifies that a case should only be counted if
            #  the case has a 'CERTIFIED' status.
            if case_status == 'CERTIFIED':

                # Note, as with all Python dictionaries, if the key does not
                # yet appear in the dictionary, the line below creates that
                # new key with a starting value of 1.

                # The 'else' part of this if/else block for the occupations
                # dictionary adds to the existing value for each key that
                # already appears in the dictionary.

                if soc_name not in occup_dict:
                    occup_dict[soc_name] = 1

                else:
                    occup_dict[soc_name] += 1

                # This block emulates the above creation of a dictionary,
                # but this time for the states data.
                if worksite_state not in states_dict:
                    states_dict[worksite_state] = 1

                else:
                    states_dict[worksite_state] += 1

            else:
                pass


    # This line sorts the dictionaries data into lists, sorting first in
    # descending ("reverse") order by the number of 'CERTIFIED' cases for
    # each occupation or state, then in descending order by the alphabetical
    #  name of the drug soc_name or state.

    final_sorted_list_occup = sorted(occup_dict.items(), key=lambda kv: (
        -kv[1], kv[0]))


    final_sorted_list_states = sorted(states_dict.items(), key=lambda kv: (-kv[
        1], kv[0]))


    # These list comprehensions append the data from each dictionary to the
    # correct columns, including the calculation of the percentage value
    # with one rounded decimal point for each certified case in the data.

    final_array_occup = [[row[0], row[1], '{:.1%}'.format(row[1]/counter)]
                         for row in final_sorted_list_occup]

    final_array_states = [[row[0], row[1], '{:.1%}'.format(row[1]/counter)]
                          for row in final_sorted_list_states]



    # These lines insert a header row at position 0 (the top row) in the final
    # arrays.
    final_array_occup.insert(0, ['TOP_OCCUPATIONS',
                             'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])

    final_array_states.insert(0, ['TOP_STATES',
                             'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])


    # This block writes the transformed occupations and states data to each of
    #  the two output files.

    with open(output_occupations_txt, 'w') as myfile_occup:
        wr = csv.writer(myfile_occup, delimiter=';')
        for i in final_array_occup:
            wr.writerow(i)

    with open(output_states_txt, 'w') as myfile_states:
        wr = csv.writer(myfile_states, delimiter=';')
        for i in final_array_states:
            wr.writerow(i)

# This block allows execution of the process_h1b_statistics function from the
# run.sh shell script, with the appropriate input and output files included
# in the run.sh shell script and run_tests.sh test script.

def main():
    input_data_txt = sys.argv[1]
    output_occupations_txt = sys.argv[2]
    output_states_txt = sys.argv[3]
    process_h1b_statistics(input_data_txt, output_occupations_txt,
                           output_states_txt)

if __name__ == '__main__':
    main()