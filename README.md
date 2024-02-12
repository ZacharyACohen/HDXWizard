# HDXWizard

HDXWizard is a free, open source software for processing and displaying hydrogen/deuterium exchange mass spectrometry (HDX MS) data. HDXWizard takes DynamX state or cluster data as a .csv or .xlsx file and generates chiclet plots and color peptide plots, as well as uptake plots and localized difference plots. Localized difference plots can be screened for correctness and exported to PyMOL.
HDXWizard allows for both direct calculation of relative fractional uptake (RFU) from theoretical maximal deuterium uptake as well as with using a maximally deuterated control (maxD).

HDXWizard is written completely in python (3.11.3) and uses Tkinter (8.6) for graphical user interface, Numpy (1.24.3) for calculations, MatPlotLib (3.7.2) for plot generation, PyMuPDF (1.23.7) for image processing, Biopython (1.8.2) for pairwise alignment, Tensorflow (2.14.0) for machine learning, and Openpyxl (3.1.2), Pandas (2.0.1), and Xlwings(0.30.12) for reading, writing, and representing excel sheets.

HDXWizard was developed at Northeastern University by Zachary Cohen and Thomas Wales


WARNING: Tensorflow is not currently compatible with python 3.12. If this is an issue, use python 3.11.
