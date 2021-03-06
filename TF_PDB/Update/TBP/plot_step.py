

import pandas as pd
import numpy as np
import pylab as pl
import os, sys
from seq_gap import *

#subname = "HG-DNA"
subname = "AdMLP"
#pdblist = ['6njq','xcca','xccb']
pdblist = ['1qne','xac1','xcc2']
#colorlist = ['royalblue','cyan','plum']
colorlist = ['red','orange','violet']

pdbinfo = pd.read_csv("../Data/refine_pdbinfo_final.csv")
bseqinfo = pd.read_csv("../Data/tf_bseq.csv")
pdbinfo['bseq1_full'] = bseqinfo['bseq1']
pdbinfo['bseq2_full'] = bseqinfo['bseq2']
pdbinfo['bidx1_full'] = bseqinfo['bidx1']
pdbinfo['bidx2_full'] = bseqinfo['bidx2']

pdbinfo = pdbinfo.loc[pdbinfo.pdbid.isin(pdblist)].reset_index(drop=True)

df = pd.read_csv('../Data/tf_local.csv')
df_range = pd.read_csv("../../../Survey/Survey_goldWC/stem/free/Canonical_all_bp_params.csv")

bp_params = ['shift','slide','rise','tilt','roll','twist']
ylim_list = [[-4,4],[-4,4],[0,8],[-60,60],[-60,60],[-20,60]]

# find gap in helices
gappdb = pdbinfo.loc[~(pdbinfo.bseq1 == pdbinfo.bseq1_full)]['pdbid'].tolist()


# generate plot for each bp params
for idx, param in enumerate(bp_params):

    print("--- Working on %s [%d/%d] ---"%(param,idx,len(bp_params)))

    fig = pl.figure(1,figsize=(6,2))
    fig.patch.set_facecolor('none')


    for i in range(len(pdbinfo)):

        pdbid = pdbinfo['pdbid'].ix[i]
        name = pdbinfo['name'].ix[i]

        bseq1 = pdbinfo['bseq1'].ix[i]
        bseq2 = pdbinfo['bseq2'].ix[i]

        bseq1_full = pdbinfo['bseq1_full'].ix[i]
        bseq2_full = pdbinfo['bseq2_full'].ix[i]

        bidx1 = list(map(int,pdbinfo['bidx1'].ix[i].split('|')))
        bidx2 = list(map(int,pdbinfo['bidx2'].ix[i].split('|')))

        bidx1_full = list(map(int,pdbinfo['bidx1_full'].ix[i].split('|')))
        bidx2_full = list(map(int,pdbinfo['bidx2_full'].ix[i].split('|')))
        
        if pdbid in gappdb:

            seqrange = np.array(range(len(bseq1_full)))
            subdf = df.loc[df['pdbid'] == pdbid]
            param_value = subdf[param].tolist()
            param_value = [np.nan] + param_value + [np.nan]
            pos = find_gap(bidx1,bidx1_full)
            param_value = fill_gap(param_value,pos)

        else:

            seqrange = np.array(range(len(bseq1)))
            subdf = df.loc[df['pdbid'] == pdbid]
            param_value = subdf[param].tolist()
            param_value = [np.nan] + param_value + [np.nan]

        if pdbid == "6njq":
            param_value[7] = np.nan
            param_value[8] = np.nan
        if pdbid == "xac1":
            param_value[7] = np.nan
            param_value[9] = np.nan


        ylim_min = ylim_list[idx][0]
        ylim_max = ylim_list[idx][1]
        ylim_mid = (ylim_min + ylim_max) / 2.

        ax1 = fig.add_subplot(1,1,1)
        ax1.patch.set_facecolor('none')
        ax2 = ax1.twiny()
        if i == 0:
            ax1.set_xticks(seqrange)
            ax1.set_xticklabels(list(bseq1_full),fontsize=15)

        ax1.plot(seqrange[:-2]+0.5,param_value[:-2],'-o',color=colorlist[i],
                 markersize=10,linewidth=3,markeredgecolor='none')

        ax1.set_ylabel(param)
        ax1.set_xlim(0,len(bseq1_full)-1)
        ax1.set_ylim(ylim_min,ylim_max)
        ax1.set_yticks([ylim_min,ylim_mid,ylim_max])
        ax1.set_yticklabels([str(ylim_min),str(ylim_mid),str(ylim_max)])
        ax2.set_xlim(ax1.get_xlim())
        ax2.set_xticks([])
        if i == 0:
            ax2.set_xticks(seqrange)
            ax2.set_xticklabels(list(bseq2_full),fontsize=15)

        ax1.spines['left'].set_linewidth(3)
        ax1.spines['right'].set_linewidth(3)
        ax1.spines['top'].set_linewidth(3)
        ax1.spines['bottom'].set_linewidth(3)

        ax1.tick_params(length=6,width=3)
        ax2.tick_params(length=6,width=3)


    fig.tight_layout()


    pl.savefig('./tf_final_tbp_%s_%s.pdf'%(subname,param))

    pl.clf()

