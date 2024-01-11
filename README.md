# HDXWizard

HDXWizard is a free, open source software for processing and displaying hydrogen-deuterium exchange (HDX) data. HDXWizard takes DynamX state data as a .csv or .xlsx file and generates chiclet plots and color peptide plots representing exchange data and differences between states. Uptake plots and linear maps, along wiht pymol model coloring can also be done.
HDXWizard allows for both direct calculation of relative fractional uptake (RFU) from theoretical maximal deuterium uptake as well as an RFU corrected for maximally deuterated control (maxD) measurements.

HDXWizard is written completely in python and uses Tkinter (8.6) for graphical user interface, Numpy (1.24.3) for calculations, MatPlotLib (3.7.2) for figure legend generation, fitz (PyMuPDF, 1.23.7) for image processing, Biopython (1.8.2) for pairwise alignment with .pdb files, Tensorflow (2.14.0) for machine learning, and Openpyxl (3.1.2), Pandas (2.0.1), and Xlwings(0.30.12) for reading, writing, and representing excel sheets.

HDXWizard was developed at Northeastern University by Zachary Cohen and Thomas Wales
