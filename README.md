# python_project_SS

This repository contains a final project for the course 'Python for Biologists'.

The goal of this project is to create an easier workflow to analyze manual mating assay results. 


## Colony_processing

### Input

This script accepts colony counting data in .csv format, including at least the columns 'Date', 'Control', 'Strain', 'Environment', 'Biological_Replicate', 'Technical_Replicate', 'Colony_Count', 'Dilution' and 'Plate' (as shown in [example_data.csv]).

### Running the script

This script can be run from the terminal by writing the following: python colony_processing.py [input.csv]. 

The optional argument --output.dir can be added to change the name of the output directory. By default, this is the name of the input .csv file, followed by '_processed'.

### Output

Absolute conjugation efficiency is calculated first, saved as '01_Absolute_Efficiency'.

This is then averaged accross technical replicates, and the standard deviation is calculated, saved as '02_Technical_Replicates_Efficiency'.

The average and standard deviation accross all replicates is then calculated, and normalized to the controls. 

Per date, this is saved as '03_Normalized_Efficiency'. 

Accross dates, this is saved as '04_Normalized_Efficiency_All_Dates'.

Finally, results per date and accross all dates are plotted, saved in '05_Conjugation_per_day' and '06_Full_Conjugation'.

