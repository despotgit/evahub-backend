# in /Users/jsachau/_INITIATIVES/TecVerb_EnergieSicherheit/JRC_Sabbatical/JS_work/gIt_evahub/evahub'
# shebang #!(usr/bin/env python3
# run in Git_evahub/evahub>  python -i backend/python-json2md_tex_V1.py TestUser/JRC_GridStorage  _06_2023
#                            CTRL-D
# USES     pdflatex
# History  from /backend/python-json2md_tex_V0.py
#           adapt for latex run with figures and backend/repgen_format_22.tex
#           dir_nam in line 117 EVAL
#           line 78 and 112   use tex template instead of md_file
#           line 122 tex_template="backend/repgen_format_22.tex"
#                        tex_template="backend/repgen_headerfooter_graph.tex" works as test
#                     use eps figures now
#           line
#
#           make lyx template in backend>repgen_format_22.lyx
#                        cp dummy_figs from here to backend>
#                    export AS  to backend as   pdflatex .tex
#
#
# https://aty.sdsu.edu/bibliog/latex/LaTeXtoPDF.html
# running pdflatex via subprocess.run in a temporary directory

#
import re
import io
import base64
import matplotlib.pyplot as plt

import markdown

import json
import matplotlib.pyplot as plt
import numpy as np
import sys

import os
from subprocess import call, PIPE

# https://stackoverflow.com/questions/59787127/how-to-add-header-and-footer-to-a-markdown-file
# https://www.freecodecamp.org/news/reusable-html-components-how-to-reuse-a-header-and-footer-on-a-website/
# pandoc -D latex | less   zeigt die latex preamble, die pandoc verwendet
# https://github.com/yzane/vscode-markdown-pdf#markdown-pdfheadertemplate
#   eg
# "markdown-pdf.headerTemplate": "<div style=\"font-size: 9px; margin-left: 1cm;\"> <span class='title'></span></div> <div style=\"font-size: 9px; margin-left: auto; margin-right: 1cm; \"> <span class='date'></span></div>",
#
# https://github.com/justinvh/Markdown-LaTeX
# dies ist eine latex extension, image generation is done via LaTeX/DVI output.
# It encodes data as base64 so there is no need for images directly.
# All the work is done in the preprocessor.
# benutzt auch python tempfile
#
# run with Python 3.9.15 github_venv :conda
# gIt_evahub > source github_venv/bin/activate
#  evahub> % python -i "backend/python-jsonplot_V1.py"    end with close figures and CTRL+D
#                    interactive in the terminal
# %matplotlibdata = ()


# Turn interactive plotting off
plt.ioff()

dir_nam = str(sys.argv[1])

DataName = str(sys.argv[2])
# split(filename,'/#') in dir_nam and DataName

UserName = "TestUser"
ProjName = "JRC_GridStorage"
DataName = "_06_2023"

####### .json files lesen
dir_nam = str(UserName) + "/" + str(ProjName)

filename = dir_nam + "/HEAD" + str(DataName) + ".json"  #' HEADER'
try:
    with open(filename, "r") as read_file:
        HEAD_dict = json.load(read_file)
        print(HEAD_dict)
except IOError as Fehler:
    print("An IOError occurred: %s" % Fehler)
if False == ("Storage_System_Name" in HEAD_dict):
    HEAD_dict["Storage_System_Name"] = ProjName  # use as default ProjName

filename = dir_nam + "/DIR" + str(DataName) + ".json"  # directed flows'
try:
    with open(filename, "r") as read_file:
        DIR_dict = json.load(read_file)
except IOError as Fehler:
    print("An IOError occurred: %s" % Fehler)

A_I_dict = {}
filename = (
    dir_nam + "/AUTH_INTRO" + str(DataName) + ".json"
)  # monatl.  Autor und Text zum report'
try:
    with open(filename, "r") as read_file:
        A_I_dict = json.loads(read_file)
except:
    print("Use Default Author and Intro: %s")

filename = (
    dir_nam + "/AUTH_INTRO_DEFAULT" + ".json"
)  # wenn nicht Default Autor und Text
try:
    with open(filename, "r") as read_file:
        A_I_dict = json.loads(read_file)
except IOError as Fehler:
    print("An IOError occurred: %s" % Fehler)

### IF all fails, USE DEFAULT ENTRIES
if False == ("Author" in A_I_dict):
    A_I_dict["Author"] = "Generic"  # use some defaults

intro_text = A_I_dict.get(
    "Intro",
    "This report provides analysis and presentation of measured data for the storage system "
    + HEAD_dict.get("Storage_System_Name"),
)

### All_dict zusammenbauen für replacement

ALL_dict = HEAD_dict  # A_I_dict | HEAD_dict # es fehlen noch results form Dir_dict'
print(ALL_dict)
# .....

###### json data in md_file einbauen   askpython.com
# keylist = list(HEAD_dict.keys())  # liefert Liste der Schlüssel set( liefert set)
# data_list = list(HEAD_dict.values())  # liefert die Inhaltedict

tex_template = "repgen_format_22.tex"
# tex_template="backend/repgen_headerfooter_graph.tex"   Test-Template is working
template_file = tex_template
# print(str)
""" try:
        cache_file = open(md_file, 'r+')
        for line in cache_file.readlines():
                line = line.strip("\n").split(" ")
        page="\n".join(line)        
except IOError:
        pass """
## Instead
try:
    with open(template_file, "r") as text_file:
        report_content = text_file.read()
except IOError as Fehler:
    print("An IOError occurred: %s" % Fehler)
    pass

#### find pattern in
#####  old : pattern = r"§§-(.*?)-§§" #regular expression as from lyx export2md
##### now replace string variables named §§-     either text or string from data or figure string
# for key in dictionary:
# file = file.replace(str(key), dictionary[key])
delim = "$-"
for key in ALL_dict:
    # if HEAD_dict[key] floating, then convert to string
    report_content = report_content.replace(delim + str(key), str(ALL_dict[key]))
# With this simple snippet I am able to replace each occurence of dictionary key, with it's value, in a file.
# First, we have to format the replacemen HEAD_dict[key] propoerly as a monidata string
# print(report_content)
output_file = dir_nam + "/latex_report.tex"
# Write the report content to the output file
with open(output_file, "w") as file:
    file.write(report_content)
print(f"Report_Content written to {output_file}")

############# make the plots #####
##################### 22/08/23 from repgen_V21_graph.py
# run with Python 3.9.15 github_venv :conda
# gIt_evahub > source github_venv/bin/activate
#  evahub> % python -i "backend/python-jsonplot_V1.py"    end with close figures and CTRL+D
#                    interactive in the treminal
# %matplotlibdata = ()

filename = dir_nam + "/EVAL" + str(DataName) + ".json"  # directed flows
try:
    with open(filename, "r") as read_file:
        DATA_dict = json.load(read_file)
except IOError as Fehler:
    print("An IOError occurred: %s" % Fehler)
pass  # previous open("TestUser/JRC_GridStorage/EVAL_06_2023.json", "r") as read_file:

keylist = list(DATA_dict.keys())  # liefert Liste der Schlüssel set( liefert set)
data_list = list(DATA_dict.values())  # liefert die Inhaltedict
# numpy arrays erzeugen
PD_sub = np.asarray(data_list[1])
PD_UIP = np.asarray(data_list[2])
BalD_sub = np.asarray(data_list[3])
BalD_UIP = np.asarray(data_list[4])
Dirflo_day = np.asarray(data_list[5])
Dirflo_hr = np.asarray(data_list[6])
Powflo_day = np.asarray(data_list[7])
Powflo_hr = np.asarray(data_list[8])

# plot in OO style
maxhrs = 31 * 24

# a figure with a single Axes
fig1, ax1 = plt.subplots(figsize=(5, 4), layout="constrained")

ax1.plot(PD_sub[:, 0], PD_sub[:, 1], label="subgrid", color="blue")
ax1.plot(PD_UIP[:, 0], PD_UIP[:, 1], color="red", label="utility")  # etc.
ax1.plot([0, maxhrs], [0, 0], color="black", linewidth=0.9)  # etc.

# Axes
# ax1.set(xlim=(0, maxhrs), xticks=np.arange(1, 8),
#       ylim=(0, 1), yticks=np.arange(0, 0.2))
ax1.set(xlim=(0, 720), ylim=(-1, 1))
ax1.legend(
    labels=[
        "subgrid",
        "utility",
    ],
    loc="upper left",
)
ax1.set_ylabel("Netpower Duration")
ax1.set_xlabel("distribution hours")

plt.savefig(dir_nam + "/Image_fig1.eps", format="eps")
####################################################

#### Figure 2 #########################
fig2, ax2 = plt.subplots(figsize=(5, 4), layout="constrained")
# ax2.plot([0, maxhrs], [0, 0], color='black', linewidth=0.9)  # etc.
ax2.plot(BalD_sub[:, 0], BalD_sub[:, 1], label="subgrid", color="blue")
ax2.plot(BalD_UIP[:, 0], BalD_UIP[:, 1], color="red", label="utility")  # etc.

# Axes
# ax2.set(xlim=(0, maxhrs), xticks=np.arange(1, 8),
#       ylim=(0, 1), yticks=np.arange(0, 0.2))
ax2.set(xlim=(0, 720), ylim=(0, 0.4))
ax2.legend(
    labels=[
        "subgrid",
        "utility",
    ],
    loc="upper left",
)
ax2.set_ylabel("Balance Duration")
ax2.set_xlabel("balanceperiod hours")

plt.savefig(dir_nam + "/Image_fig2.eps", format="eps")
#########################################


#### Figure 3 and 4 #########################
# https://www.pythoncharts.com/matplotlib/stacked-bar-charts-labels/
colors = ["red", "blue", "green"]

fig3, ax3 = plt.subplots(figsize=(5, 4), layout="constrained")  # Data
valu1 = Dirflo_day[0, :]
valu2 = Dirflo_day[1, :]
valu3 = Dirflo_day[2, :]
valu4 = Dirflo_day[3, :]
valu5 = Dirflo_day[4, :]
valu6 = Dirflo_day[5, :]


#######
# https://stackoverflow.com/questions/61130168
# stacked-bar-chart-in-matplotlib-how-to-code-with-lots-and-lots-of-categories
# https://www.tutorialspoint.com/matplotlib/matplotlib_quick_guide.htm

nbr_days = np.size(Dirflo_day[1, :])
day_ind = np.arange(nbr_days)

bot = 0
ind = 0
for avg in [valu1, valu2, valu3]:
    plt.bar(day_ind + 1, abs(avg), color=colors[ind], width=0.7, bottom=bot)
    bot += avg
    ind = ind + 1
# below zero directed flows -< works right
bot = 0
ind = 0
for avg in [valu4, valu5, valu6]:
    plt.bar(day_ind + 1, -abs(avg), color=colors[ind], width=0.7, bottom=bot)
    bot -= avg
    ind = ind + 1

ax3.plot([0, nbr_days], [0, 0], color="black", linewidth=0.9)  # etc.
ax3.set_title("daily power averages")
plt.legend(ncol=3)
ax3.legend(labels=["", "P_a", "P_b ", "P_c"], loc="upper left")

# Axes
# ax3.et(xlim=(0, maxhrs), xticks=np.arange(1, 8),
#       ylim=(0, 1), yticks=np.arange(0, 0.2))
ax3.set(xlim=(0, 31.5), ylim=(-1, 1))  # days'
ax3.set_xlabel("day of month ")

plt.savefig(dir_nam + "/Image_chart1.eps", format="eps")

#########################################
fig = plt.figure()
fig4, ax4 = plt.subplots(figsize=(5, 4), layout="constrained")
# Data
valu1 = Dirflo_hr[0, :]
valu2 = Dirflo_hr[1, :]
valu3 = Dirflo_hr[2, :]
valu4 = Dirflo_hr[3, :]
valu5 = Dirflo_hr[4, :]
valu6 = Dirflo_hr[5, :]

nbr_hrs = np.size(Dirflo_hr[1, :])
hr_ind = np.arange(nbr_hrs)

bot = 0
ind = 0
for avg in [valu1, valu2, valu3]:
    plt.bar(hr_ind, abs(avg), color=colors[ind], width=0.7, bottom=bot)
    bot += avg
    ind = ind + 1

plt.bar  # zero bar'
# below zero directed flows -< works right
bot = 0
ind = 0
for avg in [valu4, valu5, valu6]:
    plt.bar(hr_ind, -abs(avg), color=colors[ind], width=0.7, bottom=bot)
    bot -= avg
    ind = ind + 1
plt.bar(hr_ind, 0 * avg, color="black", width=1)  # zero bar'
# ax4.plot([0, nbr_hrs], [0, 0], color='black', linewidth=0.9)  # etc.
ax4.set_title("hourly power averages")
plt.legend(ncol=3)
# ax4.legend(labels=['','P_a', 'P_b ','P_c'],loc='upper left')

# Axes
# ax4.et(xlim=(0, maxhrs), xticks=np.arange(1, 8),
#       ylim=(0, 1), yticks=np.arange(0, 0.2))
ax4.set(xlim=(-0.5, 24), ylim=(-1, 1))  # hours'
ax4.set_xlabel("hour of day ")


plt.savefig(dir_nam + "/Image_chart2.eps", format="eps")
#############################

## now call pandoc
report_file = "Report" + DataName + ".pdf"

# call('pandoc -i '+output_file+' -o '+report_file ,shell=True) # after insert
old_dir = os.getcwd()
os.chdir(dir_nam)
call("pdflatex latex_report.tex", shell=True)  # after insert
call("mv latex_report.pdf " + report_file, shell=True)  # after insert

call("open -a Preview " + report_file, shell=True)
os.chdir(old_dir)
#############################

sys.exit()
