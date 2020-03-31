## Experiment 1: Indirect manipulation of the crowding and the no-crowding displays (re-structured)

### *Introduction*  
This is the first conducted experiment to explore the role of crowding in numerosity estimation. In this experiment, we create displays that differ in terms of crowding levels while keeping other display properties(eg. convex hull) as similar as possible. For each disc in the display, there is a corresponding crowding (or no-crowding zone). For the no-crowding condition, radially placed ellipses (crowding zones) were filled in the displays, which protected that no disc falls into others crowding zone. For the crowding condition, tangentially placed ellipses were filled in the displays.

### *Manipulation*
* crowding level: crowding vs. no-crowding

* numerosity range: 5 levels (from small to large: 0.3 winsize - 0.7 winsize )

* numerosity: 
  * winsize 0.3: 21 - 25
  * winsize 0.4: 31 - 35
  * winsize 0.5: 41 - 45
  * winsize 0.6: 48 - 53
  * winsize 0.7: 54 - 58
### *Task*

direct estimation task

### *Folder structure*
* analysis
  * correctproperties
    *  calculateproperties.py: re-calculate displays' properties.
    *  cleanedTotalData_fullinfo.xlsx
    *  cleanedTotalData_fullinfo_v2.xlsx: output of calculateproperties.py
* displays
  * update_stim_info_full.xlsx: all used displays details
* rawdata
* results