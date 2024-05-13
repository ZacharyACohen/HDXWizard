## How can I install HDXWizard?
Instructions for installation of HDXWizard are available in the "README.md".
## What version of Python do I need to run HDXWizard?
Any version of Python 3.11 will work.
## Can I install HDXWizard on a Windows 7 computer?
No, HDXWizard requires python 3.11 to run, which is not available on Windows 7 devices.
## Can I install HDXWizard on Mac Devices?
A
## Is HDXWizard free?
Yes, HDXWizard is free and open source.
## What input data do I need?
The program takes DynamX state or cluster data files as input, either as .xlsx or .csv files. Sequences can also be added, but are not necessary for any outputs.
## The application does not fit on my computer screen?
While HDXWizard does not fit perfectly on devices with screens <15 inches, the program still works without issue.
## When I correct for a maximally deuterated control (maxD), what values are corrected?
All values will be corrected (aside from uptake plots unless specifically enabled). For chiclet plots as well as peptide and condensed peptide plots, values are displayed in relative fractional uptake (RFU). These values are calculated by dividing uptake values for a peptide by the uptake of its maximally deuterated control peptide. Differences here can take two forms: 1) Difference in RFU, which is calculated by subtracting the RFU of one state from another, and 2) Difference in daltons. These will be corrected with the equation corrected_uptake (uptake/maxD_uptake) * N, where N is the length of the peptide - #prolines - 1, unless proline is the first residue, before subtracting two states to find the difference in uptake in Daltons.
## When I correct for a set amount of back exchange, what values are corrected?
All values will be corrected (aside from uptake plots unless specifically enabled). For chiclet plots as well as peptide and condensed peptide plots, values are displayed in relative fractional uptake (RFU). These values are calculated by dividing the uptake for a peptide by (N * ((100-correction)/100), where N is the length of the peptide - #prolines - 1, unless proline is the first residue. Differences will be expressed as difference in Daltons by dividing corrected RFU by N before taking the difference of two states.
## How can I change the cutoffs between colors?
In the "formatting options" frame, the button "create custom colors" will allow for fully customizable color schemes.
## How are localized difference plots generated?
Localized difference plots are generated 
## Is localized difference plot output perfect?
## Is there a default value of significance that the neural network was trained on?
## 
