# load vrpstats.xlsx and plot the data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# the path of the folder
path = r'L:\Huanchen\Thyrovoice\VRPstats.xlsx'
# data is in sheet named "main data (2)"
data = pd.read_excel(path, sheet_name="main data (2)")
# colomn name is the second row
data.columns = data.iloc[0]
data = data.drop(0)

# Extracting the relevant first columns and handling non-numeric entries
diff_vhi_numeric = pd.to_numeric(data["Diff VHI"], errors='coerce')
CPP_change_post_pre_numeric = pd.to_numeric(data["cppdiff"], errors='coerce')
CSE_change_post_pre_numeric = pd.to_numeric(data["csediff"], errors='coerce')
SB_change_post_pre_numeric = pd.to_numeric(data["sbdiff"], errors='coerce')
QC_change_post_pre_numeric = pd.to_numeric(data["qcdiff"], errors='coerce')
Crest_change_post_pre_numeric = pd.to_numeric(data["crestdiff"], errors='coerce')
dEGG_change_post_pre_numeric = pd.to_numeric(data["deggmax"], errors='coerce')

# Plotting the linear regression plots in subplots, y axis is VHI, set the title, discard the extreme values
fig, axs = plt.subplots(2, 3, figsize=(12, 7))
sns.regplot(x=CPP_change_post_pre_numeric, y=diff_vhi_numeric, ax=axs[0, 0], ci=None, scatter_kws={'alpha':0.2})
axs[0, 0].set_title('CPP')
sns.regplot(x=CSE_change_post_pre_numeric, y=diff_vhi_numeric, ax=axs[0, 1], ci=None, scatter_kws={'alpha':0.2})
axs[0, 1].set_title('CSE')
sns.regplot(x=SB_change_post_pre_numeric, y=diff_vhi_numeric, ax=axs[0, 2], ci=None, scatter_kws={'alpha':0.2})
axs[0, 2].set_title('SB')
sns.regplot(x=QC_change_post_pre_numeric, y=diff_vhi_numeric, ax=axs[1, 0], ci=None, scatter_kws={'alpha':0.2})
axs[1, 0].set_title('QC')
sns.regplot(x=Crest_change_post_pre_numeric, y=diff_vhi_numeric, ax=axs[1, 1], ci=None, scatter_kws={'alpha':0.2})
axs[1, 1].set_title('Crest')
sns.regplot(x=dEGG_change_post_pre_numeric, y=diff_vhi_numeric, ax=axs[1, 2], ci=None, scatter_kws={'alpha':0.2})
axs[1, 2].set_title('dEGG')


# set the label of the x axis and y axis
for ax in axs.flat:
    ax.set(xlabel='Change post-pre', ylabel='Diff VHI')
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.label_outer()

# set the title
fig.suptitle('VHI&metrics change post-pre')

# show the plot
plt.show()

# plt.savefig('VHI&Area change', format='jpg')