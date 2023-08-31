# HDXWizard

HDXWizard is a free, open source software for processing and displaying hydrogen-deuterium exchange (HDX) data. HDXWizard takes DynamX state data as a .csv or .xlsx file and generates chiclet plots and color peptide plots representing exchange data and differences between states.
HDXWizard allows for both direct calculation of relative fractional uptake (RFU) from theoretical maximal deuterium uptake as well as an RFU corrected for maximally deuterated control (maxD) measurements.

HDXWizard is written completely in python and uses Tkinter (8.6) for graphical user interface, Numpy (1.24.3) for calculations, MatPlotLib (3.7.2) for figure legend generation, Openpyxl (3.1.2) for reading and writing excel sheets, and Requests (2.31.0) for checking GitHub for program updates.

HDXWizard was developed at Northeastern University by Zachary Cohen and Thomas Wales
