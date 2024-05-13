## How can I install HDXWizard?
Instructions for installation of HDXWizard are available in the "README.md"
## What version of Python do I need to run HDXWizard?
Any version of Python 3.11 will work
## Can I install HDXWizard on a Windows 7 computer?
No, HDXWizard requires python 3.11 to run, which is not available on Windows 7 devices
## Can I install HDXWizard on Mac Devices?
A
## Is HDXWizard free?
Yes, HDXWizard is free and open source
## The application does not fit on my computer screen?
While HDXWizard does not fit perfectly on devices with screens <15 inches, the program still works without issue
## When I correct for a maximally deuterated control (maxD), what values are corrected?
All values will be corrected (aside from uptake plots unless specifically enabled). For chiclet plots as well as peptide and condensed peptide plots, values are displayed in relative fractional uptake (RFU). Here, these values will be calculated by dividing uptake values for a peptide by the uptake of its maximally deuterated control peptide. Differences here can take two forms: 1) Difference in RFU, which is calculated by subtracting the RFU of one state from another, and 2) Difference in daltons. These will be corrected with the equation corrected_uptake (uptake/maxD_uptake) * N, where N is the length of the peptide - #prolines - 1, unless proline is the first residue, before subtracting two states to find the difference in uptake in Daltons.
## When I correct for a set amount of back exchange, what values are corrected?
