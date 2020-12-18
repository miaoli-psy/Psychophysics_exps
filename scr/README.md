# Exp1_rerun_directEstimation_analysis
* 5 numerosity ranges (21-25; 31-35; 41-45; 49-53; 54-58) 
* Crowding vs. No-crowding (other physical properties of the displays were matched between 2 conditions)
* Direct estimation 10 blocks, each block 50 trials 
* 5 References: median, median ± 12.5%, median ± 25% 

### Exp1_rerun_dataAnalysis.py: Behavioral data analysis  

### 'scaterplot.py':


### local_density.py:  
    input:
    1. '../fullStimuliInfo.xlsx':  
    2. '../cleanedTotalData_fullinfo.xlsx'  
    output:
    1. updated_stim_info_df : include increasing ellipse sizes count_number(s) and local density information for each stimulus display.
    2. totalData_new

### upper_lower_viewFields.py
    input:
    1. '../update_stim_info.xlsx' (output from local_density)
    output:  
    totalData_new_vdf

### NDiscsCrowdingZones.py
    input:
    1. '../totalData_new.xlsx' (a cleaned data file)
    output:
    a regplot: deviation score against number of discs into others crowding zones
    Note: here we averaged per display, therefore the CI could be caused by within numerosity(display) variances of psychical properties

    (if we average per participant, the CI should be caused by individual difference)
