# itertools module used for skipping the header line when initially reading file to dict
from itertools import islice

# csv module used for writing final array to the output .txt file
from collections import Counter
import csv
# sys module enables reading arguments used in Python function
import sys

from collections import defaultdict


def process_h1b_statistics(input_data_txt, output_occupations_txt,
                           output_states_txt):






    # Instantiate a CSV reader, check if you have the appropriate delimiter
    reader = csv.reader(open(input_data_txt))

    # Get the first row (assuming this row contains the header)
    input_header = next(reader)
    #print(input_header)
    # Filter out the columns that you want to keep by storing the column
    # index

    state_pattern = "(.*)WORK(.*)1_STATE"

    import re
    occup_header_indices = []
    state_header_indices = []
    for i, top_line in enumerate(input_header):
        if 'STATUS' in top_line or 'SOC_NAME' in top_line:
            occup_header_indices.append(i)
        if 'STATUS' in top_line or re.match(state_pattern, top_line):
            state_header_indices.append(i)


    # Create a CSV writer to store the columns you want to keep
    writer = csv.writer(open(output_occupations_txt, 'w'), delimiter=',')

    # Construct the header of the output file
    occup_header_names = []
    state_header_names = []
    for column_index in occup_header_indices:
        occup_header_names.append(input_header[column_index])
    for column_index in state_header_indices:
        state_header_names.append(input_header[column_index])

    #print(occup_header_names, state_header_names)


    with open(input_data_txt, "r") as infile:
        header = infile.read().split(';')
        header = [word.lower() for word in header]
        header[0] = 'index'
        #print(header)

    header = [item.strip("'") for item in header]


        # print(header)
        # wanted_cols = [header.index(label) for label in occup_header_names if
        #                label in header]
        #
        #
        #
        # # wanted_cols is now a list of column numbers you want
        #
        # for line in infile.readlines():  # Iterate through remaining file
        #     fields = line.split(';')
        #     data = [fields[col] for col in wanted_cols]


    #print(header)

    #
    # # Write the header to the output file
    # writer.writerow(output_header)
    #
    # # Iterate of the remainder of the input file, construct a row
    # # with columns you want to keep and write this row to the output file
    # for row in reader:
    #     new_row = []
    #     for column_index in columns_to_keep:
    #         new_row.append(row[column_index])
    #     writer.writerow(new_row)


    # The input file is eventually read in to these two dictionaries.
    occup_dict = {}
    states_dict = {}
    # The counter value counts all rows and represents the denominator in
    # calculating the PERCENTAGE column
    counter = 0
    with open(input_data_txt, "r") as file:
        # This enables skipping the header line.
        skipped = islice(file, 1, None)
        for i, line in enumerate(skipped, 2):
            counter += 1
            # A ValueError occurs when splitting and writing each line and
            # from the input file to variables for each of the columns that
            # appear in the input file
            try:
                header = line.split(";")
            except:
                pass


            # These if/else blocks read the data into two dictionaries,
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

            case_status = header[3].strip('/"')

            # This if clause specifies that a case should only be counted if
            #  the case has a 'CERTIFIED' status.
            if case_status == 'CERTIFIED':

                # Note, as with all Python dictionaries, if the key does not
                #  yet appear in the dictionary, the line below creates that
                #  new key with a starting value of 1.
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

process_h1b_statistics('../input/h1b_input.csv',
                       '../output/top_10_occupations.txt', 'top_10_states.txt') # h1b_fy_2014_abridged