### Import necessary library modules
import argparse
import pandas as pd
import os
import numpy as np
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
        print("Each technical replicate for a mating has exactly two corresponding rows. Great!")
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
    # Calculate the associated standard deviation too (can be done in the same step)
    conj_tech = conj_eff.groupby(['Date', 'Control', 'Strain', 'Environment', 'Biological_Replicate'])['Ratio'].agg(['mean', 'std']).reset_index()
    
    ### Save this output
    tech_conj_path = os.path.join(output_dir, 'technical_replicates_conj_efficiency.csv')
    conj_tech.to_csv(tech_conj_path, index = False)


    # BIOLOGICAL REPLICATES VARIATION
    # Calculate averages for each combination of Date-Strain-Environment
    # Also calculate associated SD - both propagating error and without doing so
    # Not sure yet which I want to keep, so both for now

    # Write a separate function to calculate this
    def bio_stats(condition):
        weights = 1 / (condition['std'] ** 2)
        weighted_mean = np.average(condition['mean'], weights = weights)
        weighted_std = np.sqrt(1 / np.sum(weights))
        unweighted_mean = condition['mean'].mean()
        unweighted_std = condition['mean'].std()
        return pd.Series({
            'Weighted_Mean' : weighted_mean, 
            'Weighted_Std' : weighted_std,
            'Mean' : unweighted_mean,
            'Std' : unweighted_std
            })

    # Apply this function to each identifier
    conj_bio = conj_tech.groupby(['Date', 'Control', 'Strain', 'Environment']).apply(bio_stats).reset_index()

    ### Save this output
    conj_bio_path = os.path.join(output_dir, 'biological_replicates_conj_efficiency.csv')
    conj_bio.to_csv(conj_bio_path, index = False)


    # NORMALIZE TO CONTROLS
    # Per date, if control = yes, divide all values with the same Date-Strain-Environment
    # By this value (incl. itself)
    # Also normalize SD - divide by mean control condition

    # I will do this using a dictionary (wooo first time)
    # Filter 'Control = yes' rows
    control = conj_bio[conj_bio['Control'] == 'yes']
    # Mapping each 'Date' to the corresponding 'mean', when 'Control' is 'yes'
    control_dict = dict(control.groupby('Date')['Mean'].first())

    # Create a function to divide each mean & std by the control mean from my dictionary
    def normalize_mean(row):
        date = row['Date']
        control_mean = control_dict.get(date)
        if control_mean is not None:
            norm_mean = row['Mean'] / control_mean
            norm_std = row['Std'] / control_mean
            return pd.Series({'Normalized_Mean' : norm_mean, 'Normalized_Std' : norm_std})
        else: 
            raise ValueError(f'There is no control found for day {date}')
    
    # Apply the function
    norm_data = conj_bio.apply(normalize_mean, axis = 1)

    # Add additional columns to data
    conj_bio = pd.concat([conj_bio, norm_data], axis = 1)

    ### To propagate error: look into how to do this!!!

    ### Save this output
    norm_conj_path = os.path.join(output_dir, 'normalized_conj_efficiency.csv')
    conj_bio.to_csv(norm_conj_path, index = False)


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