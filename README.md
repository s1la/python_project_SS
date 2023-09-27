# python_project_SS

This repository contains a final project for the course 'Python for Biologists'.

The goal of this project is to create an easier workflow to analyze manual mating assay results. 


## Colony counting

### Input

When spotting onto the selective plates, do so according to the pattern provided on [layout_reference].

After performing a liquid mating assay, plates should be scanned using a ChemiDoc imaging system/ordinary tabletop scanner (decide!), and saved as a [filetype].

When naming the image files, do so according to the following pattern: **date_control:strain-environment_sample:strain-environment_D-or-T**, with D indicating Donor selecting plates and T indicating Transconjugant selecting plates.

### Script

[Information about how to use the script, and what it does.]

### Output

This script will output a .csv file containing eight columns, showing date, condition (strain, environment, sample, replicate), colony count, dilution at which this colony count was obtained, and D or T. 
  
## Data processing

### Input

This script can use the output from the Colony Counting script, or similarly structured data (see [example_data.csv]).

### Script

This script can be run from the terminal by writing the following: python colony_processing.py [arguments].

The average of your technological and biological repicates, with the associated standard deviations, is calculated.

Sample data is normalized to corresponding controls per date. Averages per condition with standard deviations are plotted, with a separate figure per date. This is saved as [output_plot_1_name.pdf]

For multi-day runs with the same sample conditions, plots are also generated with the data of multiple days. Both averages per condition with pooled variance, and boxplots are generated, with one figure per condition. This is saved as [output_plot_2_name.pdf]

Finally, summary datafiles are generated, saved as [data_filenames.csv]
