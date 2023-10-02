### Import necessary library modules
import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Creating a function to load in the csv file
def load_data(csv_file):
    raw_data = pd.read_csv(csv_file)
    return raw_data

# Creating a function to process our data
def process_and_plot(raw_data, output_dir):
    
    # RAW COUNTS

    # Calculate full colony count, add extra column to dataset
    # Colony_count / 10^Dilution, for each row -> Raw_count
    def calc_full_count(row):
        return row['Colony_Count'] / (10 ** row['Dilution'])
    # Apply function along rows, so axis = 1
    raw_data['Full_Count'] = raw_data.apply(calc_full_count, axis = 1)


    # CONJUGATION EFFICIENCY 

    # Divide Donors by Transconjugants

    # Create a new column 'unique_identifier'
    
    raw_data['Identifier'] = raw_data[['Date', 'Strain', 'Environment', 'Biological_Replicate', 'Technical_Replicate']].astype(str).agg('-'.join, axis=1)
    counts = raw_data.groupby(['Date', 'Strain', 'Environment', 'Biological_Replicate', 'Technical_Replicate']).size()
    unequal_counts = counts[counts != 2]

    # Each Date, Strain, Environment, Biological_repl, Technical_repl should only have two rows: one for D and one for T
    # If this is not true, spit out an error message showing for which identifiers this is not the case:

    if not unequal_counts.empty:
        print(f"Error: The following matings are lacking either D or T counts, or have too many:")
        print(unequal_counts)
    else:
        print("Each mating has exactly two corresponding rows. Great!")
        # If all is well, calculate the conjugation efficiency: Per unique ID, divide Full_Count(Plate = T)/ Full_Count(Plate=D)
        conj_eff = (
            raw_data.pivot(index= ['Date', 'Control', 'Strain', 'Environment', 'Biological_Replicate', 'Technical_Replicate'], columns = 'Plate', values = 'Full_Count')
                    .assign(Ratio= lambda x: x['T']/ x['D'])
                    .reset_index()
            )

    #### Save the absolute conjugation efficiency
    abs_conj_path = os.path.join(output_dir, 'absolute_conj_efficiency.csv')
    conj_eff.to_csv(abs_conj_path, index=False)


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

def main():

# Create an argument parser

    parser = argparse.ArgumentParser(description = "Process Colony count data and generate plots.")

# Add command-line arguments

    parser.add_argument("input_csv", help = "Input CSV file name. Should include Date, Control, Strain, Environment, Biological_ and Technical_Replicate, Colony_Count, Dilution and Plate columns")

    parser.add_argument("--output_dir", default="plots", help="Specify name for output directory. Input file name + '_processed' by default")

# Parse command-line arguments

    args = parser.parse_args()

# Determine output directory

    if args.output_dir is None:
        # Use input file name (without extension) as the default + 'processed' at the end
        input_file_name = os.path.splitext(os.path.basename(args.input_csv))[0]
        args.output_dir = input_file_name + "_processed"

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load data
    raw_data = load_data(args.input_csv)

    # Process data and generate plots
    process_and_plot(raw_data, args.output_dir)

if __name__ == "__main__":
    main()