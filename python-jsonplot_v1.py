# in /Users/jsachau/_INITIATIVES/TecVerb_EnergieSicherheit/JRC_Sabbatical/JS_work/gIt_evahub/evahub/backend'

import json

import matplotlib.pyplot as plt
import numpy as np

# run with Python 3.9.15 github_venv :conda
# backend > source github_venv/bin/activate
#  evahub> % python -i "backend/python-jsonplot.py"    end with CTRL+D
#                    interactive in the treminal
# %matplotlibdata = ()
with open(
    "backend/documents/TestUser/JRC_GridStorage/Eval_06_2023.json", "r"
) as read_file:
    data = json.load(read_file)
keylist = list(data.keys())  # liefert Liste der Schlüssel set( liefert set)
data_list = list(data.values())  # liefert die Inhaltedict
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
#########################################


#### Figure 3 and 4 #########################
# https://www.pythoncharts.com/matplotlib/stacked-bar-charts-labels/
colors = ["red", "blue", "green"]

fig3, ax3 = plt.subplots(figsize=(5, 4), layout="constrained")

# Data
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
#########################################

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

plt.show()
plt.close()
