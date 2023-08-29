import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import openpyxl
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side
from openpyxl.styles import Alignment

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import webbrowser
import requests

import os
import csv
import tempfile
import atexit
import json






print("Initializing Program")
print("Checking for Updates")


version_number = "23.8.28"

try:
    program_needs_update = False
    url = "https://raw.githubusercontent.com/ZacharyACohen/HDXWizard/main/Version%20Number"
    response = requests.get(url)
    if response.status_code == 200:
        remote_version = response.text.strip()
        newest_version = remote_version.split("!")[1]
        print(f"Newest Version: {newest_version}")
        print(f"Current Version: {version_number}")
        if newest_version == version_number:
            print("Program is updated")
        else:
            print("Please go to https://github.com/ZacharyACohen/HDXWizard.git to update program")
            program_needs_update = True
    else:
        print("Failed to Fetch Remote File")
except:
    print("Update Check Inconclusive. Could Not Connect to Web")
    
print("\n\n")


sdbt_xlsx_clicked = False
sdbt_csv_clicked = False
seqbt_txt_clicked = False
seqbt_fasta_clicked = False
skip_bt_clicked = False
txt_h_bt_clicked = False

data = []
seq = None



def open_sd_file_xlsx():
    global sdbt_xlsx_clicked, data, sdbt_csv_clicked, temp_file_path_excel
    sdbt_xlsx.config(state="disabled")
    sdbt_xlsx.config(relief="sunken", bg="white", fg="black")
    sd_file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if sd_file_path.endswith(".xlsx"):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active


        source_workbook = openpyxl.load_workbook(sd_file_path)
        source_worksheet = source_workbook.active
        for row in source_worksheet.iter_rows(values_only=True):
            worksheet.append(row)

        for row in worksheet.iter_rows():
            cella = row[12]
            if cella.value == "NaN" or cella.value == "":
                cella.value = -99999
            cellb = row[8]  # Assuming column I is the 9th column (index 8)
            if cellb.value:
                cellb.value = cellb.value.replace("~", "_")
                cellb.value = cellb.value.replace("|", "_")
                cellb.value = cellb.value.replace(" ", "_")
            celle = row[0]
            if celle.value:
                celle.value = celle.value.replace("~", "_")
                celle.value = celle.value.replace("|", "_")
                celle.value = celle.value.replace(" ", "_")
            cellc = row[4]
            celld = row[5]
            cellc.value = None
            celld.value = None
            cellf = row[13]
            if cellf.value == "NaN" or cellf.value == "":
                cellf.value = -99999


        temp_file_path_excel = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False).name
        workbook.save(temp_file_path_excel)
        atexit.register(os.remove, temp_file_path_excel)

        output_file_path = temp_file_path_excel.replace('.xlsx', '.txt')
        atexit.register(os.remove, output_file_path)
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            for row in worksheet.iter_rows():
                writer.writerow([cell.value for cell in row])



        if output_file_path:
            with open(output_file_path, "r") as f:
                lines2 = f.readlines()
                lines = lines2[1:]
            if len(data) == 0:
                data = [line.strip().split() for line in lines]
            else:
                new_data = [line.strip().split() for line in lines]
                for line in new_data:
                    data.append(line)

            sdbt_xlsx_2 = tk.Button(window, text=".xlsx", bg="green", fg="white",  width=5, command=open_sd_file_xlsx)
            sdbt_xlsx_2.place(x=170, y=30)
            sdbt_xlsx_clicked = True

            sdbt_csv = tk.Button(window, text=".csv",bg="orange",fg="black", width=5, command=open_sd_file_csv)
            sdbt_csv.place(x=120, y=30)
            sdbt_csv_clicked = False



            check_button_clicks()

prot_seq_dic = {}
def open_sd_file_csv():
    global sdbt_csv_clicked, data, sdbt_xlsx_clicked, temp_file_path_excel

    sd_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if sd_file_path.endswith(".csv"):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        with open(sd_file_path, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                worksheet.append(row)

        for row in worksheet.iter_rows():
            cella = row[12]
            if cella.value == "NaN" or cella.value == "":
                cella.value = -99999
            cellb = row[8]  # Assuming column I is the 9th column (index 8)
            if cellb.value:
                cellb.value = cellb.value.replace("~", "_")
                cellb.value = cellb.value.replace("|", "_")
                cellb.value = cellb.value.replace(" ", "_")
            celle = row[0]
            if celle.value:
                celle.value = celle.value.replace("~", "_")
                celle.value = celle.value.replace("|", "_")
                celle.value = celle.value.replace(" ", "_")
            cellc = row[4]
            celld = row[5]
            cellc.value = None
            celld.value = None
            cellf = row[13]
            if cellf.value == "NaN" or cellf.value == "":
                cellf.value = -99999

        temp_file_path_excel = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False).name
        workbook.save(temp_file_path_excel)
        atexit.register(os.remove, temp_file_path_excel)

        output_file_path = temp_file_path_excel.replace('.xlsx', '.txt')
        atexit.register(os.remove, output_file_path)
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            for row in worksheet.iter_rows():
                writer.writerow([cell.value for cell in row])



        if output_file_path:
            with open(output_file_path, "r") as f:
                lines2 = f.readlines()
                lines = lines2[1:]


            if len(data) == 0:
                data = [line.strip().split() for line in lines]
            else:
                new_data = [line.strip().split() for line in lines]
                for line in new_data:
                    data.append(line)




            sdbt_xlsx =tk.Button(window, text=".xlsx",bg="orange",fg="black", width=5, command=open_sd_file_xlsx)
            sdbt_xlsx.place(x=170,y=30)
            sdbt_xlsx_clicked = False


            sdbt_csv_2 = tk.Button(window, text=".csv", bg="green", fg="white",  width=5,  command=open_sd_file_csv)
            sdbt_csv_2.place(x=120, y=30)
            sdbt_csv_clicked = True



            check_button_clicks()





def open_sequence_txt():
    global seqbt_txt_clicked, seq
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        seq = open(file_path, 'r')
        seqbt2 = tk.Button(window, text=".txt (p)", bg="green", fg="white",  width=5, command=lambda: [open_sequence_txt(), skip_sequence_off(), open_sequence_fasta_off(), txt_h_off()])
        seqbt2.place(x=220, y=75)
        seqbt_txt_clicked = True
        check_button_clicks()
def seq_txt_off():
    global seqbt_txt_clicked
    seqbt_txt_clicked = False
    seqbt_txt = tk.Button(window, text=".txt (p)", bg="orange", fg="black", width=5,  command=lambda: [open_sequence_txt(), skip_sequence_off(), open_sequence_fasta_off(), txt_h_off()])
    seqbt_txt.place(x=220, y=75)

def open_sequence_fasta():
    global seqbt_fasta_clicked, fasta_file_path
    seqbt_fasta_clicked = True
    fasta_file_path = filedialog.askopenfilename(filetypes=[("Fasta Files", "*.fasta")])
    if fasta_file_path:
        seq_headers = open(fasta_file_path, 'r')
        for line in seq_headers:
            if line.startswith(">"):
                pieces = line.split(">")
                if len(pieces) == 2:
                    new_pieces = pieces[1].split()
                    if len(new_pieces) == 2:
                        if new_pieces[0].strip() == new_pieces[1].strip():
                            protein_name = new_pieces[1].strip()
                    if len(new_pieces) == 4:
                        if new_pieces[0] == new_pieces[2] and new_pieces[1] == new_pieces[3]:
                            protein_name = new_pieces[0] + " " + new_pieces[1]
                    if len(new_pieces) == 1:
                        protein_name = new_pieces[0].strip()
                if len(pieces) == 1:
                    protein_name = pieces[1].strip()
                if protein_name not in prot_seq_dic:
                    next_line = next(seq_headers, None)  # Read the next line
                    if next_line is not None and next_line.strip() != "":
                        prot_seq_dic[protein_name] = next_line.strip()
                    else:
                        next_next_line = next(seq_headers, None)
                        if next_next_line is not None and next_next_line.strip() != "":
                            prot_seq_dic[protein_name] = next_next_line.strip()

        seqbt_fasta = tk.Button(window, text=".fasta",bg="green",fg="white", width=5, command=lambda: [open_sequence_fasta(), seq_txt_off, skip_sequence_off(), txt_h_off()])
        seqbt_fasta.place(x=120, y=75)
        check_button_clicks()
def open_sequence_fasta_off():
    global seqbt_fasta_clicked
    seqbt_fasta_clicked = False
    seqbt_fasta = tk.Button(window, text=".fasta",bg="orange",fg="black", width=5, command=lambda: [open_sequence_fasta(), seq_txt_off, skip_sequence_off(), txt_h_off()])
    seqbt_fasta.place(x=120, y=75)

def txt_h_on():
    global txt_h_bt_clicked
    global prot_seq_dic
    txt_h_bt_clicked = True
    txt_h_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if txt_h_file_path:
        seq_headers = open(txt_h_file_path, 'r')

        for line in seq_headers:
            if line.startswith(">"):
                pieces = line.split(">")
                if len(pieces) == 2:
                    new_pieces = pieces[1].split()
                    if len(new_pieces) == 2:
                        if new_pieces[0].strip() == new_pieces[1].strip():
                            protein_name = new_pieces[1].strip()
                    if len(new_pieces) == 4:
                        if new_pieces[0] == new_pieces[2] and new_pieces[1] == new_pieces[3]:
                            protein_name = new_pieces[0] + " " + new_pieces[1]
                    if len(new_pieces) == 1:
                        protein_name = new_pieces[0].strip()
                if len(pieces) == 1:
                    protein_name = pieces[1].strip()
                if protein_name not in prot_seq_dic:
                    next_line = next(seq_headers, None)  # Read the next line
                    if next_line is not None and next_line.strip() != "":
                        prot_seq_dic[protein_name] = next_line.strip()
                    else:
                        next_next_line = next(seq_headers, None)
                        if next_next_line is not None and next_next_line.strip() != "":
                            prot_seq_dic[protein_name] = next_next_line.strip()


        txt_h_bt = tk.Button(window, text=".txt (>)",bg="green",fg="white", width=5, command=lambda: [seq_txt_off(), skip_sequence_off(), open_sequence_fasta_off(), txt_h_on()])
        txt_h_bt.place(x=170, y=75)

        check_button_clicks()

def txt_h_off():
    global txt_h_bt_clicked
    txt_h_bt_clicked = False
    txt_h_bt = tk.Button(window, text=".txt (>)",bg="orange",fg="black", width=5, command=lambda: [seq_txt_off(), skip_sequence_off(), open_sequence_fasta_off(), txt_h_on()])
    txt_h_bt.place(x=170, y=75)


def skip_sequence():
    global skip_bt_clicked
    skip_bt_clicked = True
    skip_bt2 = tk.Button(window, text="Skip",bg="green",fg="white", width=5, command=skip_sequence_off)
    skip_bt2.place(x=270, y=75)
    check_button_clicks()

def skip_sequence_off():
    global skip_bt_clicked
    skip_bt_clicked = False
    skip_bt = tk.Button(window, text="Skip",bg="orange",fg="black", width=5, command=lambda: [skip_sequence(), seq_txt_off(), open_sequence_fasta_off(), txt_h_off()])
    skip_bt.place(x=270, y=75)

def open_info():
    try:
        os.startfile("HDXWizard_Operating_Instructions_1.0.pdf")
    except:
        info_error = tk.Label(window, text="Error, cannot find information file")
        info_error.place(x=120, y=120)

window = tk.Tk()
window.geometry("1500x760")
window.title("HDXWizard")
canvas = tk.Canvas(window, width=1500, height=760)
canvas.place(x=0, y=0)

def go_to_git():
    webbrowser.open("https://github.com/ZacharyACohen/HDXWizard.git")

if program_needs_update is True:
    popup_window_update = tk.Toplevel(window)  # Create a new window for the popup menu
    popup_window_update.geometry("500x100")
    popup_window_update.title("Update Available")
    tk.Label(popup_window_update, text=f"Current Version: {version_number}").place(x=10, y=10)
    tk.Label(popup_window_update, text=f"Newest Version: {newest_version}").place(x=10, y=40)
    update_label = tk.Label(popup_window_update, text="Please go to https://github.com/ZacharyACohen/HDXWizard.git to update program")
    update_label.place(x=10, y=70)
    go_bt = tk.Button(popup_window_update, text="GO", command=go_to_git).place(x=460, y=68)
    popup_window_update.attributes("-topmost", True)



file_enter_lab = tk.Label(window, text="File Entry")
file_enter_lab.place(x=40, y=5)

sdlab = tk.Label(window, text="Insert State Data: ")
sdlab.place(x=15, y=30)

sdbt_csv = tk.Button(window, text=".csv",bg="orange",fg="black", width=5, command=open_sd_file_csv)
sdbt_csv.place(x=120, y=30)

sdbt_xlsx =tk.Button(window, text=".xlsx",bg="orange",fg="black", width=5, command=open_sd_file_xlsx)
sdbt_xlsx.place(x=170,y=30)


seqlab = tk.Label(window, text="Insert Sequence: ")
seqlab.place(x=15, y=75)

seqbt_txt = tk.Button(window, text=".txt (p)",bg="orange",fg="black", width=5, command=lambda: [open_sequence_txt(), skip_sequence_off(), open_sequence_fasta_off(), txt_h_off()])
seqbt_txt.place(x=220, y=75)

seqbt_fasta = tk.Button(window, text=".fasta",bg="orange",fg="black", width=5, command=lambda: [open_sequence_fasta(), seq_txt_off, skip_sequence_off(), txt_h_off()])
seqbt_fasta.place(x=120, y=75)

skip_bt = tk.Button(window, text="Skip",bg="orange",fg="black", width=5, command=lambda: [skip_sequence(), seq_txt_off(), open_sequence_fasta_off(), txt_h_off()])
skip_bt.place(x=270, y=75)

txt_h_bt = tk.Button(window, text=".txt (>)",bg="orange",fg="black", width=5, command=lambda: [seq_txt_off(), skip_sequence_off(), open_sequence_fasta_off(), txt_h_on()])
txt_h_bt.place(x=170, y=75)

sd_explain_lb = tk.Label(window, text="Add unlimited")
sd_explain_lb.place(x=220 ,y=33)
x1 = 10
x2 = 370
y=65
canvas.create_line(x1, y, x2, y)
seq_explain_lb = tk.Label(window, text="For fasta and .txt (>) files (.txt with fasta format): add unlimited")
seq_explain_lb.place(x=15, y=105)
seq_explain_lb2 = tk.Label(window, text="For .txt (p), add one file containing only one sequence (no header)")
seq_explain_lb2.place(x=15, y=120)

info_bt = tk.Button(window, text="INFO", bg="grey", fg="black", command=open_info)
info_bt.place(x=600, y=500)




def check_button_clicks():
    if (sdbt_xlsx_clicked or sdbt_csv_clicked) and (seqbt_txt_clicked or seqbt_fasta_clicked or skip_bt_clicked or txt_h_bt_clicked):

        msg1 = tk.Label(window, text="RFU Calculation and Correction")
        msg1.place(x=15, y=160)
        exp_bt = tk.Button(window, text="Experimental",bg="orange",fg="black",command=lambda: [theo_bt_off(), exp_bt_on()])
        exp_bt.place(x=170, y=190)
        theo_bt = tk.Button(window, text="Theoretical",bg="orange",fg="black",command=lambda: [exp_bt_off(), theo_bt_on()])
        theo_bt.place(x=50, y=190)

        x1 = 10
        y = 152
        x2 = 370
        canvas.create_line(x1, y, x2, y)

        x = 10
        y1 = 152
        y2 = 750

        canvas.create_line(x, y1, x, y2)

        x = 370
        y1 = 152
        y2 = 750

        canvas.create_line(x, y1, x, y2)


x1, y1 = 10, 10  # Top-left coordinates of the rectangle
x2, y2 = 370, 150  # Bottom-right coordinates of the rectangle
canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")

def increase_progress(x):
    progress['value'] += x
    window.update()

def start_progress():
    global progress
    pmax = 1
    if pepmap_bt_on:
        pmax = pmax + len(statedic_of_pepdic_cor)
    if difmap_bt_on:
        pmax = pmax + 1.5*len(new_dic_of_dif_list) + 1
    if chic_bt_on:
        pmax = pmax+0.33
    if cdif_bt_on:
        pmax=pmax + 0.33
    if condpeps_bt_on:
        pmax = pmax + len(statedic_of_pepdic_cor)
    if difcond_bt_on:
        pmax = pmax + len(new_dic_of_dif_list)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')
    progress = ttk.Progressbar(window, style='blue.Horizontal.TProgressbar', orient='horizontal', mode='determinate', length=200, maximum=pmax)
    progress.place(x=1270, y=160, width=200, height=25)  # Position the progress bar at the bottom left
    window.update()

difmap_bt_on = False
pepmap_bt_on = False
chic_bt_on = False
cdif_bt_on = False
condpeps_bt_on = False
difcond_bt_on = False
def difmap_on():
    global difmap_bt_on
    difmap_bt_2 = tk.Button(window, text="Peptide Difference",bg="green",fg="white",width=17, command=difmap_off)
    difmap_bt_2.place(x=1340,y=80)
    difmap_bt_on = True
def difmap_off():
    global difmap_bt_on
    difmap_bt = tk.Button(window, text="Peptide Difference",bg="orange",fg="black",width=17, command=difmap_on)
    difmap_bt.place(x=1340,y=80)
    difmap_bt_on = False
def pepmap_on():
    global pepmap_bt_on
    pepmap_bt_2 = tk.Button(window, text="Peptide Plot",bg="green",fg="white",width=17, command=pepmap_off)
    pepmap_bt_2.place(x=1190,y=80)
    pepmap_bt_on = True
def pepmap_off():
    global pepmap_bt_on
    pepmap_bt = tk.Button(window, text="Peptide Plot",bg="orange",fg="black",width=17, command=pepmap_on)
    pepmap_bt.place(x=1190,y=80)
    pepmap_bt_on = False
def chiclet_on():
    global chic_bt_on
    chiclet_bt_2 = tk.Button(window, text="Chiclet Plot",bg="green",fg="white",width=17, command=chiclet_off)
    chiclet_bt_2.place(x=1190,y=40)
    chic_bt_on = True
def chiclet_off():
    global chic_bt_on
    chic_bt = tk.Button(window, text="Chiclet Plot",bg="orange",fg="black", width=17, command=chiclet_on)
    chic_bt.place(x=1190,y=40)
    chic_bt_on = False
def cdif_on():
    global cdif_bt_on
    cdif_bt_2 = tk.Button(window, text="Chiclet Difference",bg="green",fg="white",width=17, command=cdif_off)
    cdif_bt_2.place(x=1340,y=40)
    cdif_bt_on = True
def cdif_off():
    global cdif_bt_on
    cdif_bt = tk.Button(window, text="Chiclet Difference",bg="orange",fg="black",width=17, command=cdif_on)
    cdif_bt.place(x=1340,y=40)
    cdif_bt_on = False
def condpeps_on():
    global condpeps_bt_on
    condpeps_bt_2 = tk.Button(window, text="Condensed Peptide",bg="green",fg="white",width=17, command=condpeps_off)
    condpeps_bt_2.place(x=1190,y=120)
    condpeps_bt_on = True
def condpeps_off():
    global condpeps_bt_on
    condpeps_bt = tk.Button(window, text="Condensed Peptide",bg="orange",fg="black",width=17, command=condpeps_on)
    condpeps_bt.place(x=1190,y=120)
    condpeps_bt_on = False
def difcond_on():
    global difcond_bt_on
    difcond_bt_2 = tk.Button(window, text="Condensed Difference",bg="green",fg="white",width=17, command=difcond_off)
    difcond_bt_2.place(x=1340,y=120)
    difcond_bt_on = True
def difcond_off():
    global difcond_bt_on
    difcond_bt = tk.Button(window, text="Condensed Difference",bg="orange",fg="black",width=17, command=difcond_on)
    difcond_bt.place(x=1340,y=120)
    difcond_bt_on = False


def create_custom_colors():
    def show_examples():
        try:
            os.startfile("Creating Custom Color Schemes.pdf")
        except:
            color_error = tk.Label(popup_window_uptake, text="Error, cannot find example file")
            color_error.place(x=730, y=360)
            print('yes')
    popup_window_uptake = tk.Toplevel(window)  # Create a new window for the popup menu
    popup_window_uptake.geometry("920x500")
    canvas = tk.Canvas(popup_window_uptake, width=920, height=500)
    canvas.place(x=0, y=0)
    x1 = 5
    y1 = 5
    x2 = 345
    y2 = 495
    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")
    tk.Label(popup_window_uptake, text="Create Custom Colors for All Uptake Maps").place(x=20, y=1)
    tk.Label(popup_window_uptake, text="Enter RFU as a decimal, with the highest exchanging color first").place(x=10, y=25)
    tk.Label(popup_window_uptake, text="Hexadecimal Color").place(x=115, y=50)
    tk.Label(popup_window_uptake, text="White Text").place(x=235, y=50)


    lab1 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab1.place(x=20, y=70)
    lab2 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab2.place(x=20, y=100)
    lab3 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab3.place(x=20, y=130)
    lab4 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab4.place(x=20, y=160)
    lab5 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab5.place(x=20, y=190)
    lab6 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab6.place(x=20, y=220)
    lab7 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab7.place(x=20, y=250)
    lab8 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab8.place(x=20, y=280)
    lab9 = tk.Label(popup_window_uptake, text="If RFU >           :")
    lab9.place(x=20, y=310)
    lab10 = tk.Label(popup_window_uptake, text="If RFU >  0       :")
    lab10.place(x=20, y=340)
    lab11 = tk.Label(popup_window_uptake, text="If RFU <  0       :")
    lab11.place(x=20, y=370)
    lab12 = tk.Label(popup_window_uptake, text="If RFU =  0       :")
    lab12.place(x=20, y=400)
    lab13 = tk.Label(popup_window_uptake, text="If Peptide Absent :")
    lab13.place(x=20, y=430)

    val1 = tk.Entry(popup_window_uptake, width=4)
    val1.place(x=67, y=70)
    val2 = tk.Entry(popup_window_uptake, width=4)
    val2.place(x=67, y=100)
    val3 = tk.Entry(popup_window_uptake, width=4)
    val3.place(x=67, y=130)
    val4 = tk.Entry(popup_window_uptake, width=4)
    val4.place(x=67, y=160)
    val5 = tk.Entry(popup_window_uptake, width=4)
    val5.place(x=67, y=190)
    val6 = tk.Entry(popup_window_uptake, width=4)
    val6.place(x=67, y=220)
    val7 = tk.Entry(popup_window_uptake, width=4)
    val7.place(x=67, y=250)
    val8 = tk.Entry(popup_window_uptake, width=4)
    val8.place(x=67, y=280)
    val9 = tk.Entry(popup_window_uptake, width=4)
    val9.place(x=67, y=310)


    col1 = tk.Entry(popup_window_uptake, width=8)
    col1.place(x=140, y=70)
    col2 = tk.Entry(popup_window_uptake, width=8)
    col2.place(x=140, y=100)
    col3 = tk.Entry(popup_window_uptake, width=8)
    col3.place(x=140, y=130)
    col4 = tk.Entry(popup_window_uptake, width=8)
    col4.place(x=140, y=160)
    col5 = tk.Entry(popup_window_uptake, width=8)
    col5.place(x=140, y=190)
    col6 = tk.Entry(popup_window_uptake, width=8)
    col6.place(x=140, y=220)
    col7 = tk.Entry(popup_window_uptake, width=8)
    col7.place(x=140, y=250)
    col8 = tk.Entry(popup_window_uptake, width=8)
    col8.place(x=140, y=280)
    col9 = tk.Entry(popup_window_uptake, width=8)
    col9.place(x=140, y=310)
    col10 = tk.Entry(popup_window_uptake, width=8)
    col10.place(x=140, y=340)
    col11 = tk.Entry(popup_window_uptake, width=8)
    col11.place(x=140, y=370)
    col12 = tk.Entry(popup_window_uptake, width=8)
    col12.place(x=140, y=400)
    col12.insert(0, "F2F2F2")
    col13 = tk.Entry(popup_window_uptake, width=8)
    col13.place(x=140, y=430)
    col13.insert(0, "FAE8D7")

    global chkval_1, chkval_2, chkval_3, chkval_4, chkval_5, chkval_6, chkval_7, chkval_8, chkval_9, chkval_10, chkval_11, chkval_12, chkval_13
    chkval_1 = tk.IntVar(value=1)
    txtchk1 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_1)
    txtchk1.place(x=255, y=65)

    chkval_2 = tk.IntVar(value=1)
    txtchk2 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_2)
    txtchk2.place(x=255, y=95)

    chkval_3 = tk.IntVar(value=1)
    txtchk3 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_3)
    txtchk3.place(x=255, y=125)

    chkval_4 = tk.IntVar(value=1)
    txtchk4 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_4)
    txtchk4.place(x=255, y=155)

    chkval_5 = tk.IntVar(value=1)
    txtchk5 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_5)
    txtchk5.place(x=255, y=185)

    chkval_6 = tk.IntVar(value=1)
    txtchk6 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_6)
    txtchk6.place(x=255, y=215)

    chkval_7 = tk.IntVar(value=1)
    txtchk7 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_7)
    txtchk7.place(x=255, y=245)

    chkval_8 = tk.IntVar(value=1)
    txtchk8 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_8)
    txtchk8.place(x=255, y=275)

    chkval_9 = tk.IntVar(value=1)
    txtchk9 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_9)
    txtchk9.place(x=255, y=305)

    chkval_10 = tk.IntVar(value=1)
    txtchk10 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_10)
    txtchk10.place(x=255, y=335)

    chkval_11 = tk.IntVar(value=1)
    txtchk11 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_11)
    txtchk11.place(x=255, y=365)

    chkval_12 = tk.IntVar(value=1)
    txtchk12 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_12)
    txtchk12.place(x=255, y=395)

    chkval_13 = tk.IntVar(value=1)
    txtchk13 = tk.Checkbutton(popup_window_uptake, text='', variable=chkval_13)
    txtchk13.place(x=255, y=425)

    def save_colors():
        vals = []
        if val1.get() != "":
            vals.append(val1.get())
        if val2.get() != "":
            vals.append(val2.get())
        if val3.get() != "":
            vals.append(val3.get())
        if val4.get() != "":
            vals.append(val4.get())
        if val5.get() != "":
            vals.append(val5.get())
        if val6.get() != "":
            vals.append(val6.get())
        if val7.get() != "":
            vals.append(val7.get())
        if val8.get() != "":
            vals.append(val8.get())
        if val9.get() != "":
            vals.append(val9.get())
        potential_val_error_1 = False
        potential_val_error_2 = False
        for i, val in enumerate(vals):
            if float(val) > 1:
                potential_val_error_2 = True
                break
            try:
                next_val = vals[i + 1]
            except:
                continue
            if next_val > val:
                potential_val_error_1 = True
                break


        if potential_val_error_1 == True:
            tk.Label(popup_window_uptake, text=f"Potential Error found. {next_val} > {val}").place(x=100, y=460)
        if potential_val_error_2 == True:
            tk.Label(popup_window_uptake, text=f"Potential Error found. {val} > 1")


        uptake_color_dic = {}
        if val1.get() != "" and col1.get() != "":
            uptake_color_dic[val1.get()] = col1.get()
        if val2.get() != "" and col2.get() != "":
            uptake_color_dic[val2.get()] = col2.get()
        if val3.get() != "" and col3.get() != "":
            uptake_color_dic[val3.get()] = col3.get()
        if val4.get() != "" and col4.get() != "":
            uptake_color_dic[val4.get()] = col4.get()
        if val5.get() != "" and col5.get() != "":
            uptake_color_dic[val5.get()] = col5.get()
        if val6.get() != "" and col6.get() != "":
            uptake_color_dic[val6.get()] = col6.get()
        if val7.get() != "" and col7.get() != "":
            uptake_color_dic[val7.get()] = col7.get()
        if val8.get() != "" and col8.get() != "":
            uptake_color_dic[val8.get()] = col8.get()
        if val9.get() != "" and col9.get() != "":
            uptake_color_dic[val9.get()] = col9.get()
        if col10.get() != "":
            uptake_color_dic[">0"] = col10.get()
        else:
            uptake_color_dic[">0"] = "000000"
        if col11.get() != "":
            uptake_color_dic["<0"] = col11.get()
        else:
            uptake_color_dic["<0"] = "000000"
        if col12.get() != "":
            uptake_color_dic["=0"] = col12.get()
        else:
            uptake_color_dic["=0"] = "F2F2F2"
        if col13.get() != "":
            uptake_color_dic[-99999] = col13.get()
        else:
            uptake_color_dic[-99999] = "FAE8D7"


        uptake_text_dic = {}
        if val1.get() != "" and col1.get != "":
            uptake_text_dic[val1.get()] = chkval_1.get()
        if val2.get() != "" and col2.get != "":
            uptake_text_dic[val2.get()] = chkval_2.get()
        if val3.get() != "" and col3.get != "":
            uptake_text_dic[val3.get()] = chkval_3.get()
        if val4.get() != "" and col4.get != "":
            uptake_text_dic[val4.get()] = chkval_4.get()
        if val5.get() != "" and col5.get() != "":
            uptake_text_dic[val5.get()] = chkval_5.get()
        if val6.get() != "" and col6.get() != "":
            uptake_text_dic[val6.get()] = chkval_6.get()
        if val7.get() != "" and col7.get() != "":
            uptake_text_dic[val7.get()] = chkval_7.get()
        if val8.get() != "" and col8.get() != "":
            uptake_text_dic[val8.get()] = chkval_8.get()
        if val9.get() != "" and col9.get() != "":
            uptake_text_dic[val9.get()] = chkval_9.get()
        uptake_text_dic[">0"] = chkval_10.get()
        uptake_text_dic["<0"] = chkval_11.get()
        uptake_text_dic["=0"] = chkval_12.get()
        uptake_text_dic[-99999] = chkval_13.get()
        json_data = {
            "header": "Uptake Colors",
            "uptake_color_dic": uptake_color_dic,
            "uptake_text_dic": uptake_text_dic
        }
        with open("./Colors/new_uptake_colors.json", 'w') as f:
            json.dump(json_data, f, indent = 4)
        tk.Label(popup_window_uptake, text="File Saved in /Colors. Please Change Name").place(x=100, y=475)




    save_bt_uptake = tk.Button(popup_window_uptake, text = "Save Colors", command=save_colors)
    save_bt_uptake.place(x=20, y=460)


    x1 = 347
    y1 = 5
    x2 = 915
    y2 = 495
    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")
    tk.Label(popup_window_uptake, text="Create Custom Colors for All Difference Maps").place(x=370, y=1)
    tk.Label(popup_window_uptake, text="Enter Difference with the highest absolute value differences first. For RFU enter as a decimal").place(x=360, y=50)
    tk.Label(popup_window_uptake, text="Is this difference in Daltons (Theoretical) or RFU (Experimental)").place(x=360, y=25)
    #switch between Da and RFU selection
    tk.Label(popup_window_uptake, text="Protection").place(x=440, y=70)
    x1=352
    y=89
    x2=625
    canvas.create_line(x1, y, x2, y)
    tk.Label(popup_window_uptake, text="Deprotection").place(x=720, y=70)
    x1 = 635
    y=89
    x2=895
    canvas.create_line(x1, y, x2, y)
    tk.Label(popup_window_uptake, text="Hexadecimal Color").place(x=445, y=90)
    tk.Label(popup_window_uptake, text="White Text").place(x=565, y=90)
    tk.Label(popup_window_uptake, text="Hexadecimal Color").place(x=727, y=90)
    tk.Label(popup_window_uptake, text="White Text").place(x=847, y=90)
    #cheese: fix show_examples if there is an error
    examples_bt = tk.Button(popup_window_uptake, text="See examples", command=show_examples)
    examples_bt.place(x=825, y=330)


    plab1 = tk.Label(popup_window_uptake, text="If dif >           :")
    plab1.place(x=360, y=120)
    plab2 = tk.Label(popup_window_uptake, text="If dif >           :")
    plab2.place(x=360, y=150)
    plab3 = tk.Label(popup_window_uptake, text="If dif >           :")
    plab3.place(x=360, y=180)
    plab4 = tk.Label(popup_window_uptake, text="If dif >           :")
    plab4.place(x=360, y=210)
    plab5 = tk.Label(popup_window_uptake, text="If dif >           :")
    plab5.place(x=360, y=240)
    plab6 = tk.Label(popup_window_uptake, text="If dif >  0        :")
    plab6.place(x=360, y=270)

    dlab1 = tk.Label(popup_window_uptake, text="If dif >           :")
    dlab1.place(x=640, y=120)
    dlab2 = tk.Label(popup_window_uptake, text="If dif >           :")
    dlab2.place(x=640, y=150)
    dlab3 = tk.Label(popup_window_uptake, text="If dif >           :")
    dlab3.place(x=640, y=180)
    dlab4 = tk.Label(popup_window_uptake, text="If dif >           :")
    dlab4.place(x=640, y=210)
    dlab5 = tk.Label(popup_window_uptake, text="If dif >           :")
    dlab5.place(x=640, y=240)
    dlab6 = tk.Label(popup_window_uptake, text="If dif >  0        :")
    dlab6.place(x=640, y=270)

    blab1 = tk.Label(popup_window_uptake, text="If dif =  0       :")
    blab1.place(x=360, y=300)
    blab2 = tk.Label(popup_window_uptake, text="If Peptide Absent :")
    blab2.place(x=360, y=330)

    pval1 = tk.Entry(popup_window_uptake, width=4)
    pval1.place(x=401, y=120)
    pval2 = tk.Entry(popup_window_uptake, width=4)
    pval2.place(x=401, y=150)
    pval3 = tk.Entry(popup_window_uptake, width=4)
    pval3.place(x=401, y=180)
    pval4 = tk.Entry(popup_window_uptake, width=4)
    pval4.place(x=401, y=210)
    pval5 = tk.Entry(popup_window_uptake, width=4)
    pval5.place(x=401, y=240)

    dval1 = tk.Entry(popup_window_uptake, width=4)
    dval1.place(x=681, y=120)
    dval2 = tk.Entry(popup_window_uptake, width=4)
    dval2.place(x=681, y=150)
    dval3 = tk.Entry(popup_window_uptake, width=4)
    dval3.place(x=681, y=180)
    dval4 = tk.Entry(popup_window_uptake, width=4)
    dval4.place(x=681, y=210)
    dval5 = tk.Entry(popup_window_uptake, width=4)
    dval5.place(x=681, y=240)

    pcol1 = tk.Entry(popup_window_uptake, width=8)
    pcol1.place(x=474, y=120)
    pcol2 = tk.Entry(popup_window_uptake, width=8)
    pcol2.place(x=474, y=150)
    pcol3 = tk.Entry(popup_window_uptake, width=8)
    pcol3.place(x=474, y=180)
    pcol4 = tk.Entry(popup_window_uptake, width=8)
    pcol4.place(x=474, y=210)
    pcol5 = tk.Entry(popup_window_uptake, width=8)
    pcol5.place(x=474, y=240)
    pcol6 = tk.Entry(popup_window_uptake, width=8)
    pcol6.place(x=474, y=270)
    pcol6.insert(0, "F2F2F2")

    bcol1 = tk.Entry(popup_window_uptake, width=8)
    bcol1.place(x=474, y=300)
    bcol1.insert(0, "F2F2F2")
    bcol2 = tk.Entry(popup_window_uptake, width=8)
    bcol2.place(x=474, y=330)
    bcol2.insert(0, "FAE8D7")

    dcol1 = tk.Entry(popup_window_uptake, width=8)
    dcol1.place(x=754, y=120)
    dcol2 = tk.Entry(popup_window_uptake, width=8)
    dcol2.place(x=754, y=150)
    dcol3 = tk.Entry(popup_window_uptake, width=8)
    dcol3.place(x=754, y=180)
    dcol4 = tk.Entry(popup_window_uptake, width=8)
    dcol4.place(x=754, y=210)
    dcol5 = tk.Entry(popup_window_uptake, width=8)
    dcol5.place(x=754, y=240)
    dcol6 = tk.Entry(popup_window_uptake, width=8)
    dcol6.place(x=754, y=270)
    dcol6.insert(0, "F2F2F2")

    global pchkval_1, pchkval_2, pchkval_3, pchkval_4, pchkval_5, pchkval_6, bchkval_1, bchkval_2, dchkval_1, dchkval_2, dchkval_3, dchkval_4, dchkval_5, dchkval_6
    pchkval_1 = tk.IntVar(value=1)
    ptxtchk1 = tk.Checkbutton(popup_window_uptake, text='', variable=pchkval_1)
    ptxtchk1.place(x=589, y=115)

    pchkval_2 = tk.IntVar(value=1)
    ptxtchk2 = tk.Checkbutton(popup_window_uptake, text='', variable=pchkval_2)
    ptxtchk2.place(x=589, y=145)

    pchkval_3 = tk.IntVar(value=1)
    ptxtchk3 = tk.Checkbutton(popup_window_uptake, text='', variable=pchkval_3)
    ptxtchk3.place(x=589, y=175)

    pchkval_4 = tk.IntVar(value=1)
    ptxtchk4 = tk.Checkbutton(popup_window_uptake, text='', variable=pchkval_4)
    ptxtchk4.place(x=589, y=205)

    pchkval_5 = tk.IntVar(value=1)
    ptxtchk5 = tk.Checkbutton(popup_window_uptake, text='', variable=pchkval_5)
    ptxtchk5.place(x=589, y=235)

    pchkval_6 = tk.IntVar(value=0)
    ptxtchk6 = tk.Checkbutton(popup_window_uptake, text='', variable=pchkval_6)
    ptxtchk6.place(x=589, y=265)

    dchkval_1 = tk.IntVar(value=1)
    dtxtchk1 = tk.Checkbutton(popup_window_uptake, text='', variable=dchkval_1)
    dtxtchk1.place(x=869, y=115)

    dchkval_2 = tk.IntVar(value=1)
    dtxtchk2 = tk.Checkbutton(popup_window_uptake, text='', variable=dchkval_2)
    dtxtchk2.place(x=869, y=145)

    dchkval_3 = tk.IntVar(value=1)
    dtxtchk3 = tk.Checkbutton(popup_window_uptake, text='', variable=dchkval_3)
    dtxtchk3.place(x=869, y=175)

    dchkval_4 = tk.IntVar(value=1)
    dtxtchk4 = tk.Checkbutton(popup_window_uptake, text='', variable=dchkval_4)
    dtxtchk4.place(x=869, y=205)

    dchkval_5 = tk.IntVar(value=1)
    dtxtchk5 = tk.Checkbutton(popup_window_uptake, text='', variable=dchkval_5)
    dtxtchk5.place(x=869, y=235)

    dchkval_6 = tk.IntVar(value=0)
    dtxtchk6 = tk.Checkbutton(popup_window_uptake, text='', variable=dchkval_6)
    dtxtchk6.place(x=869, y=265)

    bchkval_1 = tk.IntVar(value=0)
    btxtchk1 = tk.Checkbutton(popup_window_uptake, text='', variable=bchkval_1)
    btxtchk1.place(x=589, y=295)

    bchkval_2 = tk.IntVar(value=1)
    btxtchk2 = tk.Checkbutton(popup_window_uptake, text='', variable=bchkval_2)
    btxtchk2.place(x=589, y=325)


    def save_colors2():
        pvals = []
        dvals = []
        if pval1.get() != "":
            pvals.append(pval1.get())
        if pval2.get() != "":
            pvals.append(pval2.get())
        if pval3.get() != "":
            pvals.append(pval3.get())
        if pval4.get() != "":
            pvals.append(pval4.get())
        if pval5.get() != "":
            pvals.append(pval5.get())
        if dval1.get() != "":
            dvals.append(dval1.get())
        if dval2.get() != "":
            dvals.append(dval2.get())
        if dval3.get() != "":
            dvals.append(dval3.get())
        if dval4.get() != "":
            dvals.append(dval4.get())
        if dval5.get() != "":
            dvals.append(dval5.get())
        potential_val_error_1 = False
        for i, val in enumerate(pvals):
            try:
                next_val = pvals[i + 1]
            except:
                continue
            if next_val > val:
                potential_val_error_1 = True
                break
        if potential_val_error_1 == False:
            for i, val in enumerate(dvals):
                try:
                    next_val = dvals[i + 1]
                except:
                    continue
                if next_val > val:
                    potential_val_error_1 = True
                    break
        if potential_val_error_1 == True:
            tk.Label(popup_window_uptake, text=f"Potential Error found. {next_val} > {val}").place(x=500, y=420)

        protection_color_dic = {}
        if pval1.get() != "" and pcol1.get() != "":
            protection_color_dic[pval1.get()] = pcol1.get()
        if pval2.get() != "" and pcol2.get() != "":
            protection_color_dic[pval2.get()] = pcol2.get()
        if pval3.get() != "" and pcol3.get() != "":
            protection_color_dic[pval3.get()] = pcol3.get()
        if pval4.get() != "" and pcol4.get() != "":
            protection_color_dic[pval4.get()] = pcol4.get()
        if pval5.get() != "" and pcol5.get() != "":
            protection_color_dic[pval5.get()] = pcol5.get()
        if pcol6.get() != "":
            protection_color_dic[">0"] = pcol6.get()
        else:
            protection_color_dic[">0"] = "F2F2F2"
        deprotection_color_dic = {}
        if dval1.get() != "" and dcol1.get() != "":
            deprotection_color_dic[dval1.get()] = dcol1.get()
        if dval2.get() != "" and dcol2.get() != "":
            deprotection_color_dic[dval2.get()] = dcol2.get()
        if dval3.get() != "" and dcol3.get() != "":
            deprotection_color_dic[dval3.get()] = dcol3.get()
        if dval4.get() != "" and dcol4.get() != "":
            deprotection_color_dic[dval4.get()] = dcol4.get()
        if dval5.get() != "" and dcol5.get() != "":
            deprotection_color_dic[dval5.get()] = dcol5.get()
        if dcol6.get() != "":
            deprotection_color_dic[">0"] = dcol6.get()
        else:
            deprotection_color_dic[">0"] = "F2F2F2"
        both_color_dic = {}
        if bcol1.get() != "":
            both_color_dic["=0"] = bcol1.get()
        else:
            both_color_dic["=0"] = "F2F2F2"
        if bcol2.get() != "":
            both_color_dic[-99999] = bcol2.get()
        else:
            both_color_dic[-99999] = "FAE8D7"


        protection_text_dic = {}
        if pval1.get() != "" and pcol1.get != "":
            protection_text_dic[pval1.get()] = pchkval_1.get()
        if pval2.get() != "" and pcol2.get != "":
            protection_text_dic[pval2.get()] = pchkval_2.get()
        if pval3.get() != "" and pcol3.get != "":
            protection_text_dic[pval3.get()] = pchkval_3.get()
        if pval4.get() != "" and pcol4.get != "":
            protection_text_dic[pval4.get()] = pchkval_4.get()
        if pval5.get() != "" and pcol5.get() != "":
            protection_text_dic[pval5.get()] = pchkval_5.get()
        protection_text_dic[">0"] = pchkval_6.get()

        deprotection_text_dic = {}
        if dval1.get() != "" and dcol1.get != "":
            deprotection_text_dic[dval1.get()] = dchkval_1.get()
        if dval2.get() != "" and dcol2.get != "":
            deprotection_text_dic[dval2.get()] = dchkval_2.get()
        if dval3.get() != "" and dcol3.get != "":
            deprotection_text_dic[dval3.get()] = dchkval_3.get()
        if dval4.get() != "" and dcol4.get != "":
            deprotection_text_dic[dval4.get()] = dchkval_4.get()
        if dval5.get() != "" and dcol5.get() != "":
            deprotection_text_dic[dval5.get()] = dchkval_5.get()
        deprotection_text_dic[">0"] = dchkval_6.get()

        both_text_dic = {}
        both_text_dic["=0"] = bchkval_1.get()
        both_text_dic[-99999] = bchkval_2.get()
        json_data = {
            "header": "Difference Colors",
            "protection_color_dic": protection_color_dic,
            "protection_text_dic": protection_text_dic,
            "deprotection_color_dic": deprotection_color_dic,
            "deprotection_text_dic": deprotection_text_dic,
            "both_color_dic": both_color_dic,
            "both_text_dic": both_text_dic
        }
        with open("./Colors/new_dif_colors.json", 'w') as f:
            json.dump(json_data, f, indent=4)
        tk.Label(popup_window_uptake, text="File Saved in /Colors as 'new_dif_colors.json'. Please Change Name").place(x=500, y=455)


    save_bt_dif = tk.Button(popup_window_uptake, text = "Save Colors", command=save_colors2)
    save_bt_dif.place(x=370, y=460)













def create_format_box():
    format_title = tk.Label(window, text="Formatting Options")
    format_title.place(x=960, y=5)

    x1,y1 = 922, 10
    x2, y2 = 1170, 450
    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")



    folder_path = "./Colors"  # Path to the "Color Patterns" folder
    file_names = os.listdir(folder_path)  # Get a list of file names in the folder
    global uptake_color_scheme_dropdown, difference_color_scheme_dropdown
    uptake_color_scheme_dropdown = ttk.Combobox(window, values=file_names, width=17)
    uptake_color_scheme_dropdown.set("uptake_default.json")
    uptake_color_scheme_dropdown.bind("<<ComboboxSelected>>")
    uptake_color_scheme_dropdown.place(x=1030, y=30)
    tk.Label(window, text="Uptake Colors: ").place(x=930, y=30)
    tk.Label(window, text="Difference Colors: ").place(x=930, y=60)
    difference_color_scheme_dropdown = ttk.Combobox(window, values=file_names, width=17)
    if exp_bt_on_c == True:
        difference_color_scheme_dropdown.set("exp_dif_default.json")
    if theo_bt_on_c == True:
        difference_color_scheme_dropdown.set("theo_dif_default.json")
    difference_color_scheme_dropdown.bind("<<ComboboxSelected>>")
    difference_color_scheme_dropdown.place(x=1030, y=60)
    create_colors = tk.Button(window, text="Create Custom Colors", command=create_custom_colors)
    create_colors.place(x=980, y=90)
    chiclet_options_title = tk.Label(window, text="Chiclet Options")
    chiclet_options_title.place(x=930, y=140)
    x1 = 930
    x2 = 1162
    y = 164
    canvas.create_line(x1, y, x2, y)
    sorting_lb = tk.Label(window, text="Sort Peptides:")
    sorting_lb.place(x=930, y=170)
    global sort_var
    sort_var = tk.IntVar(value=1)
    chk1 = tk.Checkbutton(window, text='', variable=sort_var)
    chk1.place(x=1100, y=170)

    global con_pep_height_enter, con_pep_width_enter, full_pep_height_enter, full_pep_width_enter
    full_pepmap_title = tk.Label(window, text="Full Peptide Map Options")
    full_pepmap_title.place(x=930, y=220)
    x1 = 930
    x2 = 1162
    y = 244
    canvas.create_line(x1, y, x2, y)
    full_pep_width_lb = tk.Label(window, text = "Cell Width:")
    full_pep_width_lb.place(x=930, y=250)
    full_pep_width_enter = tk.Entry(window, width=5)
    full_pep_width_enter.insert(0, "4")
    full_pep_width_enter.place(x=1000, y=250)


    con_pepmap_title = tk.Label(window, text="Condensed Peptide Map Options")
    con_pepmap_title.place(x=930, y=320)
    x1 = 930
    x2 = 1162
    y = 344
    canvas.create_line(x1, y, x2, y)
    con_pep_width_lb = tk.Label(window, text = "Cell Width:")
    con_pep_width_lb.place(x=930, y=350)
    con_pep_width_enter = tk.Entry(window, width=5)
    con_pep_width_enter.insert(0, "2.5")
    con_pep_width_enter.place(x=1000, y=350)



    insig_dif_lb = tk.Label(window, text="Show Insignificant Values:")
    insig_dif_lb.place(x=930, y=380)
    global insig_dif_chk
    insig_dif_chk = tk.IntVar(value=1)
    insig_check = tk.Checkbutton(window, text='', variable=insig_dif_chk)
    insig_check.place(x=1100, y=380)

    tk.Label(window, text="Show Error:").place(x=930, y=410)
    global sd_checkvar
    sd_checkvar = tk.IntVar(value=1)
    sd_check = tk.Checkbutton(window, text='', variable=sd_checkvar)
    sd_check.place(x=1100, y=410)




def create_run_box():
    global run_bt
    run_box_title =tk.Label(window, text="Choose Scripts")
    run_box_title.place(x=1210, y=5)
    x1,y1 = 1172,10
    x2,y2= 1485, 450
    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")

    run_bt = tk.Button(window, text="\u23F5",bg="blue",fg="white",width=7, command=r_initialize)
    run_bt.place(x=1190,y=160)
    chic_bt = tk.Button(window, text="Chiclet Plot",bg="orange",fg="black", width=17, command=chiclet_on)
    chic_bt.place(x=1190,y=40)
    cdif_bt = tk.Button(window, text="Chiclet Difference",bg="orange",fg="black", width=17, command=cdif_on)
    cdif_bt.place(x=1340,y=40)
    pepmap_bt = tk.Button(window, text="Peptide Plot",bg="orange",fg="black", width=17, command=pepmap_on)
    pepmap_bt.place(x=1190,y=80)
    difmap_bt = tk.Button(window, text="Peptide Difference",bg="orange",fg="black",width=17, command=difmap_on)
    difmap_bt.place(x=1340,y=80)
    condpep_bt = tk.Button(window, text="Condensed Peptide",bg="orange",fg="black",width=17, command=condpeps_on)
    condpep_bt.place(x=1190,y=120)
    difcond_bt = tk.Button(window, text="Condensed Difference",bg="orange",fg="black",width=17, command=difcond_on)
    difcond_bt.place(x=1340,y=120)


def check_button_clicks2():
    global states, peplist, startvallist, endvallist, state_options, data, protein_states
    states = {}

    peplist = {}

    startvallist = {}

    endvallist = {}

    state_options =[]

    protein_states = {}


    msg2 = tk.Label(window, text="Add Differences")
    msg2.place(x=395, y=5)
    dif_bt = tk.Button(window, text="+Dif",bg="white",fg="black",command=dif_bt_done)
    dif_bt.place(x=495, y=10)


    x1, y1 = 372, 10  # Top-left coordinates of the rectangle
    x2, y2 = 920, 450  # Bottom-right coordinates of the rectangle
    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")

    create_format_box()

    create_run_box()




    # loop through each line in data
    for i, line in enumerate(data):
        protein = line[0]
        state = f"{line[0]}~{line[6]}"  # get the state from the 7th term
        peptide = line[3]  # get the peptide from the 1st term
        if protein not in protein_states:
            protein_states[protein] = True
        if state not in states:
            states[state] = True  # add state to dictionary
            peplist[state] = list() #create a peptidelist for eqach state
            startvallist[state] = list() #create a list of values for each state
            endvallist[state] = list()
        if peptide not in peplist[state]:
            peplist[state].append(peptide)
            startval = int(line[1])
            endval = int(line[2])
            startvallist[state].append(startval)
            endvallist[state].append(endval)
    for state in states:
        if state not in state_options:
            state_options.append(state)

    dif_bt_done()



def make_maxdic_dropdowns():
    global maxdic, dropdowns, snum, dropdown_widgets, label_widgets
    snum = 0
    dropdown_widgets = []  # List to store dropdown widgets
    label_widgets = []  # List to store label widgets
    for state in states:
        state_label = tk.Label(window, text=state + ":")
        font_size = 12
        while state_label.winfo_reqwidth() > 150:
            font_size = font_size-1
            state_label.config(font=("Arial", font_size))
        state_label.place(x= 10, y=(250+(25*snum)))
        label_widgets.append(state_label)

        dropdown_var = tk.StringVar(value=state)  # Create a unique StringVar for each dropdown
        dropdown = ttk.Combobox(window, values=state_options, width=28)
        dropdown.set(dropdown_var.get())
        dropdown.place(x=165, y=(250+(25*snum)))
        dropdown.bind("<<ComboboxSelected>>")
        dropdown_widgets.append(dropdown)

        dropdowns[state] = dropdown  # Map the dropdown variable to the state

        snum += 1






def create_custom_state():
    global state_options, avg1, avg2, popup_window

    popup_window = tk.Toplevel(window)  # Create a new window for the popup menu
    popup_window.geometry("200x250")

     # Calculate the desired position for the popup window
    x = window.winfo_x() + 100  # Adjust the value as needed
    y = window.winfo_y() + 200  # Adjust the value as needed

    # Set the position of the popup window
    popup_window.geometry(f"+{x}+{y}")

    average_lb = tk.Label(popup_window, text="Average two states:")
    average_lb.grid(column=0, row=0)


    options = state_options


    avg1 = ttk.Combobox(popup_window, values=options, width=28)
    avg1.grid(column=0, row=1, padx=5)

    avg2 = ttk.Combobox(popup_window, values=options, width=28)
    avg2.grid(column=0, row=2, padx=5)

    state_save_bt = tk.Button(popup_window, text="Save State", bg="white", fg="black", command=state_save)
    state_save_bt.grid(column=0, row=3)


    # You can further customize the popup window properties here if needed

    popup_window.transient(window)  # Set the main window as the parent of the popup window
    popup_window.grab_set()  # Grab the focus to the popup window
    popup_window.mainloop()  # Start the main loop for the popup window

def state_save():
    global state_options, popup_window
    state_options.append("pyAVG|"+f'{avg1.get()}'+'|' f'{avg2.get()}')
    state_save_lb = tk.Label(popup_window, text="State Saved")
    state_save_lb.grid(column=0, row=4)
    state_sav_lb2 = tk.Label(popup_window, text="(Only for maxD)")
    state_sav_lb2.grid(column=0, row=5)
    make_maxdic_dropdowns()


    global new_states_dic
    new_states_dic = {}
    for state_o in state_options:
        if state_o.startswith("pyAVG"):
            toavg_list = list()
            first_split = state_o.split("|")
            toavg_list.extend(first_split)
            toavg_list_con = [toavg_list[1], toavg_list[2]]
            new_states_dic[state_o] = toavg_list_con











exp_bt_on_c = False
theo_bt_on_c = False
def exp_bt_on():
    global exp_bt_on_c, maxD_label, custom_state_bt, exp_st_lb, maxD_peptides_lb, maxD_label_line, state_label_line
    exp_bt2 = tk.Button(window, text="Experimental",bg="green",fg="white",command=lambda: [exp_bt_off(), theo_bt_on()])
    exp_bt2.place(x=170, y=190)
    exp_bt_on_c = True

    check_button_clicks2()

    global maxdic, dropdowns
    maxdic = {}  # Initialize an empty dictionary
    dropdowns = {}  # Initialize an empty dictionary to store dropdown variables

    make_maxdic_dropdowns()

    exp_st_lb = tk.Label(window, text="State")
    exp_st_lb.place(x=35, y=223)
    maxD_peptides_lb = tk.Label(window, text="maxD Peptide Extraction")
    maxD_peptides_lb.place(x=170, y=223)
    custom_state_bt = tk.Button(window, text="Custom State", bg="white", fg="black", command=create_custom_state)
    custom_state_bt.place(x=275, y=190)

    x1 = 15
    y = 247
    x2 = 130
    state_label_line = canvas.create_line(x1, y, x2, y)

    x1 = 165
    y=247
    x2 = 347
    maxD_label_line = canvas.create_line(x1, y, x2, y)



def theo_bt_on():
    global theo_bt_on_c, be_entry, per_label, back_exchange_label
    theo_bt2 = tk.Button(window, text="Theoretical",bg="green",fg="white",command=lambda: [theo_bt_off(), exp_bt_on()])
    theo_bt2.place(x=50, y=190)
    theo_bt_on_c = True
    check_button_clicks2()
    back_exchange_label = tk.Label(window, text="Back Exchange:")
    back_exchange_label.place(x=20, y=220)
    global be_entry
    be_entry = tk.Entry(window, width=5)
    be_entry.insert(0, "0")
    be_entry.place(x=110, y=220)
    per_label = tk.Label(window, text="%")
    per_label.place(x=140, y=220)


def exp_bt_off():
    global exp_bt_on_c
    exp_bt1 = tk.Button(window, text="Experimental",bg="orange",fg="black",command=lambda: [theo_bt_off(), exp_bt_on()])
    exp_bt1.place(x=170, y=190)
    exp_bt_on_c = False
    global dropdown_widgets, label_widgets, custom_state_bt
    try:
        for dropdown in dropdown_widgets:
            dropdown.destroy()
        for label in label_widgets:
            label.destroy()
    except:
        pass
    try:
        custom_state_bt.destroy()
        exp_st_lb.destroy()
        maxD_peptides_lb.destroy()
    except:
        pass
    try:
        canvas.delete(maxD_label_line)
        canvas.delete(state_label_line)
    except:
        pass


def theo_bt_off():
    global theo_bt_on_c, be_entry, per_label, back_exchange_label
    theo_bt1 = tk.Button(window, text="Theoretical",bg="orange",fg="black",command=lambda: [exp_bt_off(), theo_bt_on()])
    theo_bt1.place(x=50, y=190)
    theo_bt_on_c = False
    try:
        back_exchange_label.destroy()
        per_label.destroy()
        be_entry.destroy()
    except:
        pass

onedif_state = tk.StringVar()
twodif_state = tk.StringVar()

def update_dropdown_options(event):
    if onedif_state.get() != "":
        onedif_dropdown["values"] = state_options
    if twodif_state.get() != "":
        twodif_dropdown["values"] = state_options


# s_entry1 = "dif1"
# s_entry2 = "dif2"
# s_entry3 = "dif3"
# s_entry4 = "dif4"
# s_entry5 = "dif5"
# s_entry6 = "dif6"
# s_entry7 = "dif7"
# s_entry8 = "dif8"
# s_entry9 = "dif9"
# s_entry10 = "dif10"
# s_entry11 = "dif11"
# s_entry12 = "dif12"

def dif_bt_done():
    minus_label = tk.Label(window, text="-")
    minus_label.place(x=564, y=60)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif_dropdown
    onedif_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif_dropdown.place(x=380, y=60)
    onedif_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif_dropdown
    twodif_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif_dropdown.place(x=580, y=60)
    twodif_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry1
    s_entry1 = tk.Entry(window)
    s_entry1.place(x=775, y=60)
    d_label = tk.Label(window, text="Difference Title:")
    d_label.place(x=795, y=35)
    onedif_lb = tk.Label(window, text="State One")
    onedif_lb.place(x=430, y=35)
    twodif_lb = tk.Label(window, text="State Two")
    twodif_lb.place(x=630, y=35)

    dif_bt2 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt2_done)
    dif_bt2.place(x=495, y=10)

def dif_bt2_done():
    minus_label2 = tk.Label(window, text="-")
    minus_label2.place(x=564, y=90)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif2_dropdown
    onedif2_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif2_dropdown.place(x=380, y=90)
    onedif2_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif2_dropdown
    twodif2_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif2_dropdown.place(x=580, y=90)
    twodif2_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry2
    s_entry2 = tk.Entry(window)
    s_entry2.place(x=775, y=90)

    dif_bt3 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt3_done)
    dif_bt3.place(x=495, y=10)

def dif_bt3_done():
    minus_label3 = tk.Label(window, text="-")
    minus_label3.place(x=564, y=120)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif3_dropdown
    onedif3_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif3_dropdown.place(x=380, y=120)
    onedif3_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif3_dropdown
    twodif3_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif3_dropdown.place(x=580, y=120)
    twodif3_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry3
    s_entry3 = tk.Entry(window)
    s_entry3.place(x=775, y=120)

    dif_bt4 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt4_done)
    dif_bt4.place(x=495, y=10)

def dif_bt4_done():
    minus_label4 = tk.Label(window, text="-")
    minus_label4.place(x=564, y=150)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif4_dropdown
    onedif4_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif4_dropdown.place(x=380, y=150)
    onedif4_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif4_dropdown
    twodif4_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif4_dropdown.place(x=580, y=150)
    twodif4_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry4
    s_entry4 = tk.Entry(window)
    s_entry4.place(x=775, y=150)

    dif_bt5 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt5_done)
    dif_bt5.place(x=495, y=10)

def dif_bt5_done():
    minus_label5 = tk.Label(window, text="-")
    minus_label5.place(x=564, y=180)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif5_dropdown
    onedif5_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif5_dropdown.place(x=380, y=180)
    onedif5_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif5_dropdown
    twodif5_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif5_dropdown.place(x=580, y=180)
    twodif5_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry5
    s_entry5 = tk.Entry(window)
    s_entry5.place(x=775, y=180)

    dif_bt6 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt6_done)
    dif_bt6.place(x=495, y=10)

def dif_bt6_done():
    minus_label6 = tk.Label(window, text="-")
    minus_label6.place(x=564, y=210)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif6_dropdown
    onedif6_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif6_dropdown.place(x=380, y=210)
    onedif6_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif6_dropdown
    twodif6_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif6_dropdown.place(x=580, y=210)
    twodif6_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry6
    s_entry6 = tk.Entry(window)
    s_entry6.place(x=775, y=210)

    dif_bt7 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt7_done)
    dif_bt7.place(x=495, y=10)

def dif_bt7_done():
    minus_label7 = tk.Label(window, text="-")
    minus_label7.place(x=564, y=240)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif7_dropdown
    onedif7_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif7_dropdown.place(x=380, y=240)
    onedif7_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif7_dropdown
    twodif7_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif7_dropdown.place(x=580, y=240)
    twodif7_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry7
    s_entry7 = tk.Entry(window)
    s_entry7.place(x=775, y=240)

    dif_bt8 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt8_done)
    dif_bt8.place(x=495, y=10)

def dif_bt8_done():
    minus_label8 = tk.Label(window, text="-")
    minus_label8.place(x=564, y=270)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif8_dropdown
    onedif8_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif8_dropdown.place(x=380, y=270)
    onedif8_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif8_dropdown
    twodif8_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif8_dropdown.place(x=580, y=270)
    twodif8_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry8
    s_entry8 = tk.Entry(window)
    s_entry8.place(x=775, y=270)

    dif_bt9 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt9_done)
    dif_bt9.place(x=495, y=10)
def dif_bt9_done():
    minus_label9 = tk.Label(window, text="-")
    minus_label9.place(x=564, y=300)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif9_dropdown
    onedif9_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif9_dropdown.place(x=380, y=300)
    onedif9_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif9_dropdown
    twodif9_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif9_dropdown.place(x=580, y=300)
    twodif9_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry9
    s_entry9 = tk.Entry(window)
    s_entry9.place(x=775, y=300)

    dif_bt10 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt10_done)
    dif_bt10.place(x=495, y=10)

def dif_bt10_done():
    minus_label10 = tk.Label(window, text="-")
    minus_label10.place(x=564, y=330)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif10_dropdown
    onedif10_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif10_dropdown.place(x=380, y=330)
    onedif10_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif10_dropdown
    twodif10_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif10_dropdown.place(x=580, y=330)
    twodif10_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry10
    s_entry10 = tk.Entry(window)
    s_entry10.place(x=775, y=330)

    dif_bt11 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt11_done)
    dif_bt11.place(x=495, y=10)
def dif_bt11_done():
    minus_label11 = tk.Label(window, text="-")
    minus_label11.place(x=564, y=360)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif11_dropdown
    onedif11_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif11_dropdown.place(x=380, y=360)
    onedif11_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif11_dropdown
    twodif11_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif11_dropdown.place(x=580, y=360)
    twodif11_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry11
    s_entry11 = tk.Entry(window)
    s_entry11.place(x=775, y=360)

    dif_bt12 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt12_done)
    dif_bt12.place(x=495, y=10)

def dif_bt12_done():
    minus_label12 = tk.Label(window, text="-")
    minus_label12.place(x=564, y=390)

    filtered_options = []
    for state in state_options:
        if not state.startswith("pyAVG"):
            filtered_options.append(state)

    global onedif12_dropdown
    onedif12_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    onedif12_dropdown.place(x=380, y=390)
    onedif12_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global twodif12_dropdown
    twodif12_dropdown = ttk.Combobox(window, values=filtered_options, width=26)
    twodif12_dropdown.place(x=580, y=390)
    twodif12_dropdown.bind("<<ComboboxSelected>>", update_dropdown_options)

    global s_entry12
    s_entry12 = tk.Entry(window)
    s_entry12.place(x=775, y=390)

    dif_bt13 = tk.Button(window, text="+Dif", bg="white", fg="black", command=dif_bt13_done)
    dif_bt13.place(x=495, y=10)

def dif_bt13_done():
    maxstates_error1 = tk.Label(window, text="Sorry, a maximum of 12 differences is supported")
    maxstates_error1.place(x=480, y=420)



dif_list = []
dic_of_dif_list = {}
new_dic_of_dif_list = {}
pairlist = []
title_list = []
def check_dif_reqs():
    global new_dic_of_dif_list
    try:
        dic_of_dif_list[s_entry1.get()] = [onedif_dropdown.get(), twodif_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry2.get()] = [onedif2_dropdown.get(), twodif2_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry3.get()] =[onedif3_dropdown.get(), twodif3_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry4.get()] = [onedif4_dropdown.get(), twodif4_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry5.get()] = [onedif5_dropdown.get(), twodif5_dropdown.get()]
    except:
        pass
    try:
        dic_of_dif_list[s_entry6.get()] = [onedif6_dropdown.get(), twodif6_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry7.get()] = [onedif7_dropdown.get(), twodif7_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry8.get()] =[onedif8_dropdown.get(), twodif8_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry9.get()] = [onedif9_dropdown.get(), twodif9_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry10.get()] = [onedif10_dropdown.get(), twodif10_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry11.get()] = [onedif11_dropdown.get(), twodif11_dropdown.get()]
    except:
        pass
    try:
         dic_of_dif_list[s_entry12.get()] = [onedif12_dropdown.get(), twodif12_dropdown.get()]
    except:
        pass
    for stt, pair in  dic_of_dif_list.items():
        if pair[0] == "" or pair[1] == "":
            continue
        pairlist.append(pair)
        title_list.append(stt)
    x=0
    for title in title_list:
        new_dic_of_dif_list[title] = pairlist[x]
        x=x+1


global comp_error_lab
comp_error_lab = None

def r_initialize():
    global comp_error_lab
    try:
        tit_bt.destroy()
    except:
        pass
    if comp_error_lab is not None:
        comp_error_lab.destroy()
    new_dic_of_dif_lists = {}
    check_dif_reqs()

    global uptake_color_length, uptake_val_1, uptake_col_1, uptake_val_2, uptake_col_2, uptake_val_3, uptake_col_3, uptake_val_4, uptake_col_4, uptake_val_5, uptake_col_5, uptake_val_6, uptake_col_6, uptake_val_7, uptake_col_7, uptake_val_8, uptake_col_8, uptake_val_9, uptake_col_9, uptake_eqz_key, uptake_abs_key, uptake_ltz_key, uptake_gtz_key, uptake_text_1, uptake_text_2, uptake_text_3, uptake_text_4, uptake_text_5, uptake_text_6, uptake_text_7, uptake_text_8, uptake_text_9, uptake_gtz_text, uptake_eqz_text, uptake_ltz_text, uptake_abs_text
    uptake_val_1 = 0
    uptake_val_2 = 0
    uptake_val_3 = 0
    uptake_val_4 = 0
    uptake_val_5 = 0
    uptake_val_6 = 0
    uptake_val_7 = 0
    uptake_val_8 = 0
    uptake_val_9 = 0
    uptake_color_length = 0
    with open("./Colors/" + uptake_color_scheme_dropdown.get(), 'r') as f:
        json_data = json.load(f)
        if json_data.get("header") == "Uptake Colors":
            uptake_color_dic = json_data.get("uptake_color_dic", {})
            uptake_text_dic = json_data.get("uptake_text_dic", {})
        else:
            comp_error_lab = tk.Label(window, text="Uptake color selection is not compatible")
            comp_error_lab.place(x=1190, y=190)
            run_bt.config(state="normal")
            run_bt.config(relief="raised")
            return
        x = 1
        for key, color in uptake_color_dic.items():
            if key == "=0":
                uptake_eqz_key = color
                continue
            if key == "-99999":
                uptake_abs_key = color
                continue
            if key == ">0":
                uptake_gtz_key = color
                continue
            if key == "<0":
                uptake_ltz_key = color
                continue
            if x == 1:
                uptake_val_1 = float(key)
                uptake_col_1 = color
                uptake_color_length = 1
            elif x == 2:
                uptake_val_2 = float(key)
                uptake_col_2 = color
                uptake_color_length = 2
            elif x == 3:
                uptake_val_3 = float(key)
                uptake_col_3 = color
                uptake_color_length = 3
            elif x == 4:
                uptake_val_4 = float(key)
                uptake_col_4 = color
                uptake_color_length = 4
            elif x == 5:
                uptake_val_5 = float(key)
                uptake_col_5 = color
                uptake_color_length = 5
            elif x == 6:
                uptake_val_6 = float(key)
                uptake_col_6 = color
                uptake_color_length = 6
            elif x == 7:
                uptake_val_7 = float(key)
                uptake_col_7 = color
                uptake_color_length = 7
            elif x == 8:
                uptake_val_8 = float(key)
                uptake_col_8 = color
                uptake_color_length = 8
            elif x == 9:
                uptake_val_9 = float(key)
                uptake_col_9 = color
                uptake_color_length = 9
            x += 1

        for key, text in uptake_text_dic.items():
            try:
                key = float(key)
            except:
                pass
            if text == 1:
                text = 'FFFFFFFF'
            if text == 0:
                text = 'FF000000'
            if key == "=0":
                uptake_eqz_text = text
            if key == "-99999":
                uptake_abs_text = text
            if key == ">0":
                uptake_gtz_text = text
            if key == "<0":
                uptake_ltz_text = text
            if key == uptake_val_1:
                uptake_text_1 = text
            if key == uptake_val_2:
                uptake_text_2 = text
            if key == uptake_val_3:
                uptake_text_3 = text
            if key == uptake_val_4:
                uptake_text_4 = text
            if key == uptake_val_5:
                uptake_text_5 = text
            if key == uptake_val_6:
                uptake_text_6 = text
            if key == uptake_val_7:
                uptake_text_7 = text
            if key == uptake_val_8:
                uptake_text_8 = text
            if key == uptake_val_9:
                uptake_text_9 = text

    global p_val_1, p_val_2, p_val_3, p_val_4, p_val_5, d_val_1, d_val_2, d_val_3, d_val_4, d_val_5, p_col_1, p_col_2, p_col_3, p_col_4, p_col_5, d_col_1, d_col_2, d_col_3, d_col_4, d_col_5, p_col_gtz, p_col_length, p_text_1, p_text_2, p_text_3, p_text_4, p_text_5, d_text_1, d_text_2, d_text_3, d_text_4, d_text_5, p_text_gtz, d_col_gtz, d_text_gtz, d_col_length, b_col_eqz, b_col_abs, b_text_eqz, b_text_abs
    p_val_1 = 0
    p_val_2 = 0
    p_val_3 = 0
    p_val_4 = 0
    p_val_5 = 0
    d_val_1 = 0
    d_val_2 = 0
    d_val_3 = 0
    d_val_4 = 0
    d_val_5 = 0
    p_col_length = 0
    d_col_length = 0
    with open("./Colors/" + difference_color_scheme_dropdown.get(), 'r') as f:
        json_data = json.load(f)
        if json_data.get("header") == "Difference Colors":
            pval_color_dic = json_data.get("protection_color_dic", {})
            pval_text_dic = json_data.get("protection_text_dic", {})
            dval_color_dic = json_data.get("deprotection_color_dic", {})
            dval_text_dic = json_data.get("deprotection_text_dic", {})
            bval_color_dic = json_data.get("both_color_dic", {})
            bval_text_dic = json_data.get("both_text_dic", {})
        else:
            comp_error_lab = tk.Label(window, text="Difference color selection is not compatible")
            comp_error_lab.place(x=1190, y=190)
            run_bt.config(state="normal")
            run_bt.config(relief="raised")
            return
        x = 1
        for key, color in pval_color_dic.items():
            if key == ">0":
                p_col_gtz = color
                continue
            if x == 1:
                p_val_1 = float(key)
                p_col_1 = color
                p_col_length = 1
            elif x == 2:
                p_val_2 = float(key)
                p_col_2 = color
                p_col_length = 2
            elif x == 3:
                p_val_3 = float(key)
                p_col_3 = color
                p_col_length = 3
            elif x == 4:
                p_val_4 = float(key)
                p_col_4 = color
                p_col_length = 4
            elif x == 5:
                p_val_5 = float(key)
                p_col_5 = color
                p_col_length = 5
            x += 1
        for key, text in pval_text_dic.items():
            try:
                key = float(key)
            except:
                pass
            if text == 1:
                text = 'FFFFFFFF'
            if text == 0:
                text = 'FF000000'
            if key == ">0":
                p_text_gtz = text
            if key == p_val_1:
                p_text_1 = text
            elif key == p_val_2:
                p_text_2 = text
            elif key == p_val_3:
                p_text_3 = text
            elif key == p_val_4:
                p_text_4 = text
            elif key == p_val_5:
                p_text_5 = text

        x = 1
        for key, color in dval_color_dic.items():
            if key == ">0":
                d_col_gtz = color
                continue
            if x == 1:
                d_val_1 = float(key)
                d_col_1 = color
                d_col_length = 1
            elif x == 2:
                d_val_2 = float(key)
                d_col_2 = color
                d_col_length = 2
            elif x == 3:
                d_val_3 = float(key)
                d_col_3 = color
                d_col_length = 3
            elif x == 4:
                d_val_4 = float(key)
                d_col_4 = color
                d_col_length = 4
            elif x == 5:
                d_val_5 = float(key)
                d_col_5 = color
                d_col_length = 5
            x += 1
        for key, text in dval_text_dic.items():
            try:
                key = float(key)
            except:
                pass
            if text == 1:
                text = 'FFFFFFFF'
            if text == 0:
                text = 'FF000000'
            if key == ">0":
                d_text_gtz = text
            if key == d_val_1:
                d_text_1 = text
            elif key == d_val_2:
                d_text_2 = text
            elif key == d_val_3:
                d_text_3 = text
            elif key == d_val_4:
                d_text_4 = text
            elif key == d_val_5:
                d_text_5 = text

        for key, color in bval_color_dic.items():
            if key == "=0":
                b_col_eqz = color
            if key == "-99999":
                b_col_abs = color
        for key, text in bval_text_dic.items():
            if text == 1:
                text = 'FFFFFFFF'
            if text == 0:
                text = 'FF000000'
            if key == "=0":
                b_text_eqz = text
            if key == "-99999":
                b_text_abs = text





    global statedic_of_pepdic_cor, new_dic_of_dif_list, s_timepoints
    statedic_of_pepdic_cor = {}
    run_bt.config(state="disabled")
    run_bt.config(relief="sunken", bg="white", fg="black")
    s_timepoints = {}
    for state in states:
        timepoints = list()
        for i, line in enumerate(data):
            if f"{line[0]}~{line[6]}" == state:
                timepoint = float(line[7])
                if timepoint not in timepoints:
                    timepoints.append(timepoint)
        timepoints.sort()
        s_timepoints[state] = timepoints



    global statedic_of_pepdic_raw, statedic_of_sddic_raw
    statedic_of_pepdic_raw = {}
    statedic_of_sddic_raw = {}
    for state in states:
        if state not in statedic_of_pepdic_raw:
            statedic_of_pepdic_raw[state] = True
            pepdic_raw = {}
            sddic_raw = {}
        for peptide in peplist[state]:
            upt_tp_tup_list = list()
            sd_tp_tup_list = list()
            for i, line in enumerate(data):
                if line[3] == peptide and f"{line[0]}~{line[6]}" == state:
                    uptake = float(line[10])
                    SD = float(line[11])
                    tmpt = float(line[7])
                    upt_tp_tup_list.append((uptake, tmpt))
                    sd_tp_tup_list.append((SD, tmpt))
                    upt_tp_tup_list = sorted(upt_tp_tup_list, key=lambda x: x[1])
                    sd_tp_tup_list = sorted(sd_tp_tup_list, key=lambda x: x[1])

            new_upt_tp_tup_list = []
            np_up_tp_array = np.array(upt_tp_tup_list, dtype=[('uptake', float), ('timepoint', float)])
            unique_timepoints = np.unique(np_up_tp_array['timepoint'])
            for timepoint in unique_timepoints:
                uptakes_at_timepoint = np_up_tp_array['uptake'][np_up_tp_array['timepoint'] == timepoint]
                average_uptake = np.mean(uptakes_at_timepoint)
                new_upt_tp_tup_list.append((average_uptake, timepoint))
            pepdic_raw[peptide] = sorted(new_upt_tp_tup_list, key=lambda x: x[1])


            new_sd_tp_tup_list = []
            np_sd_tp_array = np.array(sd_tp_tup_list, dtype=[('standard deviation', float), ('timepoint', float)])
            unique_timepoints = np.unique(np_sd_tp_array['timepoint'])
            for timepoint in unique_timepoints:
                sds_at_timepoint = np_sd_tp_array['standard deviation'][np_sd_tp_array['timepoint'] == timepoint]
                combined_sd = np.sqrt(np.sum(sds_at_timepoint ** 2))
                new_sd_tp_tup_list.append((combined_sd, timepoint))
            sddic_raw[peptide] = sorted(new_sd_tp_tup_list, key=lambda x: x[1])

        statedic_of_pepdic_raw[state] = pepdic_raw
        statedic_of_sddic_raw[state] = sddic_raw



    global statedic_of_pepdic_raw2
    statedic_of_pepdic_raw2 = {}
    for state, pepdic_raw in statedic_of_pepdic_raw.items():
        pepdic_raw2 = {}
        for peptide, upt_tp_tups in pepdic_raw.items():
            upt_tp_tups2 = list()
            for timepoint in s_timepoints[state]:
                timepoint_found = False
                for uptake, tp in upt_tp_tups:
                    if timepoint == tp:
                        timepoint_found = True
                        break
                if timepoint_found == False:
                    new_tup = (-99999, timepoint)
                    upt_tp_tups2.append(new_tup)
                    pepdic_raw2[peptide] = upt_tp_tups2
                if timepoint_found == True:
                    upt_tp_tups2.append((uptake, tp))
            upt_tp_tups2 = sorted(upt_tp_tups2, key=lambda x: x[1])
            pepdic_raw2[peptide] = upt_tp_tups2

        statedic_of_pepdic_raw2[state] = pepdic_raw2


    global statedic_of_sddic_raw2
    statedic_of_sddic_raw2 = {}
    for state, sddic_raw in statedic_of_sddic_raw.items():
        sddic_raw2 = {}
        for peptide, sd_tp_tups in sddic_raw.items():
            sd_tp_tups2 = list()
            for timepoint in s_timepoints[state]:
                timepoint_found = False
                for sd, tp in sd_tp_tups:
                    if timepoint == tp:
                        timepoint_found = True
                        break
                if timepoint_found == False:
                    new_sd = (-99999, timepoint)
                    sd_tp_tups2.append(new_sd)
                    sddic_raw2[peptide] = upt_tp_tups2
                if timepoint_found == True:
                    sd_tp_tups2.append((sd, tp))
            sd_tp_tups2 = sorted(sd_tp_tups2, key=lambda x: x[1])
            sddic_raw2[peptide] = sd_tp_tups2
        statedic_of_sddic_raw2[state] = sddic_raw2

    global noD_dic_states, statedic_of_sddic_cor
    noD_dic_states = {}
    statedic_of_pepdic_cor = {}
    statedic_of_sddic_cor = {}
    if exp_bt_on_c == True:
        for state, dropdown in dropdowns.items():
            selected_value = dropdown.get()
            maxdic[state] = selected_value

        for state, pepdic_raw2 in statedic_of_pepdic_raw2.items():
            if not maxdic[state].startswith("pyAVG"):
                maxfile = maxdic[state]

                noD_dic_peptides = {}
                maxd_list = list()
                maxSD_list = list()
                maxtheo_list = list()
                for peptide, upt_tp_tups in pepdic_raw2.items():
                    try:
                        maxfile_up_tp_tups = statedic_of_pepdic_raw2[maxfile][peptide]
                        max_tp = max(maxfile_up_tp_tups, key=lambda x: x[1])[1]
                        maxD = next(x[0] for x in maxfile_up_tp_tups if x[1] == max_tp)
                    except:
                        maxD = -99999
                    try:
                        maxfile_sd_tp_tups = statedic_of_sddic_raw2[maxfile][peptide]
                        max_tp = max(maxfile_sd_tp_tups, key=lambda x: x[1])[1]
                        maxSD = next(x[0] for x in maxfile_sd_tp_tups if x[1] == max_tp)
                    except:
                        maxSD = -99999
                    if maxD != -99999:
                        maxd_list.append(maxD)
                        if maxSD != -99999:
                            maxSD_list.append(maxSD)
                        length = len(peptide)
                        prolinecount=0
                        for letter in peptide:
                            if letter == 'P':
                                prolinecount = prolinecount+1
                        if peptide[0] == 'P':
                            max_theo = length-prolinecount
                        else:
                            max_theo = (length-1)-prolinecount
                        maxtheo_list.append(max_theo)
                    else:
                        noD_dic_peptides[peptide] = True
                noD_dic_states[state] = noD_dic_peptides
                if len(maxd_list) != 0:
                    total_uptake = sum(maxd_list)
                    total_theo = sum(maxtheo_list)
                    sd_array_squared = np.asarray(maxSD_list) ** 2
                    sd_comb = (np.sqrt(np.sum(sd_array_squared)))/len(maxSD_list)
                    average_rfu = (total_uptake / total_theo)
                    average_rfu_sd_percent = sd_comb / (total_uptake/len(maxd_list))
                    average_rfu_sd = average_rfu_sd_percent * average_rfu
                else:
                    average_rfu = 1
                    average_rfu_sd = 0



                pepdic_cor = {}
                sddic_cor = {}
                for peptide, upt_tp_tups in pepdic_raw2.items():
                    try:
                        maxfile_up_tp_tups = statedic_of_pepdic_raw2[maxfile][peptide]
                        max_tp = max(maxfile_up_tp_tups, key=lambda x: x[1])[1]
                        maxD = next(x[0] for x in maxfile_up_tp_tups if x[1] == max_tp)
                    except:
                        maxD = -99999
                    try:
                        maxfile_sd_tp_tups = statedic_of_sddic_raw2[maxfile][peptide]
                        max_tp = max(maxfile_sd_tp_tups, key=lambda x: x[1])[1]
                        maxSD = next(x[0] for x in maxfile_sd_tp_tups if x[1] == max_tp)
                    except:
                        maxSD = -99999
                    if maxD == -99999:
                        length = len(peptide)
                        prolinecount=0
                        for letter in peptide:
                            if letter == 'P':
                                prolinecount = prolinecount+1
                        if peptide[0] == 'P':
                            maxD_i = length-prolinecount
                        else:
                            maxD_i = (length-1)-prolinecount
                        maxD = maxD_i * average_rfu
                        maxSD = (float(average_rfu_sd) / float(average_rfu)) * maxD

                    Dcorrected_tups = list()
                    Dcorrected_sd_tups = list()
                    sd_tp_tups = statedic_of_sddic_raw2[state][peptide]
                    for uptake, timepoint in upt_tp_tups:
                        if uptake != -99999:
                            Dcorrected = (float(uptake) / float(maxD))
                            for sd, tp in sd_tp_tups:
                                if tp == timepoint:
                                    uptake_SD = float(sd)
                                    break
                            if uptake_SD != -99999 and uptake != 0 and maxSD != -99999:
                                Dcorrected_SD_percent = np.sqrt((((uptake_SD)/(float(uptake))) ** 2) + (((maxSD)/(float(maxD))) ** 2))
                                Dcorrected_SD = Dcorrected_SD_percent * Dcorrected
                            else:
                                Dcorrected_SD = -99999

                        else:
                            Dcorrected = -99999
                            Dcorrected_SD = -99999
                        Dcorrected_tups.append((Dcorrected, timepoint))
                        Dcorrected_sd_tups.append((Dcorrected_SD, timepoint))
                    pepdic_cor[peptide] = Dcorrected_tups
                    sddic_cor[peptide] = Dcorrected_sd_tups
                statedic_of_pepdic_cor[state] = pepdic_cor
                statedic_of_sddic_cor[state] = sddic_cor



            if maxdic[state].startswith("pyAVG"):
                pepdic_cor = {}
                sddic_cor = {}
                maxd_list = list()
                maxtheo_list = list()
                maxSD_list = list()
                maxfiles = new_states_dic[maxdic[state]]
                st1 = maxfiles[0]
                st2 = maxfiles[1]

                noD_dic_peptides = {}
                for peptide, upt_tp_tups in pepdic_raw2.items():
                    try:
                        up_tp_tups1 = statedic_of_pepdic_raw2[st1][peptide]
                        max_tp1 = max(up_tp_tups1, key=lambda x: x[1])[1]
                        maxD1 = next(x[0] for x in up_tp_tups1 if x[1] == max_tp1)
                    except:
                        maxD1 = -99999
                    try:
                        up_tp_tups2 = statedic_of_pepdic_raw2[st2][peptide]
                        max_tp2 = max(up_tp_tups2, key=lambda x: x[1])[1]
                        maxD2 = next(x[0] for x in up_tp_tups2 if x[1] == max_tp2)
                    except:
                        maxD2 = -99999
                    try:
                        sd_tp_tups1 = statedic_of_sddic_raw2[st1][peptide]
                        max_tp1 = max(sd_tp_tups1, key=lambda x: x[1])[1]
                        maxSD1 = next(x[0] for x in sd_tp_tups1 if x[1] == max_tp1)
                    except:
                        maxSD1 = -99999
                    try:
                        sd_tp_tups2 = statedic_of_sddic_raw2[st2][peptide]
                        max_tp2 = max(sd_tp_tups2, key=lambda x: x[1])[1]
                        maxSD2 = next(x[0] for x in sd_tp_tups2 if x[1] == max_tp2)
                    except:
                        maxSD2 = -99999
                    if maxD1 != -99999:
                        maxd_list.append(maxD1)
                        if maxSD1 != -99999:
                            maxSD_list.append(maxSD1)
                        length = len(peptide)
                        prolinecount=0
                        for letter in peptide:
                            if letter == 'P':
                                prolinecount = prolinecount+1
                        if peptide[0] == 'P':
                            max_theo = length-prolinecount
                        else:
                            max_theo = (length-1)-prolinecount
                        maxtheo_list.append(max_theo)

                    if maxD2 != -99999:
                        maxd_list.append(maxD2)
                        if maxSD1 != -99999:
                            maxSD_list.append(maxSD2)
                        length = len(peptide)
                        prolinecount=0
                        for letter in peptide:
                            if letter == 'P':
                                prolinecount = prolinecount+1
                        if peptide[0] == 'P':
                            max_theo = length-prolinecount
                        else:
                            max_theo = (length-1)-prolinecount
                        maxtheo_list.append(max_theo)
                    if maxD1 == -99999 and maxD2 == -99999:
                        noD_dic_peptides[peptide] = True
                noD_dic_states[state] = noD_dic_peptides
                if len(maxd_list) != 0:
                    total_uptake = sum(maxd_list)
                    total_theo = sum(maxtheo_list)
                    average_rfu = (total_uptake / total_theo)
                    sd_array_squared = np.asarray(maxSD_list) ** 2
                    sd_comb = (np.sqrt(np.sum(sd_array_squared)))/len(maxSD_list)
                    average_rfu_sd_percent = sd_comb / (total_uptake/len(maxd_list))
                    average_rfu_sd = average_rfu_sd_percent * average_rfu
                else:
                    average_rfu = 1
                    average_rfu_sd = 0


                for peptide, upt_tp_tups in pepdic_raw2.items():
                    if peptide in peplist[st1]:
                        if peptide in peplist[st2]:
                            up_tp_tups1 = statedic_of_pepdic_raw2[st1][peptide]
                            up_tp_tups2 = statedic_of_pepdic_raw2[st2][peptide]
                            sd_tp_tups1 = statedic_of_sddic_raw2[st1][peptide]
                            sd_tp_tups2 = statedic_of_sddic_raw2[st2][peptide]
                            max_tp_1 = max(up_tp_tups1, key=lambda x: x[1])[1]
                            maxD_1 = next(x[0] for x in up_tp_tups1 if x[1] == max_tp_1)
                            max_tp_2 = max(up_tp_tups2, key=lambda x: x[1])[1]
                            maxD_2 = next(x[0] for x in up_tp_tups2 if x[1] == max_tp_2)
                            max_tp_sd1 = max(sd_tp_tups1, key=lambda x: x[1])[1]
                            maxSD_1 = next(x[0] for x in sd_tp_tups1 if x[1] == max_tp_sd1)
                            max_tp_sd2 = max(sd_tp_tups2, key=lambda x: x[1])[1]
                            maxSD_2 = next(x[0] for x in sd_tp_tups2 if x[1] == max_tp_sd2)

                            if maxD_1 != -99999 and maxD_2 != -99999:
                                maxD = (maxD_1 + maxD_2)/2
                                if maxSD_1 != -99999 and maxSD_2 != -99999:
                                    maxSD = (np.sqrt(((maxSD_1) ** 2) + ((maxSD_2) ** 2)))/2
                                elif maxSD_1 != -99999:
                                    maxSD = maxSD_1
                                elif maxSD_2 != -99999:
                                    maxSD = maxSD_2
                                else:
                                    maxSD = -99999
                            elif maxD_1 != -99999:
                                maxD = maxD_1
                                if maxSD_1 != -99999:
                                    maxSD = maxSD_1
                                else:
                                    maxSD = -99999
                            elif maxD_2 != -99999:
                                maxD = maxD_2
                                if maxSD_2 != -99999:
                                    maxSD = maxSD_2
                                else:
                                    maxSD = -99999
                            else:
                                length = len(peptide)
                                prolinecount=0
                                for letter in peptide:
                                    if letter == 'P':
                                        prolinecount = prolinecount+1
                                if peptide[0] == 'P':
                                    maxD_i = length-prolinecount
                                else:
                                    maxD_i = (length-1)-prolinecount
                                maxD = maxD_i * average_rfu
                                maxSD = (float(average_rfu_sd) / float(average_rfu)) * maxD

                        else:
                            up_tp_tups1 = statedic_of_pepdic_raw2[st1][peptide]
                            max_tp_1 = max(up_tp_tups1, key=lambda x: x[1])[1]
                            maxD = next(x[0] for x in up_tp_tups1 if x[1] == max_tp_1)
                            sd_tp_tups1 = statedic_of_sddic_raw2[st1][peptide]
                            max_tp_sd1 = max(sd_tp_tups1, key=lambda x: x[1])[1]
                            maxSD_1 = next(x[0] for x in sd_tp_tups1 if x[1] == max_tp_sd1)
                            if maxD == -99999:
                                length = len(peptide)
                                prolinecount=0
                                for letter in peptide:
                                    if letter == 'P':
                                        prolinecount = prolinecount+1
                                if peptide[0] == 'P':
                                    maxD_i = length-prolinecount
                                else:
                                    maxD_i = (length-1)-prolinecount
                                maxD = maxD_i * average_rfu
                                maxSD = (float(average_rfu_sd) / float(average_rfu)) * maxD
                            else:
                                maxSD = maxSD_1
                        Dcorrected_tups = list()
                        Dcorrected_sd_tups = list()
                        sd_tp_tups = statedic_of_sddic_raw2[state][peptide]
                        for uptake, timepoint in upt_tp_tups:
                            if uptake != -99999:
                                Dcorrected = (float(uptake) / float(maxD))
                                for sd, tp in sd_tp_tups:
                                    if tp == timepoint:
                                        uptake_SD = float(sd)
                                        break
                                if uptake_SD != -99999 and uptake != 0 and maxSD != -99999:
                                    Dcorrected_SD_percent = np.sqrt((((uptake_SD)/(float(uptake))) ** 2) + (((maxSD)/(float(maxD))) ** 2))
                                    Dcorrected_SD = Dcorrected_SD_percent * Dcorrected
                                else:
                                    Dcorrected_SD = -99999
                            else:
                                Dcorrected = -99999
                                Dcorrected_SD = -99999
                            Dcorrected_tups.append((Dcorrected, timepoint))
                            Dcorrected_sd_tups.append((Dcorrected_SD, timepoint))
                        pepdic_cor[peptide] = Dcorrected_tups
                        sddic_cor[peptide] = Dcorrected_sd_tups

                    if peptide in peplist[st2]:
                        if peptide not in peplist[st1]:
                            up_tp_tups2 = statedic_of_pepdic_raw2[st2][peptide]
                            max_tp_2 = max(up_tp_tups2, key=lambda x: x[1])[1]
                            maxD = next(x[0] for x in up_tp_tups2 if x[1] == max_tp_2)
                            sd_tp_tups2 = statedic_of_sddic_raw2[st2][peptide]
                            max_tp_sd2 = max(sd_tp_tups2, key=lambda x: x[1])[1]
                            maxSD_2 = next(x[0] for x in sd_tp_tups2 if x[1] == max_tp_sd2)
                            if maxD == -99999:
                                length = len(peptide)
                                prolinecount=0
                                for letter in peptide:
                                    if letter == 'P':
                                        prolinecount = prolinecount+1
                                if peptide[0] == 'P':
                                    maxD_i = length-prolinecount
                                else:
                                    maxD_i = (length-1)-prolinecount
                                maxD = maxD_i * average_rfu
                                maxSD = (float(average_rfu_sd) / float(average_rfu)) * maxD
                            else:
                                maxSD = maxSD_2
                            Dcorrected_tups = list()
                            Dcorrected_sd_tups = list()
                            sd_tp_tups = statedic_of_sddic_raw2[state][peptide]
                            for uptake, timepoint in upt_tp_tups:
                                if uptake != -99999:
                                    Dcorrected = (float(uptake) / float(maxD))
                                    for sd, tp in sd_tp_tups:
                                        if tp == timepoint:
                                            uptake_SD = float(sd)
                                            break
                                    if uptake_SD != -99999 and uptake != 0 and maxSD != -99999:
                                        Dcorrected_SD_percent = np.sqrt((((uptake_SD)/(float(uptake))) ** 2) + (((maxSD)/(float(maxD))) ** 2))
                                        Dcorrected_SD = Dcorrected_SD_percent * Dcorrected
                                    else:
                                        Dcorrected_SD = -99999
                                else:
                                    Dcorrected = -99999
                                    Dcorrected_SD = -99999
                                Dcorrected_tups.append((Dcorrected, timepoint))
                                Dcorrected_sd_tups.append((Dcorrected_SD, timepoint))
                            pepdic_cor[peptide] = Dcorrected_tups
                            sddic_cor[peptide] = Dcorrected_sd_tups
                    if peptide not in peplist[st1] and peptide not in peplist[st2]:
                        length = len(peptide)
                        prolinecount=0
                        for letter in peptide:
                            if letter == 'P':
                                prolinecount = prolinecount+1
                        if peptide[0] == 'P':
                            maxD_i = length-prolinecount
                        else:
                            maxD_i = (length-1)-prolinecount
                        maxD = maxD_i * average_rfu
                        maxSD = (float(average_rfu_sd) / float(average_rfu)) * maxD
                        Dcorrected_tups = list()
                        Dcorrected_sd_tups = list()
                        sd_tp_tups = statedic_of_sddic_raw2[state][peptide]
                        for uptake, timepoint in upt_tp_tups:
                            if uptake != -99999:
                                Dcorrected = (float(uptake) / float(maxD))
                                for sd, tp in sd_tp_tups:
                                    if tp == timepoint:
                                        uptake_SD = float(sd)
                                        break
                                if uptake_SD != -99999 and uptake != 0 and maxSD != -99999:
                                    Dcorrected_SD_percent = np.sqrt((((uptake_SD)/(float(uptake))) ** 2) + (((maxSD)/(float(maxD))) ** 2))
                                    Dcorrected_SD = Dcorrected_SD_percent * Dcorrected
                                else:
                                    Dcorrected_SD = -99999
                            else:
                                Dcorrected = -99999
                                Dcorrected_SD = -99999
                            Dcorrected_tups.append((Dcorrected, timepoint))
                            Dcorrected_sd_tups.append((Dcorrected_SD, timepoint))
                        pepdic_cor[peptide] = Dcorrected_tups
                        sddic_cor[peptide] = Dcorrected_sd_tups


                statedic_of_pepdic_cor[state] = pepdic_cor
                statedic_of_sddic_cor[state] = sddic_cor


    if theo_bt_on_c == True:
        be = be_entry.get()
        try:
            back_exchange = float(be)
        except:
            back_exchange = 0
            be_label = tk.Label(window, text="Invalid Back Exchange. Defaulted to 0")
            be_label.place(x=30, y=400)
        for state, pepdic_raw2 in statedic_of_pepdic_raw2.items():
            pepdic_cor = {}
            sddic_cor = {}
            for peptide, upt_tp_tups in pepdic_raw2.items():
                length = len(peptide)
                prolinecount=0
                for letter in peptide:
                    if letter == 'P':
                        prolinecount = prolinecount+1
                if peptide[0] == 'P':
                    maxD = length-prolinecount
                else:
                    maxD = (length-1)-prolinecount
                be_maxD = maxD * ((100-back_exchange)/100)
                Dcorrected_tups = list()
                Dcorrected_SD_tups = list()
                sd_tp_tups = statedic_of_sddic_raw2[state][peptide]
                for uptake, timepoint in upt_tp_tups:
                    if uptake != -99999:
                        Dcorrected = (float(uptake) / float(be_maxD))
                        for sd, tp in sd_tp_tups:
                            if tp == timepoint:
                                uptake_SD = float(sd)
                                break
                        if uptake_SD != -99999 and uptake != 0:
                            Dcorrected_SD = (uptake_SD/float(uptake)) * Dcorrected
                        else:
                            Dcorrected_SD = -99999
                    else:
                        Dcorrected = -99999
                        Dcorrected_SD = -99999
                    Dcorrected_tups.append((Dcorrected, timepoint))
                    Dcorrected_SD_tups.append((Dcorrected_SD, timepoint))
                pepdic_cor[peptide] = Dcorrected_tups
                sddic_cor[peptide] = Dcorrected_SD_tups
            statedic_of_pepdic_cor[state] = pepdic_cor
            statedic_of_sddic_cor[state] = sddic_cor



    start_progress()

    global peptide_starts
    global peptide_ends
    peptide_starts = {}

    # loop through each line in data
    for i, line in enumerate(data):
        peptide = line[3]  # get the peptide from the 1st term
        start_val = int(line[1])  # get the start value from the 2nd term
        if peptide not in peptide_starts:
            peptide_starts[peptide] = [start_val]  # create a new list with the start value


    peptide_ends = {}

    # loop through each line in data
    for i, line in enumerate(data):
        peptide = line[3]  # get the peptide from the 1st term
        end_val = int(line[2])  # get the end value from the 2nd term
        if peptide not in peptide_ends:
            peptide_ends[peptide] = [end_val]  # create a new list with the end value

    try:
        global seqlist_dic
        beginnings = {}
        seqlist_dic = {}
        seqlist_dic_proteins = {}


        if seqbt_txt_clicked == True:
            seqlist = list()
            for line in seq:
                line = line.rstrip()
                for r in line:
                    seqlist.append(r)
            for state in states:
                seqlist_dic[state] = seqlist
        if seqbt_fasta_clicked or txt_h_bt_clicked:
            if len(prot_seq_dic) == 1:
                for protein, s in prot_seq_dic.items():
                    seqlist = list()
                    line = s.strip()
                    for r in line:
                        seqlist.append(r)
                    for state in states:
                        seqlist_dic[state] = seqlist
            if len(prot_seq_dic) >= 2:
                for protein, s in prot_seq_dic.items():
                    seqlist = list()
                    for line in s:
                        line = line.strip()
                        for r in line:
                            seqlist.append(r)
                    seqlist_dic_proteins[protein] = seqlist
                seqlist_dic = {}
                for protein, sequence in seqlist_dic_proteins.items():
                    for state in states:
                        if state.startswith(protein):
                            seqlist_dic[state] = sequence
            for state in states:
                if state not in seqlist_dic:
                    peptide_start_list = list()
                    peptide_end_list = list()
                    for peptide, start in peptide_starts.items():
                        peptide_start_list.append(start)
                    beginning_l = min(peptide_start_list)
                    beginnings[state] = beginning_l[0]
                    for peptide, end in peptide_ends.items():
                        peptide_end_list.append(end)
                    ending_l = max(peptide_end_list)
                    ending = ending_l[0]
                    b_e_range = (ending - beginnings[state]) + 3
                    seqlist = list()
                    x = 0
                    while x <= b_e_range:
                        seqlist.append("A")
                        x += 1
                    seqlist_dic[state] = seqlist


    except:
        if (pepmap_bt_on or difmap_bt_on or condpeps_bt_on or difcond_bt_on) and skip_bt_clicked == False:

            popup_window2 = tk.Toplevel(window)  # Create a new window for the popup menu
            popup_window2.geometry("600x100")

             # Calculate the desired position for the popup window
            x = window.winfo_x() + 400  # Adjust the value as needed
            y = window.winfo_y() + 200  # Adjust the value as needed

            # Set the position of the popup window
            popup_window2.geometry(f"+{x}+{y}")

            noseq_lb = tk.Label(popup_window2, text="There has been an error reading your sequence. Please make sure the file is correctly formatted. Too many spaces in protein name will cause an error")
            noseq_lb.place(x=50, y=50)
    if skip_bt_clicked == True:
        peptide_start_list = list()
        peptide_end_list = list()
        for peptide, start in peptide_starts.items():
            peptide_start_list.append(start)
        beginning_l = min(peptide_start_list)
        beginning = beginning_l[0]
        for peptide, end in peptide_ends.items():
            peptide_end_list.append(end)
        ending_l = max(peptide_end_list)
        ending = ending_l[0]
        b_e_range = (ending - beginning) + 3
        seqlist = list()
        x = 0
        while x <= b_e_range:
            seqlist.append("A")
            x += 1
        for state in states:
            seqlist_dic[state] = seqlist

    global seq_start
    seq_start = {}
    if seqbt_txt_clicked == True:
        sequence = ""
        for res in seqlist:
            sequence = sequence + res
        for state in states:
            for peptide in peplist[state]:
                one_peptide_sequence = peptide
                one_peptide_starts = peptide_starts.get(peptide, None)
                one_peptide_start = int(one_peptide_starts[0])

                if one_peptide_sequence not in sequence:
                    continue
                else:
                    split_sequence = sequence.split(peptide)
                    before_space = split_sequence[0]
                    seq_start[state] = one_peptide_start - len(before_space)
                    break

    if skip_bt_clicked:
        for state in states:
            seq_start[state] = beginning
    if seqbt_fasta_clicked or txt_h_bt_clicked:
        for state in states:
            sequence = ""
            for res in seqlist_dic[state]:
                sequence = sequence + res
            for peptide in peplist[state]:
                one_peptide_sequence = peptide
                one_peptide_starts = peptide_starts.get(peptide, None)
                one_peptide_start = int(one_peptide_starts[0])

                if one_peptide_sequence not in sequence:
                    continue
                else:
                    split_sequence = sequence.split(peptide)
                    before_space = split_sequence[0]
                    seq_start[state] = one_peptide_start - len(before_space)
                    break
    for state in states:
        if state not in seq_start:
            seq_start[state] = beginnings[state]





    global wb
    wb = openpyxl.Workbook()

    r_make_legend1()
    r_make_legend2()
    if chic_bt_on == True:
        r_chiclet()
    if cdif_bt_on == True:
        r_chicdif()
    if pepmap_bt_on == True:
        r_pepmaps()
    if difmap_bt_on == True:
        r_difmaps()
    if condpeps_bt_on == True:
        r_condpeps()
    if difcond_bt_on == True:
        r_difcond()
    save_wb()

def r_make_legend1():
    ws = wb.create_sheet(title="Figure Legends")
    fig, ax = plt.subplots()
    xpos = uptake_color_length + 1
    if uptake_color_length >= 1:
        color = assign_hex(uptake_col_1)
        square_1 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_1 * 100), ha='center', va='bottom', fontsize=12)
        ax.plot([xpos + 1, xpos + 1], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos + 1, 1.35, "100", ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_1)
    if uptake_color_length >= 2:
        color = assign_hex(uptake_col_2)
        square_2 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_2 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_2)
    if uptake_color_length >= 3:
        color = assign_hex(uptake_col_3)
        square_3 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_3 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_3)
    if uptake_color_length >= 4:
        color = assign_hex(uptake_col_4)
        square_4 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_4 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_4)
    if uptake_color_length >= 5:
        color = assign_hex(uptake_col_5)
        square_5 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_5 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_5)
    if uptake_color_length >= 6:
        color = assign_hex(uptake_col_6)
        square_6 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_6 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_6)
    if uptake_color_length >= 7:
        color = assign_hex(uptake_col_7)
        square_7 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_7 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_7)
    if uptake_color_length >= 8:
        color = assign_hex(uptake_col_8)
        square_8 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_8 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_8)
    if uptake_color_length >= 9:
        color = assign_hex(uptake_col_9)
        square_9 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        ax.text(xpos, 1.35, round(uptake_val_9 * 100), ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_9)
    color = assign_hex(uptake_gtz_key)
    square_10 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
    ax.text(xpos, 1.35, "0", ha='center', va='bottom', fontsize=12)
    ax.add_patch(square_10)

    color = assign_hex(uptake_abs_key)
    square_11 = patches.Rectangle((xpos, -1.5), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(square_11)
    ax.text(xpos + 2, -1.25, " No Data", ha='center', va='bottom', fontsize=14)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, uptake_color_length + 3.5)
    ax.set_ylim(-3, 2.5)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.savefig('./RecentLegends/uptakelegend.png', dpi=300)
    plt.close()
    img = openpyxl.drawing.image.Image('./RecentLegends/uptakelegend.png')
    img.anchor = 'A1'
    ws.add_image(img)

def r_make_legend2():
    fig, ax = plt.subplots()
    xpos = p_col_length + d_col_length + 1
    if d_col_length >= 1:
        color = assign_hex(d_col_1)
        square_1 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        if exp_bt_on_c:
            ax.text(xpos, 1.35, round(d_val_1 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos, 1.35, d_val_1, ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_1)
    if d_col_length >= 2:
        color = assign_hex(d_col_2)
        square_2 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        if exp_bt_on_c:
            ax.text(xpos, 1.35, round(d_val_2 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos, 1.35, d_val_2, ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_2)
    if d_col_length >= 3:
        color = assign_hex(d_col_3)
        square_3 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        if exp_bt_on_c:
            ax.text(xpos, 1.35, round(d_val_3 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos, 1.35, d_val_3, ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_3)
    if d_col_length >= 4:
        color = assign_hex(d_col_4)
        square_4 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        if exp_bt_on_c:
            ax.text(xpos, 1.35, round(d_val_4 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos, 1.35, d_val_4, ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_4)
    if d_col_length >= 5:
        color = assign_hex(d_col_5)
        square_5 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        if exp_bt_on_c:
            ax.text(xpos, 1.35, round(d_val_5 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos, 1.35, d_val_5, ha='center', va='bottom', fontsize=12)
        xpos -= 1
        ax.add_patch(square_5)
    color = assign_hex(d_col_gtz)
    square_6 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
    ax.text(xpos, 1.35, "0", ha='center', va='bottom', fontsize=12)
    xpos -= 1
    ax.add_patch(square_6)
    color = assign_hex(p_col_gtz)
    square_7 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
    xpos -= 1
    ax.add_patch(square_7)
    if p_col_length >= 5:
        if exp_bt_on_c:
            ax.text(xpos + 1, 1.35, round(p_val_5 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos + 1, 1.35, p_val_5, ha='center', va='bottom', fontsize=12)
        color = assign_hex(p_col_5)
        square_8 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        xpos -= 1
        ax.add_patch(square_8)
    if p_col_length >= 4:
        if exp_bt_on_c:
            ax.text(xpos + 1, 1.35, round(p_val_4 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos + 1, 1.35, p_val_4, ha='center', va='bottom', fontsize=12)
        color = assign_hex(p_col_4)
        square_9 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        xpos -= 1
        ax.add_patch(square_9)
    if p_col_length >= 3:
        if exp_bt_on_c:
            ax.text(xpos + 1, 1.35, round(p_val_3 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos + 1, 1.35, p_val_3, ha='center', va='bottom', fontsize=12)
        color = assign_hex(p_col_3)
        square_10 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        xpos -= 1
        ax.add_patch(square_10)
    if p_col_length >= 2:
        if exp_bt_on_c:
            ax.text(xpos + 1, 1.35, round(p_val_2 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos + 1, 1.35, p_val_2, ha='center', va='bottom', fontsize=12)
        color = assign_hex(p_col_2)
        square_11 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.plot([xpos, xpos], [1, 1.3], color='black', linewidth=1)
        xpos -= 1
        ax.add_patch(square_11)
    if p_col_length >= 1:
        if exp_bt_on_c:
            ax.text(xpos + 1, 1.35, round(p_val_1 * 100), ha='center', va='bottom', fontsize=12)
        else:
            ax.text(xpos + 1, 1.35, p_val_1, ha='center', va='bottom', fontsize=12)
        color = assign_hex(p_col_1)
        square_12 = patches.Rectangle((xpos, 0), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(square_12)

    color = assign_hex(b_col_abs)
    square_13 = patches.Rectangle((xpos, -1.5), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(square_13)
    ax.text(xpos + 3, -1.25, " No Data", ha='center', va='bottom', fontsize=14)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, p_col_length + d_col_length + 3.5)
    ax.set_ylim(-3, 2.5)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.savefig('./RecentLegends/differencelegend.png', dpi=300)
    plt.close()
    ws = wb['Figure Legends']
    img = openpyxl.drawing.image.Image('./RecentLegends/differencelegend.png')
    img.anchor = 'A80'
    ws.add_image(img)




def assign_hex(col):
    color = "#" + col
    return color



def r_pepmaps():
    for state in statedic_of_pepdic_cor:
        sorted_peptides = sorted(peplist[state], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        ws_title = (f"{state}".replace(":", ";"))[-30:]
        ws = wb.create_sheet(title=ws_title)
        ws.append([" "])
        ws.append([" "] + seqlist_dic[state] + [" "])
        timepoint_number = 0
        for timepoint in s_timepoints[state]:
            if timepoint_number == 0:
                startrow = 3
                endrow = 250
            if timepoint_number != 0:
                startrow = ws.max_row +5
                endrow = ws.max_row + 250
            for peptide in sorted_peptides:
                startvalues = peptide_starts.get(peptide, None)
                startvalue= int(startvalues[0]) - seq_start[state]
                endvalues = peptide_ends.get(peptide, None)
                endvalue = int(endvalues[0]) - seq_start[state]
                peptide_length = len(peptide)
                Cuptake = None
                try:
                    for up, tp in statedic_of_pepdic_cor[state][peptide]:
                        if tp == timepoint:
                            Cuptake = up
                except:
                    pass
                if Cuptake is not None:
                    for row in ws.iter_rows(min_row=startrow, max_row=startrow):
                        row[0].value = timepoint
                    for row in ws.iter_rows(min_row=startrow,max_row=endrow):
                        cells = row[startvalue + 1:endvalue + 2]
                        if all(cell.value is None for cell in cells):
                            row[startvalue + 1].value = Cuptake
                            row[startvalue + 1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                     bottom=Side(border_style='thin', color='FF000000'),
                                     left=Side(border_style='thin', color='FF000000'))
                            row[endvalue+1].value = Cuptake
                            row[endvalue+1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                     bottom=Side(border_style='thin', color='FF000000'),
                                     right=Side(border_style='thin', color='FF000000'))
                            for cell in row[startvalue + 2:endvalue+1]:
                                cell.value = Cuptake
                                cell.border = Border(top=Side(border_style='thin', color='FF000000'),
                                     bottom=Side(border_style='thin', color='FF000000'))

                            try:
                                if peptide in noD_dic_states[state]:
                                    if Cuptake != 0 and Cuptake != -99999:
                                        row[startvalue+1].value = "*"
                                        #row[startvalue+1].alignment = Alignment(textRotation=90, vertical='center')
                                        if uptake_color_length >= 1 and Cuptake > uptake_val_1:
                                            fill = PatternFill(start_color=uptake_col_1, end_color=uptake_col_1, fill_type='solid')
                                            font = Font(color=uptake_text_1, size=16)
                                        elif uptake_color_length >= 2 and Cuptake > uptake_val_2:
                                            fill = PatternFill(start_color=uptake_col_2, end_color=uptake_col_2, fill_type='solid')
                                            font = Font(color=uptake_text_2, size=16)
                                        elif uptake_color_length >= 3 and Cuptake > uptake_val_3:
                                            fill = PatternFill(start_color=uptake_col_3, end_color=uptake_col_3, fill_type='solid')
                                            font = Font(color=uptake_text_3, size=16)
                                        elif uptake_color_length >= 4 and Cuptake > uptake_val_4:
                                            fill = PatternFill(start_color=uptake_col_4, end_color=uptake_col_4, fill_type='solid')
                                            font = Font(color=uptake_text_4, size=16)
                                        elif uptake_color_length >= 5 and Cuptake > uptake_val_5:
                                            fill = PatternFill(start_color=uptake_col_5, end_color=uptake_col_5, fill_type='solid')
                                            font = Font(color=uptake_text_5, size=16)
                                        elif uptake_color_length >= 6 and Cuptake > uptake_val_6:
                                            fill = PatternFill(start_color=uptake_col_6, end_color=uptake_col_6, fill_type='solid')
                                            font = Font(color=uptake_text_6, size=16)
                                        elif uptake_color_length >= 7 and Cuptake > uptake_val_7:
                                            fill = PatternFill(start_color=uptake_col_7, end_color=uptake_col_7, fill_type='solid')
                                            font = Font(color=uptake_text_7, size=16)
                                        elif uptake_color_length >= 8 and Cuptake > uptake_val_8:
                                            fill = PatternFill(start_color=uptake_col_8, end_color=uptake_col_8, fill_type='solid')
                                            font = Font(color=uptake_text_8, size=16)
                                        elif uptake_color_length >= 9 and Cuptake > uptake_val_9:
                                            fill = PatternFill(start_color=uptake_col_9, end_color=uptake_col_9, fill_type='solid')
                                            font = Font(color=uptake_text_9, size=16)
                                        elif Cuptake > 0.0:
                                            fill = PatternFill(start_color=uptake_gtz_key, end_color=uptake_gtz_key, fill_type='solid')
                                            font = Font(color=uptake_gtz_text, size=16)
                                        elif Cuptake == 0:
                                            fill = PatternFill(start_color=uptake_eqz_key, end_color=uptake_eqz_key, fill_type='solid')
                                            font = Font(color=uptake_eqz_text, size=16)
                                            cell.number_format = ';;;'
                                        elif Cuptake == -99999:
                                            fill = PatternFill(start_color=uptake_abs_key, end_color=uptake_abs_key, fill_type='solid')
                                            font = Font(color=uptake_abs_text, size=16)
                                            cell.number_format = ';;;'
                                        elif Cuptake < 0.0:
                                            fill = PatternFill(start_color=uptake_ltz_key, end_color=uptake_ltz_key, fill_type='solid')
                                            font = Font(color=uptake_ltz_text, size=16)
                                        row[startvalue+1].fill = fill
                                        row[startvalue+1].font = font
                            except:
                                pass







                            break
                        else:
                            continue



            timepoint_number = timepoint_number + 1





        white_fill = PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", fill_type='solid')
        for row in ws.rows:
            for cell in row:
                if cell.value != "*":
                    cell.fill = white_fill



        for i, column in enumerate(ws.columns):
            if i == 0:
                continue
            ws.column_dimensions[column[0].column_letter].width = full_pep_width_enter.get()



        for row in ws.iter_rows(min_row=3):
            for cell in row[1:]:
                cell_v = cell.value
                if cell_v != "*":
                    if uptake_color_length >= 1 and cell_v is not None and cell_v > uptake_val_1:
                        fill = PatternFill(start_color=uptake_col_1, end_color=uptake_col_1, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 2 and cell_v is not None and cell_v > uptake_val_2:
                        fill = PatternFill(start_color=uptake_col_2, end_color=uptake_col_2, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 3 and cell_v is not None and cell_v > uptake_val_3:
                        fill = PatternFill(start_color=uptake_col_3, end_color=uptake_col_3, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 4 and cell_v is not None and cell_v > uptake_val_4:
                        fill = PatternFill(start_color=uptake_col_4, end_color=uptake_col_4, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 5 and cell_v is not None and cell_v > uptake_val_5:
                        fill = PatternFill(start_color=uptake_col_5, end_color=uptake_col_5, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 6 and cell_v is not None and cell_v > uptake_val_6:
                        fill = PatternFill(start_color=uptake_col_6, end_color=uptake_col_6, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 7 and cell_v is not None and cell_v > uptake_val_7:
                        fill = PatternFill(start_color=uptake_col_7, end_color=uptake_col_7, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 8 and cell_v is not None and cell_v > uptake_val_8:
                        fill = PatternFill(start_color=uptake_col_8, end_color=uptake_col_8, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 9 and cell_v is not None and cell_v > uptake_val_9:
                        fill = PatternFill(start_color=uptake_col_9, end_color=uptake_col_9, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v > 0.0:
                        fill = PatternFill(start_color=uptake_gtz_key, end_color=uptake_gtz_key, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v == 0:
                        fill = PatternFill(start_color=uptake_eqz_key, end_color=uptake_eqz_key, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v == -99999:
                        fill = PatternFill(start_color=uptake_abs_key, end_color=uptake_abs_key, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v < 0.0:
                        fill = PatternFill(start_color=uptake_ltz_key, end_color=uptake_ltz_key, fill_type='solid')
                        cell.number_format = ';;;'
                    if cell_v is not None:
                        cell.fill = fill


        increase_progress(1)

        for row in ws.iter_rows(min_row=1, max_row=1):
            num = seq_start[state]
            for cell in row:
                if cell.column >= 2 and cell.column < ws.max_column:
                    cell.value = num
                    num = num+1

        for row in ws.iter_rows(max_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal='center')

def r_difmaps():



    for stt, pair in  new_dic_of_dif_list.items():
        first = pair[0]
        second = pair[1]
        sorted_peptides_first = sorted(peplist[first], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        sorted_peptides_second = sorted(peplist[second], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        difname = f"{stt}"
        wtit = (f"{difname}")[:30]
        ws = wb.create_sheet(title=wtit)
        ws.append([" "])
        ws.append([" "] + seqlist_dic[first] + [" "])
        timepoint_number = 0
        for timepoint in s_timepoints[first]:
            if timepoint in s_timepoints[second]:
                if timepoint_number == 0:
                    startrow = 3
                    endrow = 250
                if timepoint_number != 0:
                    startrow = ws.max_row +5
                    endrow = ws.max_row + 250
                for peptide in sorted_peptides_first:
                    startvalues = peptide_starts.get(peptide, None)
                    startvalue= int(startvalues[0]) - seq_start[first]
                    endvalues = peptide_ends.get(peptide, None)
                    endvalue = int(endvalues[0]) - seq_start[first]
                    peptide_length = len(peptide)
                    if exp_bt_on_c == True:
                        up1 = None
                        up2 = None
                        diftake = None

                        try:
                            for up, tp in statedic_of_pepdic_cor[first][peptide]:
                                if tp == timepoint:
                                    up1 = up
                            for up, tp in statedic_of_pepdic_cor[second][peptide]:
                                if tp == timepoint:
                                    up2 = up
                            if up1 is not None and up2 is not None and up1 != -99999 and up2 != -99999:
                                diftake = up1 - up2
                            elif up1 is not None and up2 is not None:
                                diftake = -99999

                        except:
                            pass

                    if theo_bt_on_c == True:
                        up1 = None
                        up2 = None
                        diftake = None
                        try:
                            for up, tp in statedic_of_pepdic_raw2[first][peptide]:
                                if tp == timepoint:
                                    up1 = up
                            for up, tp in statedic_of_pepdic_raw2[second][peptide]:
                                if tp == timepoint:
                                    up2 = up
                            if up1 is not None and up2 is not None and up1 != -99999 and up2 != -99999:
                                diftake = up1 - up2
                            elif up1 is not None and up2 is not None:
                                diftake = -99999
                        except:
                            pass
                    if diftake is not None:
                        for row in ws.iter_rows(min_row=startrow, max_row=startrow):
                            row[0].value = timepoint
                        for row in ws.iter_rows(min_row=startrow,max_row=endrow):
                            cells = row[startvalue + 1:endvalue + 2]
                            if all(cell.value is None for cell in cells):
                                row[startvalue + 1].value = diftake
                                row[startvalue + 1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                         bottom=Side(border_style='thin', color='FF000000'),
                                         left=Side(border_style='thin', color='FF000000'))
                                row[endvalue+1].value = diftake
                                row[endvalue+1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                         bottom=Side(border_style='thin', color='FF000000'),
                                         right=Side(border_style='thin', color='FF000000'))
                                for cell in row[startvalue + 2:endvalue+1]:
                                    cell.value = diftake
                                    cell.border = Border(top=Side(border_style='thin', color='FF000000'),
                                         bottom=Side(border_style='thin', color='FF000000'))
                                ch1 = False
                                ch2 = False
                                try:
                                    if noD_dic_states[first][peptide] == True:
                                        ch1 = True
                                except:
                                    pass
                                try:
                                    if noD_dic_states[second][peptide] == True:
                                        ch2 = True
                                except:
                                    pass

                                if ch1 == True or ch2 == True:
                                    if diftake != 0 and diftake != -99999:
                                        row[startvalue+1].value = "*"
                                        row[startvalue+1].alignment = Alignment(textRotation=90, vertical='center')

                                        if d_col_length >= 1 and diftake >= d_val_1:
                                            fill = PatternFill(start_color=d_col_1, end_color=d_col_1, fill_type='solid')
                                            font = Font(color=d_text_1, size=16)
                                        elif d_col_length >= 2 and diftake >= d_val_2:
                                            fill = PatternFill(start_color=d_col_2, end_color=d_col_2, fill_type='solid')
                                            font = Font(color=d_text_2, size=16)
                                        elif d_col_length >= 3 and diftake >= d_val_3:
                                            fill = PatternFill(start_color=d_col_3, end_color=d_col_3, fill_type='solid')
                                            font = Font(color=d_text_3, size=16)
                                        elif d_col_length >= 4 and diftake >= d_val_4:
                                            fill = PatternFill(start_color=d_col_4, end_color=d_col_4, fill_type='solid')
                                            font = Font(color=d_text_4, size=16)
                                        elif d_col_length >= 5 and diftake >= d_val_5:
                                            fill = PatternFill(start_color=d_col_5, end_color=d_col_5, fill_type='solid')
                                            font = Font(color=d_text_5, size=16)
                                        elif diftake > 0:
                                            fill = PatternFill(start_color=d_col_gtz, end_color=d_col_gtz, fill_type='solid')
                                            font = Font(color=d_text_gtz, size=16)
                                        elif p_col_length >= 1 and diftake <= (-1) * p_val_1:
                                            fill = PatternFill(start_color=p_col_1, end_color=p_col_1, fill_type='solid')
                                            font = Font(color=p_text_1, size=16)
                                        elif p_col_length >= 2 and diftake <= (-1) * p_val_2:
                                            fill = PatternFill(start_color=p_col_2, end_color=p_col_2, fill_type='solid')
                                            font = Font(color=p_text_2, size=16)
                                        elif p_col_length >= 3 and diftake <= (-1) * p_val_3:
                                            fill = PatternFill(start_color=p_col_3, end_color=p_col_3, fill_type='solid')
                                            font = Font(color=p_text_3, size=16)
                                        elif p_col_length >= 4 and diftake <= (-1) * p_val_4:
                                            fill = PatternFill(start_color=p_col_4, end_color=p_col_4, fill_type='solid')
                                            font = Font(color=p_text_4, size=16)
                                        elif p_col_length >= 5 and diftake <= (-1) * p_val_5:
                                            fill = PatternFill(start_color=p_col_5, end_color=p_col_5, fill_type='solid')
                                            font = Font(color=p_text_5, size=16)
                                        elif diftake < 0:
                                            fill = PatternFill(start_color=p_col_gtz, end_color=p_col_gtz, fill_type='solid')
                                            font = Font(color=p_text_gtz, size=16)

                                        row[startvalue+1].fill = fill
                                        row[startvalue+1].font = font




                                break
                            else:
                                continue





                timepoint_number = timepoint_number + 1
        increase_progress(1.5)





        white_fill = PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", fill_type='solid')
        for row in ws.rows:
            for cell in row:
                if cell.value != "*":
                    cell.fill = white_fill



        for i, column in enumerate(ws.columns):
            if i == 0:
                continue
            ws.column_dimensions[column[0].column_letter].width = full_pep_width_enter.get()




        for row in ws.iter_rows(min_row=1, max_row=1):
            num = seq_start[first]
            for cell in row:
                if cell.column >= 2 and cell.column < ws.max_column:
                    cell.value = num
                    num = num+1

        for row in ws.iter_rows(min_row=3):
            for cell in row[1:]:
                cell_v = cell.value
                if cell_v != "*":
                    if cell_v == -99999:
                        fill = PatternFill(start_color=b_col_abs, end_color=b_col_abs, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 1 and cell_v is not None and cell_v >= d_val_1:
                        fill = PatternFill(start_color=d_col_1, end_color=d_col_1, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 2 and cell_v is not None and cell_v >= d_val_2:
                        fill = PatternFill(start_color=d_col_2, end_color=d_col_2, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 3 and cell_v is not None and cell_v >= d_val_3:
                        fill = PatternFill(start_color=d_col_3, end_color=d_col_3, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 4 and cell_v is not None and cell_v >= d_val_4:
                        fill = PatternFill(start_color=d_col_4, end_color=d_col_4, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 5 and cell_v is not None and cell_v >= d_val_5:
                        fill = PatternFill(start_color=d_col_5, end_color=d_col_5, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v > 0:
                        fill = PatternFill(start_color=d_col_gtz, end_color=d_col_gtz, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >= 1 and cell_v is not None and cell_v <= (-1) * p_val_1:
                        fill = PatternFill(start_color=p_col_1, end_color=p_col_1, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >= 2 and cell_v is not None and cell_v <= (-1) * p_val_2:
                        fill = PatternFill(start_color=p_col_2, end_color=p_col_2, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >= 3 and cell_v is not None and cell_v <= (-1) * p_val_3:
                        fill = PatternFill(start_color=p_col_3, end_color=p_col_3, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >= 4 and cell_v is not None and cell_v <= (-1) * p_val_4:
                        fill = PatternFill(start_color=p_col_4, end_color=p_col_4, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >= 5 and cell_v is not None and cell_v <= (-1) * p_val_5:
                        fill = PatternFill(start_color=p_col_5, end_color=p_col_5, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v < 0:
                        fill = PatternFill(start_color=p_col_gtz, end_color=p_col_gtz, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v == 0:
                        fill = PatternFill(start_color=b_col_eqz, end_color=b_col_eqz, fill_type='solid')
                        cell.number_format = ';;;'
                    if cell_v is not None:
                        cell.fill = fill




    for sheet in wb:
        for row in sheet.iter_rows(max_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal='center')



    increase_progress(1)


def r_chiclet():
    ws = wb.create_sheet("Chiclets")
    plot_number = 0
    for state in states:
        if plot_number == 0:
            plot_start = 1
            plot_end = 50
        if plot_number > 0:
            plot_start = ws.max_column + 3
            plot_end = ws.max_column + 50
        ws.cell(row=1, column=plot_start, value=state)
        ws.cell(row=2, column=plot_start, value = "Sequence")
        ws.cell(row=2, column=plot_start+1, value = "Start")
        ws.cell(row=2, column=plot_start+2, value = "End")
        tpnum = 0
        for timepoint in s_timepoints[state]:
            if timepoint == 0:
                tpnum = tpnum + 1
                continue
            ws.cell(row=2, column=plot_start+3+tpnum, value = s_timepoints[state][tpnum])
            tpnum = tpnum + 1

        if sort_var.get() == 1:
            sorted_peptides = sorted(peplist[state], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        else:
            sorted_peptides = peplist[state]

        pepnum = 0
        for peptide in sorted_peptides:
            startvalues = peptide_starts.get(peptide, None)
            startvalue= int(startvalues[0])
            endvalues = peptide_ends.get(peptide, None)
            endvalue = int(endvalues[0])

            ws.cell(row=3+pepnum, column=plot_start, value = peptide)
            ws.cell(row=3+pepnum, column=plot_start+1, value = startvalue)
            ws.cell(row=3+pepnum, column=plot_start+2, value = endvalue)
            tnum = 0
            for timepoint in s_timepoints[state]:
                if timepoint == 0:
                    tnum = tnum + 1
                    continue
                ws.cell(row=3+pepnum, column=plot_start+3+tnum, value=statedic_of_pepdic_cor[state][peptide][tnum][0])
                tnum = tnum + 1
            try:
                if noD_dic_states[state][peptide] == True:
                    ws.cell(row=3+pepnum, column=plot_start+3+tnum, value="*")
            except:
                pass
            pepnum = pepnum + 1
        ws.column_dimensions[get_column_letter(plot_start)].width = 30
        plot_number = plot_number + 1






    white_fill = PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", fill_type='solid')
    for row in ws.rows:
        for cell in row:
            cell.fill = white_fill
    for row in ws.iter_rows(max_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal='center')

    for col in ws.iter_cols():
        for cell in col:
            if cell.value in ["Sequence", "Start", "End"]:
                break
            else:
                if cell.row >= 3:
                    cell_v = cell.value
                    if cell_v != "*":
                        if uptake_color_length >= 1 and cell_v is not None and cell_v >= uptake_val_1:
                            fill = PatternFill(start_color=uptake_col_1, end_color=uptake_col_1, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 2 and cell_v is not None and cell_v >= uptake_val_2:
                            fill = PatternFill(start_color=uptake_col_2, end_color=uptake_col_2, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 3 and cell_v is not None and cell_v >= uptake_val_3:
                            fill = PatternFill(start_color=uptake_col_3, end_color=uptake_col_3, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 4 and cell_v is not None and cell_v >= uptake_val_4:
                            fill = PatternFill(start_color=uptake_col_4, end_color=uptake_col_4, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 5 and cell_v is not None and cell_v >= uptake_val_5:
                            fill = PatternFill(start_color=uptake_col_5, end_color=uptake_col_5, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 6 and cell_v is not None and cell_v >= uptake_val_6:
                            fill = PatternFill(start_color=uptake_col_6, end_color=uptake_col_6, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 7 and cell_v is not None and cell_v >= uptake_val_7:
                            fill = PatternFill(start_color=uptake_col_7, end_color=uptake_col_7, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 8 and cell_v is not None and cell_v >= uptake_val_8:
                            fill = PatternFill(start_color=uptake_col_8, end_color=uptake_col_8, fill_type='solid')
                            cell.number_format = ';;;'
                        elif uptake_color_length >= 9 and cell_v is not None and cell_v >= uptake_val_9:
                            fill = PatternFill(start_color=uptake_col_9, end_color=uptake_col_9, fill_type='solid')
                            cell.number_format = ';;;'
                        elif cell_v is not None and cell_v > 0.0:
                            fill = PatternFill(start_color=uptake_gtz_key, end_color=uptake_gtz_key, fill_type='solid')
                            cell.number_format = ';;;'
                        elif cell_v == 0:
                            fill = PatternFill(start_color=uptake_eqz_key, end_color=uptake_eqz_key, fill_type='solid')
                            cell.number_format = ';;;'
                        elif cell_v == -99999:
                            fill = PatternFill(start_color=uptake_abs_key, end_color=uptake_abs_key, fill_type='solid')
                            cell.number_format = ';;;'
                        elif cell_v is not None and cell_v < 0.0:
                            fill = PatternFill(start_color=uptake_ltz_key, end_color=uptake_ltz_key, fill_type='solid')
                            cell.number_format = ';;;'
                        if cell_v is not None:
                            cell.fill = fill
    increase_progress(0.33)


def r_chicdif():
    ws = wb.create_sheet("Chiclet Differences")
    plot_number = 0
    for stt, pair in new_dic_of_dif_list.items():
        first = pair[0]
        second = pair[1]
        sorted_peptides_first = sorted(peplist[first], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        sorted_peptides_second = sorted(peplist[second], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        difname = f"{stt}"
        if plot_number == 0:
            plot_start = 1
            plot_end = 50
        if plot_number > 0:
            plot_start = ws.max_column + 3
            plot_end = ws.max_column + 50
        ws.cell(row=1, column=plot_start, value=difname)
        ws.cell(row=2, column=plot_start, value = "Sequence")
        ws.cell(row=2, column=plot_start+1, value = "Start")
        ws.cell(row=2, column=plot_start+2, value = "End")
        tpnum = 0
        for timepoint in s_timepoints[first]:
            if timepoint in s_timepoints[second]:
                if timepoint == 0:
                    tpnum = tpnum + 1
                    continue
                ws.cell(row=2, column=plot_start+3+tpnum, value = s_timepoints[first][tpnum])
                tpnum = tpnum + 1

        if sort_var.get() == 1:
            sorted_peptides_first = sorted(peplist[first], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
            sorted_peptides_second = sorted(peplist[second], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        else:
            sorted_peptides_first = peplist[first]
            sorted_peptides_second = peplist[second]

        sorted_peptides_first = sorted(peplist[first], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        sorted_peptides_second = sorted(peplist[second], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))

        pepnum = 0
        for peptide in sorted_peptides_first:
            if peptide in sorted_peptides_second:
                startvalues = peptide_starts.get(peptide, None)
                startvalue= int(startvalues[0])
                endvalues = peptide_ends.get(peptide, None)
                endvalue = int(endvalues[0])

                ws.cell(row=3+pepnum, column=plot_start, value = peptide)
                ws.cell(row=3+pepnum, column=plot_start+1, value = startvalue)
                ws.cell(row=3+pepnum, column=plot_start+2, value = endvalue)
                tnum = 0
                for timepoint in s_timepoints[first]:
                    if timepoint in s_timepoints[second]:
                        if timepoint == 0:
                            tnum = tnum + 1
                            continue
                        if exp_bt_on_c:
                            if statedic_of_pepdic_cor[first][peptide][tnum][0] != -99999 and statedic_of_pepdic_cor[second][peptide][tnum][0] != -99999:
                                ws.cell(row=3+pepnum, column=plot_start+3+tnum, value=statedic_of_pepdic_cor[first][peptide][tnum][0] - statedic_of_pepdic_cor[second][peptide][tnum][0])
                                tnum = tnum + 1
                            else:
                                ws.cell(row=3+pepnum, column=plot_start+3+tnum, value = -99999)
                                tnum = tnum + 1
                        if theo_bt_on_c:
                            if statedic_of_pepdic_raw2[first][peptide][tnum][0] != -99999 and statedic_of_pepdic_raw2[second][peptide][tnum][0] != -99999:
                                ws.cell(row=3+pepnum, column=plot_start+3+tnum, value=statedic_of_pepdic_raw2[first][peptide][tnum][0] - statedic_of_pepdic_raw2[second][peptide][tnum][0])
                                tnum = tnum + 1
                            else:
                                ws.cell(row=3+pepnum, column=plot_start+3+tnum, value = -99999)
                                tnum = tnum + 1
                ch1 = False
                ch2 = False
                try:
                    if noD_dic_states[first][peptide] == True:
                        ch1 = True
                except:
                    pass
                try:
                    if noD_dic_states[second][peptide] == True:
                        ch2 = True
                except:
                    pass
                if ch1 == True or ch2 == True:
                    ws.cell(row=3+pepnum, column=plot_start+3+tnum, value="*")

                pepnum = pepnum + 1
        ws.column_dimensions[get_column_letter(plot_start)].width = 30
        plot_number = plot_number + 1




    white_fill = PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", fill_type='solid')
    for row in ws.rows:
        for cell in row:
            if cell.value != "*":
                cell.fill = white_fill
    for row in ws.iter_rows(max_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal='center')

    for col in ws.iter_cols():
        for cell in col:
            if cell.value in ["Sequence", "Start", "End"]:
                break
            else:
                if cell.row >= 3:
                    cell_v = cell.value
                    if cell_v != "*":
                        if cell_v == -99999:
                            fill = PatternFill(start_color=b_col_abs, end_color=b_col_abs, fill_type='solid')
                            cell.number_format = ';;;'
                        elif d_col_length >= 1 and cell_v is not None and cell_v >= d_val_1:
                            fill = PatternFill(start_color=d_col_1, end_color=d_col_1, fill_type='solid')
                            cell.number_format = ';;;'
                        elif d_col_length >= 2 and cell_v is not None and cell_v >= d_val_2:
                            fill = PatternFill(start_color=d_col_2, end_color=d_col_2, fill_type='solid')
                            cell.number_format = ';;;'
                        elif d_col_length >= 3 and cell_v is not None and cell_v >= d_val_3:
                            fill = PatternFill(start_color=d_col_3, end_color=d_col_3, fill_type='solid')
                            cell.number_format = ';;;'
                        elif d_col_length >= 4 and cell_v is not None and cell_v >= d_val_4:
                            fill = PatternFill(start_color=d_col_4, end_color=d_col_4, fill_type='solid')
                            cell.number_format = ';;;'
                        elif d_col_length >= 5 and cell_v is not None and cell_v >= d_val_5:
                            fill = PatternFill(start_color=d_col_5, end_color=d_col_5, fill_type='solid')
                            cell.number_format = ';;;'
                        elif cell_v is not None and cell_v > 0:
                            fill = PatternFill(start_color=d_col_gtz, end_color=d_col_gtz, fill_type='solid')
                            cell.number_format = ';;;'
                        elif p_col_length >= 1 and cell_v is not None and cell_v <= (-1) * p_val_1:
                            fill = PatternFill(start_color=p_col_1, end_color=p_col_1, fill_type='solid')
                            cell.number_format = ';;;'
                        elif p_col_length >= 2 and cell_v is not None and cell_v <= (-1) * p_val_2:
                            fill = PatternFill(start_color=p_col_2, end_color=p_col_2, fill_type='solid')
                            cell.number_format = ';;;'
                        elif p_col_length >= 3 and cell_v is not None and cell_v <= (-1) * p_val_3:
                            fill = PatternFill(start_color=p_col_3, end_color=p_col_3, fill_type='solid')
                            cell.number_format = ';;;'
                        elif p_col_length >= 4 and cell_v is not None and cell_v <= (-1) * p_val_4:
                            fill = PatternFill(start_color=p_col_4, end_color=p_col_4, fill_type='solid')
                            cell.number_format = ';;;'
                        elif p_col_length >= 5 and cell_v is not None and cell_v <= (-1) * p_val_5:
                            fill = PatternFill(start_color=p_col_5, end_color=p_col_5, fill_type='solid')
                            cell.number_format = ';;;'
                        elif cell_v is not None and cell_v < 0:
                            fill = PatternFill(start_color=p_col_gtz, end_color=p_col_gtz, fill_type='solid')
                            cell.number_format = ';;;'
                        elif cell_v is not None and cell_v == 0:
                            fill = PatternFill(start_color=b_col_eqz, end_color=b_col_eqz, fill_type='solid')
                            cell.number_format = ';;;'
                        if cell_v is not None:
                            cell.fill = fill



    increase_progress(0.33)

def r_condpeps():
    whitefont = Font(color="FFFFFFFF")
    for state in statedic_of_pepdic_cor:
        sorted_peptides = sorted(peplist[state], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        ws_title = (f"{state}".replace(":", ";") + "_cond")[-30:]
        ws = wb.create_sheet(title=ws_title)
        cell_reference_list = list()
        ws.append([" "])
        ws.append([" "] + seqlist_dic[state] + [" "])
        timepoint_number = 0
        for timepoint in s_timepoints[state]:
            if timepoint_number == 0:
                startrow = 3
                endrow = 250
            if timepoint_number != 0:
                startrow = ws.max_row +5
                endrow = ws.max_row + 250
            for peptide in sorted_peptides:
                startvalues = peptide_starts.get(peptide, None)
                startvalue= int(startvalues[0]) - seq_start[state]
                endvalues = peptide_ends.get(peptide, None)
                endvalue = int(endvalues[0]) - seq_start[state]
                peptide_length = len(peptide)
                Cuptake = None
                Cuptake_SD = None

                try:
                    for up, tp in statedic_of_pepdic_cor[state][peptide]:
                        if tp == timepoint:
                            Cuptake = up
                except:
                    pass
                try:
                    for sd, tp in statedic_of_sddic_cor[state][peptide]:
                        if tp == timepoint:
                            Cuptake_SD = sd
                except:
                    Cuptake_SD = -99999

                if Cuptake is not None:
                    for row in ws.iter_rows(min_row=startrow, max_row=startrow):
                        row[0].value = timepoint
                    for row in ws.iter_rows(min_row=startrow,max_row=endrow):
                        cells = row[startvalue + 1:endvalue + 2]
                        if all(cell.value is None for cell in cells):
                            row[startvalue + 1].value = Cuptake
                            row[startvalue + 1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                     bottom=Side(border_style='thin', color='FF000000'),
                                     left=Side(border_style='thin', color='FF000000'))
                            row[endvalue+1].value = Cuptake
                            row[endvalue+1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                     bottom=Side(border_style='thin', color='FF000000'),
                                     right=Side(border_style='thin', color='FF000000'))
                            for cell in row[startvalue + 2:endvalue+1]:
                                cell.value = Cuptake
                                cell.border = Border(top=Side(border_style='thin', color='FF000000'),
                                     bottom=Side(border_style='thin', color='FF000000'))
                            middle = int((startvalue + 1 + endvalue + 1)/2)

                            if sd_checkvar.get() == 0:
                                row[middle-1].value = round(Cuptake * 100)
                            else:
                                if Cuptake_SD != -99999 and Cuptake_SD != -99999 and Cuptake_SD != 0 and Cuptake_SD != "-99999" and Cuptake_SD != "0":
                                    row[middle-1].value = str(round(Cuptake * 100)) + " " + "\u00B1" + str(round(Cuptake_SD * 100))
                                else:
                                    row[middle-1].value = round(Cuptake * 100)
                            row[middle-1].alignment = Alignment(horizontal='center')


                            if uptake_color_length >= 1 and Cuptake > uptake_val_1:
                                fill = PatternFill(start_color=uptake_col_1, end_color=uptake_col_1, fill_type='solid')
                                font = Font(color=uptake_text_1, size=16)
                            elif uptake_color_length >= 2 and Cuptake > uptake_val_2:
                                fill = PatternFill(start_color=uptake_col_2, end_color=uptake_col_2, fill_type='solid')
                                font = Font(color=uptake_text_2, size=16)
                            elif uptake_color_length >= 3 and Cuptake > uptake_val_3:
                                fill = PatternFill(start_color=uptake_col_3, end_color=uptake_col_3, fill_type='solid')
                                font = Font(color=uptake_text_3, size=16)
                            elif uptake_color_length >= 4 and Cuptake > uptake_val_4:
                                fill = PatternFill(start_color=uptake_col_4, end_color=uptake_col_4, fill_type='solid')
                                font = Font(color=uptake_text_4, size=16)
                            elif uptake_color_length >= 5 and Cuptake > uptake_val_5:
                                fill = PatternFill(start_color=uptake_col_5, end_color=uptake_col_5, fill_type='solid')
                                font = Font(color=uptake_text_5, size=16)
                            elif uptake_color_length >= 6 and Cuptake > uptake_val_6:
                                fill = PatternFill(start_color=uptake_col_6, end_color=uptake_col_6, fill_type='solid')
                                font = Font(color=uptake_text_6, size=16)
                            elif uptake_color_length >= 7 and Cuptake > uptake_val_7:
                                fill = PatternFill(start_color=uptake_col_7, end_color=uptake_col_7, fill_type='solid')
                                font = Font(color=uptake_text_7, size=16)
                            elif uptake_color_length >= 8 and Cuptake > uptake_val_8:
                                fill = PatternFill(start_color=uptake_col_8, end_color=uptake_col_8, fill_type='solid')
                                font = Font(color=uptake_text_8, size=16)
                            elif uptake_color_length >= 9 and Cuptake > uptake_val_9:
                                fill = PatternFill(start_color=uptake_col_9, end_color=uptake_col_9, fill_type='solid')
                                font = Font(color=uptake_text_9, size=16)
                            elif Cuptake > 0.0:
                                fill = PatternFill(start_color=uptake_gtz_key, end_color=uptake_gtz_key, fill_type='solid')
                                font = Font(color=uptake_gtz_text, size=16)
                            elif Cuptake == 0:
                                fill = PatternFill(start_color=uptake_eqz_key, end_color=uptake_eqz_key, fill_type='solid')
                                row[middle-1].number_format = ';;;'
                                font = Font(color=uptake_eqz_text, size=16)
                            elif Cuptake == -99999:
                                fill = PatternFill(start_color=uptake_abs_key, end_color=uptake_abs_key, fill_type='solid')
                                row[middle-1].number_format = ';;;'
                                font = Font(color=uptake_abs_text, size=16)
                            elif Cuptake < 0.0:
                                fill = PatternFill(start_color=uptake_ltz_key, end_color=uptake_ltz_key, fill_type='solid')
                                font = Font(color=uptake_ltz_text, size=16)

                            row[middle-1].fill = fill
                            row[middle-1].font = font

                            if sd_checkvar.get() == 0:
                                ws.merge_cells(start_row=row[middle-1].row, start_column=row[middle-1].column, end_row=row[middle+1].row, end_column=row[middle+1].column)
                                middle_cell_reference = row[middle-1].coordinate
                                cell_reference_list.append(middle_cell_reference)
                                if row[middle-1].number_format != ';;;':
                                    row[middle-1].number_format = "0"
                            else:
                                ws.merge_cells(start_row=row[middle-1].row, start_column=row[middle-1].column, end_row=row[middle+2].row, end_column=row[middle+2].column)
                                middle_cell_reference = row[middle-1].coordinate
                                cell_reference_list.append(middle_cell_reference)


                            try:
                                if peptide in noD_dic_states[state]:
                                    if Cuptake != 0 and Cuptake != -99999:
                                        row[startvalue+1].value = "*"
                                        #row[startvalue+1].alignment = Alignment(textRotation=90, vertical='center')
                                        if uptake_color_length >= 1 and Cuptake > uptake_val_1:
                                            fill = PatternFill(start_color=uptake_col_1, end_color=uptake_col_1, fill_type='solid')
                                            font = Font(color=uptake_text_1, size=16)
                                        elif uptake_color_length >= 2 and Cuptake > uptake_val_2:
                                            fill = PatternFill(start_color=uptake_col_2, end_color=uptake_col_2, fill_type='solid')
                                            font = Font(color=uptake_text_2, size=16)
                                        elif uptake_color_length >= 3 and Cuptake > uptake_val_3:
                                            fill = PatternFill(start_color=uptake_col_3, end_color=uptake_col_3, fill_type='solid')
                                            font = Font(color=uptake_text_3, size=16)
                                        elif uptake_color_length >= 4 and Cuptake > uptake_val_4:
                                            fill = PatternFill(start_color=uptake_col_4, end_color=uptake_col_4, fill_type='solid')
                                            font = Font(color=uptake_text_4, size=16)
                                        elif uptake_color_length >= 5 and Cuptake > uptake_val_5:
                                            fill = PatternFill(start_color=uptake_col_5, end_color=uptake_col_5, fill_type='solid')
                                            font = Font(color=uptake_text_5, size=16)
                                        elif uptake_color_length >= 6 and Cuptake > uptake_val_6:
                                            fill = PatternFill(start_color=uptake_col_6, end_color=uptake_col_6, fill_type='solid')
                                            font = Font(color=uptake_text_6, size=16)
                                        elif uptake_color_length >= 7 and Cuptake > uptake_val_7:
                                            fill = PatternFill(start_color=uptake_col_7, end_color=uptake_col_7, fill_type='solid')
                                            font = Font(color=uptake_text_7, size=16)
                                        elif uptake_color_length >= 8 and Cuptake > uptake_val_8:
                                            fill = PatternFill(start_color=uptake_col_8, end_color=uptake_col_8, fill_type='solid')
                                            font = Font(color=uptake_text_8, size=16)
                                        elif uptake_color_length >= 9 and Cuptake > uptake_val_9:
                                            fill = PatternFill(start_color=uptake_col_9, end_color=uptake_col_9, fill_type='solid')
                                            font = Font(color=uptake_text_9, size=16)
                                        elif Cuptake > 0.0:
                                            fill = PatternFill(start_color=uptake_gtz_key, end_color=uptake_gtz_key, fill_type='solid')
                                            font = Font(color=uptake_gtz_text, size=16)
                                        elif Cuptake == 0:
                                            fill = PatternFill(start_color=uptake_eqz_key, end_color=uptake_eqz_key, fill_type='solid')
                                            font = Font(color=uptake_eqz_text, size=16)
                                            cell.number_format = ';;;'
                                        elif Cuptake == -99999:
                                            fill = PatternFill(start_color=uptake_abs_key, end_color=uptake_abs_key, fill_type='solid')
                                            font = Font(color=uptake_abs_text, size=16)
                                            cell.number_format = ';;;'
                                        elif Cuptake < 0.0:
                                            fill = PatternFill(start_color=uptake_ltz_key, end_color=uptake_ltz_key, fill_type='solid')
                                            font = Font(color=uptake_ltz_text, size=16)
                                        row[startvalue+1].fill = fill
                                        row[startvalue+1].font = font
                            except:
                                pass



                            break
                        else:
                            continue



            timepoint_number = timepoint_number + 1





        white_fill = PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", fill_type='solid')
        for row in ws.rows:
            for cell in row:
                if cell.value == None:
                    cell.fill = white_fill
        for row in ws.iter_rows(min_row=2, max_row=2):
            for cell in row:
                cell.fill = white_fill




        for i, column in enumerate(ws.columns):
            if i == 0:
                continue
            ws.column_dimensions[column[0].column_letter].width = con_pep_width_enter.get()





        for row in ws.iter_rows(min_row=3):
            for cell in row[1:]:
                cell_v = cell.value
                if cell.coordinate not in cell_reference_list and cell_v != "*":
                    if uptake_color_length >= 1 and cell_v is not None and cell_v > uptake_val_1:
                        fill = PatternFill(start_color=uptake_col_1, end_color=uptake_col_1, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 2 and cell_v is not None and cell_v > uptake_val_2:
                        fill = PatternFill(start_color=uptake_col_2, end_color=uptake_col_2, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 3 and cell_v is not None and cell_v > uptake_val_3:
                        fill = PatternFill(start_color=uptake_col_3, end_color=uptake_col_3, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 4 and cell_v is not None and cell_v > uptake_val_4:
                        fill = PatternFill(start_color=uptake_col_4, end_color=uptake_col_4, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 5 and cell_v is not None and cell_v > uptake_val_5:
                        fill = PatternFill(start_color=uptake_col_5, end_color=uptake_col_5, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 6 and cell_v is not None and cell_v > uptake_val_6:
                        fill = PatternFill(start_color=uptake_col_6, end_color=uptake_col_6, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 7 and cell_v is not None and cell_v > uptake_val_7:
                        fill = PatternFill(start_color=uptake_col_7, end_color=uptake_col_7, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 8 and cell_v is not None and cell_v > uptake_val_8:
                        fill = PatternFill(start_color=uptake_col_8, end_color=uptake_col_8, fill_type='solid')
                        cell.number_format = ';;;'
                    elif uptake_color_length >= 9 and cell_v is not None and cell_v > uptake_val_9:
                        fill = PatternFill(start_color=uptake_col_9, end_color=uptake_col_9, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v > 0.0:
                        fill = PatternFill(start_color=uptake_gtz_key, end_color=uptake_gtz_key, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v == 0:
                        fill = PatternFill(start_color=uptake_eqz_key, end_color=uptake_eqz_key, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v == -99999:
                        fill = PatternFill(start_color=uptake_abs_key, end_color=uptake_abs_key, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v < 0.0:
                        fill = PatternFill(start_color=uptake_ltz_key, end_color=uptake_ltz_key, fill_type='solid')
                        cell.number_format = ';;;'
                    if cell_v is not None:
                        cell.fill = fill

        increase_progress(1)


        for row in ws.iter_rows(min_row=1, max_row=1):
            num = seq_start[state]
            for cell in row:
                if cell.column >= 2 and cell.column < ws.max_column:
                    cell.value = num
                    num = num+1


        for row in ws.iter_rows(max_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal='center')



def r_difcond():
    whitefont = Font(color="FFFFFFFF")
    for stt, pair in  new_dic_of_dif_list.items():
        first = pair[0]
        second = pair[1]
        sorted_peptides_first = sorted(peplist[first], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        sorted_peptides_second = sorted(peplist[second], key=lambda p: (int(peptide_starts.get(p, [0])[0]), len(p)))
        difname = f"{stt}"
        ws_title = (f"{difname}" + "_cond")[-30:]
        ws = wb.create_sheet(title=ws_title)
        cell_reference_list = list()
        ws.append([" "])
        ws.append([" "] + seqlist_dic[first] + [" "])
        timepoint_number = 0
        for timepoint in s_timepoints[first]:
            if timepoint in s_timepoints[second]:
                if timepoint_number == 0:
                    startrow = 3
                    endrow = 250
                if timepoint_number != 0:
                    startrow = ws.max_row +5
                    endrow = ws.max_row + 250
                for peptide in sorted_peptides_first:
                    if peptide in sorted_peptides_second:
                        startvalues = peptide_starts.get(peptide, None)
                        startvalue= int(startvalues[0]) - seq_start[first]
                        endvalues = peptide_ends.get(peptide, None)
                        endvalue = int(endvalues[0]) - seq_start[first]
                        peptide_length = len(peptide)
                        diftake = None
                        if exp_bt_on_c == True:
                            up1 = None
                            up2 = None
                            diftake = None

                            try:
                                for up, tp in statedic_of_pepdic_cor[first][peptide]:
                                    if tp == timepoint:
                                        up1 = up
                                for up, tp in statedic_of_pepdic_cor[second][peptide]:
                                    if tp == timepoint:
                                        up2 = up
                                if up1 is not None and up2 is not None and up1 != -99999 and up2 != -99999:
                                    diftake = up1 - up2
                                elif up1 is not None and up2 is not None:
                                    diftake = -99999

                            except:
                                pass

                            try:
                                SD1 = None
                                SD2 = None
                                diftake_SD = None
                                for sd, tp in statedic_of_sddic_cor[first][peptide]:
                                    if tp == timepoint:
                                        SD1 = sd
                                for sd, tp in statedic_of_sddic_cor[second][peptide]:
                                    if tp == timepoint:
                                        SD2 = sd
                                if SD1 is not None and SD2 is not None and SD1 != -99999 and SD2 != -99999:
                                    SDs = np.array([SD1, SD2])
                                    diftake_SD = np.sqrt(np.sum(SDs ** 2))
                                elif SD1 is not None and SD2 is not None:
                                    diftake_SD = -99999
                            except:
                                diftake_SD = -99999

                        if theo_bt_on_c == True:
                            up1 = None
                            up2 = None
                            diftake = None
                            try:
                                for up, tp in statedic_of_pepdic_raw2[first][peptide]:
                                    if tp == timepoint:
                                        up1 = up
                                for up, tp in statedic_of_pepdic_raw2[second][peptide]:
                                    if tp == timepoint:
                                        up2 = up
                                if up1 is not None and up2 is not None and up1 != -99999 and up2 != -99999:
                                    diftake = up1 - up2
                                elif up1 is not None and up2 is not None:
                                    diftake = -99999
                            except:
                                pass

                            try:
                                SD1 = None
                                SD2 = None
                                diftake_SD = None
                                for sd, tp in statedic_of_sddic_raw2[first][peptide]:
                                    if tp == timepoint:
                                        SD1 = sd
                                for sd, tp in statedic_of_sddic_raw2[second][peptide]:
                                    if tp == timepoint:
                                        SD2 = sd
                                if SD1 is not None and SD2 is not None and SD1 != -99999 and SD2 != -99999:
                                    SDs = np.array([SD1, SD2])
                                    diftake_SD = np.sqrt(np.sum(SDs ** 2))
                                elif SD1 is not None and SD2 is not None:
                                    diftake_SD = -99999
                            except:
                                diftake_SD = -99999


                        if diftake is not None:
                            for row in ws.iter_rows(min_row=startrow, max_row=startrow):
                                row[0].value = timepoint
                            for row in ws.iter_rows(min_row=startrow,max_row=endrow):
                                cells = row[startvalue + 1:endvalue + 2]
                                if all(cell.value is None for cell in cells):
                                    row[startvalue + 1].value = diftake
                                    row[startvalue + 1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                             bottom=Side(border_style='thin', color='FF000000'),
                                             left=Side(border_style='thin', color='FF000000'))
                                    row[endvalue+1].value = diftake
                                    row[endvalue+1].border = Border(top=Side(border_style='thin', color='FF000000'),
                                             bottom=Side(border_style='thin', color='FF000000'),
                                             right=Side(border_style='thin', color='FF000000'))
                                    for cell in row[startvalue + 2:endvalue+1]:
                                        cell.value = diftake
                                        cell.border = Border(top=Side(border_style='thin', color='FF000000'),
                                             bottom=Side(border_style='thin', color='FF000000'))
                                    middle = int((startvalue + 1 + endvalue + 1)/2)


                                    if sd_checkvar.get() == 0:
                                        if exp_bt_on_c:
                                            row[middle-1].value = round(diftake * 100, 1)
                                            row[middle-1].number_format = "0.0"
                                            row[middle-1].alignment = Alignment(horizontal='center')


                                        if theo_bt_on_c:
                                            row[middle-1].value = round(diftake, 1)
                                            row[middle-1].number_format = "0.0"
                                            row[middle-1].alignment = Alignment(horizontal='center')
                                    else:
                                        if len(peptide) > 6:
                                            if diftake_SD != -99999 and diftake_SD != 0 and diftake_SD != "-99999" and diftake_SD != "0":
                                                if exp_bt_on_c:
                                                    if (str(diftake).startswith("-") and len(str(round(diftake * 100))) == 2) or len(str(round(diftake * 100))) == 1:
                                                        row[middle-2].value = str(round(diftake * 100, 1)) + " " + "\u00B1" + str(round(diftake_SD * 100, 1))
                                                    else:
                                                        row[middle-2].value = str(round(diftake * 100)) + " " + "\u00B1" + str(round(diftake_SD * 100))
                                                        row[middle-2].alignment = Alignment(horizontal='center')
                                                if theo_bt_on_c:
                                                    if (str(diftake).startswith("-") and len(str(round(diftake))) == 2) or len(str(round(diftake))) == 1:
                                                        row[middle-2].value = str(round(diftake, 1)) + " " + "\u00B1" + str(round(diftake_SD, 1))
                                                    else:
                                                        row[middle-2].value = str(round(diftake)) + " " + "\u00B1" + str(round(diftake_SD))
                                                    row[middle-2].alignment = Alignment(horizontal='center')
                                            else:
                                                if exp_bt_on_c:
                                                    row[middle-2].value = round(diftake * 100, 1)
                                                if theo_bt_on_c:
                                                    row[middle-2].value = round(diftake, 1)
                                                row[middle-2].alignment = Alignment(horizontal='center')

                                        elif len(peptide) == 6:
                                            if diftake_SD != -99999 and diftake_SD != 0 and diftake_SD != "-99999" and diftake_SD != "0":
                                                if exp_bt_on_c:
                                                    row[middle-1].value = str(round(diftake * 100)) + " " + "\u00B1" + str(round(diftake_SD * 100))
                                                if theo_bt_on_c:
                                                    if (str(diftake).startswith("-") and len(str(round(diftake))) == 2) or len(str(round(diftake))) == 1:
                                                        row[middle-1].value = str(round(diftake)) + " " + "\u00B1" + str(round(diftake_SD))
                                                    else:
                                                        row[middle-1].value = str(round(diftake)) + " " + "\u00B1" + str(round(diftake_SD))
                                                    row[middle-1].alignment = Alignment(horizontal='center')
                                            else:
                                                if exp_bt_on_c:
                                                    row[middle-1].value = round(diftake * 100)
                                                if theo_bt_on_c:
                                                    row[middle-1].value = round(diftake, 1)
                                                row[middle-1].alignment = Alignment(horizontal='center')


                                    if sd_checkvar.get() == 0:
                                        c = 1
                                    else:
                                        if len(peptide) == 6:
                                            c = 1
                                        else:
                                            c = 2

                                    if diftake == -99999:
                                        fill = PatternFill(start_color=b_col_abs, end_color=b_col_abs, fill_type='solid')
                                        row[middle-c].number_format = ';;;'
                                    elif p_col_length >= 1 and diftake >= d_val_1:
                                        fill = PatternFill(start_color=d_col_1, end_color=d_col_1, fill_type='solid')
                                        font = Font(color=d_text_1, size=16)
                                    elif p_col_length >= 2 and diftake >= d_val_2:
                                        fill = PatternFill(start_color=d_col_2, end_color=d_col_2, fill_type='solid')
                                        font = Font(color=d_text_2, size=16)
                                    elif p_col_length >= 3 and diftake >= d_val_3:
                                        fill = PatternFill(start_color=d_col_3, end_color=d_col_3, fill_type='solid')
                                        font = Font(color=d_text_3, size=16)
                                    elif p_col_length >= 4 and diftake >= d_val_4:
                                        fill = PatternFill(start_color=d_col_4, end_color=d_col_4, fill_type='solid')
                                        font = Font(color=d_text_4, size=16)
                                    elif p_col_length >= 5 and diftake >= d_val_5:
                                        fill = PatternFill(start_color=d_col_5, end_color=d_col_5, fill_type='solid')
                                        font = Font(color=d_text_5, size=16)
                                    elif diftake > 0:
                                        fill = PatternFill(start_color=d_col_gtz, end_color=d_col_gtz, fill_type='solid')
                                        font = Font(color=d_text_gtz, size=16)
                                        if insig_dif_chk.get() == 0:
                                            row[middle-c].number_format = ';;;'
                                    elif diftake == 0:
                                        fill = PatternFill(start_color=b_col_eqz, end_color=b_col_eqz, fill_type='solid')
                                        font = Font(color=b_text_eqz, size=16)
                                        row[middle-c].number_format = ';;;'
                                    elif d_col_length >= 1 and diftake <= (-1) * p_val_1:
                                        fill = PatternFill(start_color=p_col_1, end_color=p_col_1, fill_type='solid')
                                        font = Font(color=p_text_1, size=16)
                                    elif d_col_length >= 2 and diftake <= (-1) * p_val_2:
                                        fill = PatternFill(start_color=p_col_2, end_color=p_col_2, fill_type='solid')
                                        font = Font(color=p_text_2, size=16)
                                    elif d_col_length >= 3 and diftake <= (-1) * p_val_3:
                                        fill = PatternFill(start_color=p_col_3, end_color=p_col_3, fill_type='solid')
                                        font = Font(color=p_text_3, size=16)
                                    elif d_col_length >= 4 and diftake <= (-1) * p_val_4:
                                        fill = PatternFill(start_color=p_col_4, end_color=p_col_4, fill_type='solid')
                                        font = Font(color=p_text_4, size=16)
                                    elif d_col_length >= 5 and diftake <= (-1) * p_val_5:
                                        fill = PatternFill(start_color=p_col_5, end_color=p_col_5, fill_type='solid')
                                        font = Font(color=p_text_5, size=16)
                                    elif diftake < 0:
                                        fill = PatternFill(start_color=p_col_gtz, end_color=p_col_gtz, fill_type='solid')
                                        font = Font(color=p_text_gtz, size=16)
                                        if insig_dif_chk.get() == 0:
                                            row[middle-c].number_format = ';;;'

                                    row[middle-c].fill = fill
                                    row[middle-c].font = font

                                    if sd_checkvar.get() == 0:
                                        if exp_bt_on_c:
                                            ws.merge_cells(start_row=row[middle-1].row, start_column=row[middle-1].column, end_row=row[middle+2].row, end_column=row[middle+2].column)
                                            middle_cell_reference = row[middle-1].coordinate
                                            cell_reference_list.append(middle_cell_reference)

                                        if theo_bt_on_c:
                                            ws.merge_cells(start_row=row[middle-1].row, start_column=row[middle-1].column, end_row=row[middle+2].row, end_column=row[middle+2].column)
                                            middle_cell_reference = row[middle-1].coordinate
                                            cell_reference_list.append(middle_cell_reference)


                                    if sd_checkvar.get() == 1:
                                        if len(peptide) == 6:
                                            ws.merge_cells(start_row=row[middle-1].row, start_column=row[middle-1].column, end_row=row[middle+2].row, end_column=row[middle+2].column)
                                            middle_cell_reference = row[middle-1].coordinate
                                        else:
                                            ws.merge_cells(start_row=row[middle-2].row, start_column=row[middle-2].column, end_row=row[middle+2].row, end_column=row[middle+2].column)
                                            middle_cell_reference = row[middle-2].coordinate

                                        cell_reference_list.append(middle_cell_reference)




                                    ch1 = False
                                    ch2 = False
                                    try:
                                        if noD_dic_states[first][peptide] == True:
                                            ch1 = True
                                    except:
                                        pass
                                    try:
                                        if noD_dic_states[second][peptide] == True:
                                            ch2 = True
                                    except:
                                        pass
                                    if ch1 == True or ch2 == True:
                                        if diftake != 0 and diftake != -99999:
                                            row[startvalue+1].value = "*"
                                            #row[startvalue+1].alignment = Alignment(textRotation=90, vertical='center', horizontal='left')


                                            if d_col_length >= 1 and diftake >= d_val_1:
                                                fill = PatternFill(start_color=d_col_1, end_color=d_col_1, fill_type='solid')
                                                font = Font(color=d_text_1, size=16)
                                            elif d_col_length >= 2 and diftake >= d_val_2:
                                                fill = PatternFill(start_color=d_col_2, end_color=d_col_2, fill_type='solid')
                                                font = Font(color=d_text_2, size=16)
                                            elif d_col_length >= 3 and diftake >= d_val_3:
                                                fill = PatternFill(start_color=d_col_3, end_color=d_col_3, fill_type='solid')
                                                font = Font(color=d_text_3, size=16)
                                            elif d_col_length >= 4 and diftake >= d_val_4:
                                                fill = PatternFill(start_color=d_col_4, end_color=d_col_4, fill_type='solid')
                                                font = Font(color=d_text_4, size=16)
                                            elif d_col_length >= 5 and diftake >= d_val_5:
                                                fill = PatternFill(start_color=d_col_5, end_color=d_col_5, fill_type='solid')
                                                font = Font(color=d_text_5, size=16)
                                            elif diftake > 0:
                                                fill = PatternFill(start_color=d_col_gtz, end_color=d_col_gtz, fill_type='solid')
                                                font = Font(color=d_text_gtz, size=16)
                                            elif p_col_length >= 1 and diftake <= (-1) * p_val_1:
                                                fill = PatternFill(start_color=p_col_1, end_color=p_col_1, fill_type='solid')
                                                font = Font(color=p_text_1, size=16)
                                            elif p_col_length >= 2 and diftake <= (-1) * p_val_2:
                                                fill = PatternFill(start_color=p_col_2, end_color=p_col_2, fill_type='solid')
                                                font = Font(color=p_text_2, size=16)
                                            elif p_col_length >= 3 and diftake <= (-1) * p_val_3:
                                                fill = PatternFill(start_color=p_col_3, end_color=p_col_3, fill_type='solid')
                                                font = Font(color=p_text_3, size=16)
                                            elif p_col_length >= 4 and diftake <= (-1) * p_val_4:
                                                fill = PatternFill(start_color=p_col_4, end_color=p_col_4, fill_type='solid')
                                                font = Font(color=p_text_4, size=16)
                                            elif p_col_length >= 5 and diftake <= (-1) * p_val_5:
                                                fill = PatternFill(start_color=p_col_5, end_color=p_col_5, fill_type='solid')
                                                font = Font(color=p_text_5, size=16)
                                            elif diftake < 0:
                                                fill = PatternFill(start_color=p_col_gtz, end_color=p_col_gtz, fill_type='solid')
                                                font = Font(color=p_text_gtz, size=16)
                                            row[startvalue+1].fill = fill
                                            row[startvalue+1].font = font






                                    break
                                else:
                                    continue



                    timepoint_number = timepoint_number + 1



        white_fill = PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", fill_type='solid')
        for row in ws.rows:
            for cell in row:
                if cell.value == None:
                    cell.fill = white_fill
        for row in ws.iter_rows(min_row=2, max_row=2):
            for cell in row:
                cell.fill = white_fill




        for i, column in enumerate(ws.columns):
            if i == 0:
                continue
            ws.column_dimensions[column[0].column_letter].width = con_pep_width_enter.get()


        for row in ws.iter_rows(min_row=3):
            for cell in row[1:]:
                cell_v = cell.value
                if cell.coordinate not in cell_reference_list and cell_v != "*":
                    if cell_v == -99999:
                        fill = PatternFill(start_color=b_col_abs, end_color=b_col_abs, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 1 and cell_v is not None and cell_v >= d_val_1:
                        fill = PatternFill(start_color=d_col_1, end_color=d_col_1, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 2 and cell_v is not None and cell_v >= d_val_2:
                        fill = PatternFill(start_color=d_col_2, end_color=d_col_2, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 3 and cell_v is not None and cell_v >= d_val_3:
                        fill = PatternFill(start_color=d_col_3, end_color=d_col_3, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 4 and cell_v is not None and cell_v >= d_val_4:
                        fill = PatternFill(start_color=d_col_4, end_color=d_col_4, fill_type='solid')
                        cell.number_format = ';;;'
                    elif d_col_length >= 5 and cell_v is not None and cell_v >= d_val_5:
                        fill = PatternFill(start_color=d_col_5, end_color=d_col_5, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v > 0:
                        fill = PatternFill(start_color=d_col_gtz, end_color=d_col_gtz, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >=1 and cell_v is not None and cell_v <= (-1) * p_val_1:
                        fill = PatternFill(start_color=p_col_1, end_color=p_col_1, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >=2 and cell_v is not None and cell_v <= (-1) * p_val_2:
                        fill = PatternFill(start_color=p_col_2, end_color=p_col_2, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >=3 and cell_v is not None and cell_v <= (-1) * p_val_3:
                        fill = PatternFill(start_color=p_col_3, end_color=p_col_3, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >=4 and cell_v is not None and cell_v <= (-1) * p_val_4:
                        fill = PatternFill(start_color=p_col_4, end_color=p_col_4, fill_type='solid')
                        cell.number_format = ';;;'
                    elif p_col_length >=5 and cell_v is not None and cell_v <= (-1) * p_val_5:
                        fill = PatternFill(start_color=p_col_5, end_color=p_col_5, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v < 0:
                        fill = PatternFill(start_color=p_col_gtz, end_color=p_col_gtz, fill_type='solid')
                        cell.number_format = ';;;'
                    elif cell_v is not None and cell_v == 0:
                        fill = PatternFill(start_color=b_col_eqz, end_color=b_col_eqz, fill_type='solid')
                        cell.number_format = ';;;'
                    if cell.value is not None:
                        cell.fill = fill



        increase_progress(1)


        for row in ws.iter_rows(min_row=1, max_row=1):
            num = seq_start[first]
            for cell in row:
                if cell.column >= 2 and cell.column < ws.max_column:
                    cell.value = num
                    num = num+1


        for row in ws.iter_rows(max_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal='center')


def save_wb():
    wb.remove(wb['Sheet'])
    def get_user_title():
        wb_tit = filedialog.asksaveasfilename(filetypes=[("Excel Files", "*.xlsx")])
        if wb_tit:
            if not wb_tit.endswith(".xlsx"):
                wb_tit += ".xlsx"
            wb.save(wb_tit)
            tk.messagebox.showinfo("Save Workbook", f"The workbook has been saved as '{wb_tit}'.")
        else:
            tk.messagebox.showwarning("Save Workbook", "No file path selected. The workbook was not saved.")


    increase_progress(1)


    run_bt.config(state="normal")
    run_bt.config(relief="raised")

    global tit_bt
    tit_bt = tk.Button(window, text="Save Workbook", command=get_user_title)
    tit_bt.place(x=1290, y=190)








window.mainloop()
