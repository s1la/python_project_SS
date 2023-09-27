### Import necessary library modules
# import argparse
# import pandas as pd
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns

# Creating a function to load in the csv file


# Creating a function to process our data

    
    # RAW COUNTS

    # Calculate full colony count, add extra column to dataset
    # Colony_count * 10^Dilution, for each row -> Raw_count

    # CONJUGATION EFFICIENCY 

    # Divide Donors by Transconjugants
    # Look through "D" data first
    # Each Date, Strain, Environment, Biological_repl, Technical_repl 
    # should be unique. If it is not, spit out an error message
    # "identifier -name- is not unique in D"

    # For each of these unique identifiers, find the corresponding row for T
    # If no match is found, spit out an error
    # "identifier -name- does not exist in T"
    # If this does not lead to a unique row, spit out an error
    # "identifier -name- is not unique in T"
    # If the identifiers are unique, divide Raw_count 

    # This should give two results, one of which is Plate = D, one of which is Plate = T
    # If this is not the case, spit out an error message 
    # Divide these two values by eachother: T/D -> Conj_eff

    # TECHNICAL REPLICATES VARIATION
    # Calculate the average of Conj_Eff for each combination of Date-Strain-Environment-Biological_Replicate combination
    # Calculate the associated standard deviation too. 
    # Save relevant columns

    # BIOLOGICAL REPLICATES VARIATION
    # Calculate averages for each combination of Date-Strain-Environment
    # Also calculate associated SD - propagating error
    # Save relevant columns

    # NORMALIZE TO CONTROLS
    # Per date, if control = yes, divide all values with the same Date-Strain-Environment
    # By this value (incl. itself)
    # Also normalize SD
    # Add as an additional column 

# Create a function to generate our plots
# def generate_plots(data, output_dir):
    # PLOTTING PER DAY
    # One figure per date
    # Per day, plot norm avg per condition/strain + corresponding SD 
    # Save all day plots together in one .pdf, named according to input file name

    # PLOTTING ACCROSS DAYS
    # Per condition, plot norm avg + corresponding control, and their pooled SD
    # Again, save in one .pdf


# Creating main function - argparse
# Create an argument parser

# parser = argparse.ArgumentParser(description = "Process Colony count data and generate plots.")

# Add command-line arguments

# parser.add_argument("input_csv", help = "Input CSV file name. Should include Date, Control, Strain, Environment, Biological_ and Technical_Replicate, Colony_Count, Dilution and Plate columns")

# parser.add_argument("--output_dir", default="plots", help="Specify name for output directory. Input file name + '_processed' by default")

# Parse command-line arguments

# args = parser.parse_args()

# Determine output directory

#if args.output_dir is None:
    # Use input file name (without extension) as the default
    # input_file_name = os.path.splitext(os.path.basename(args.input_file))[0]
    # args.output_dir = input_file_name + "_processed"

# Create the output directory if it doesn't exist
# os.makedirs(args.output_dir, exist_ok=True)

# Load data
# input_data = load_data(args.input_file)

# Process data


# Generate plots