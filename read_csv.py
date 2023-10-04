# in folder voicelab/Huanchen/Thyroidectomy/audio/, there are a lot of subjects' csv files.
# iterate the folder and find the csv files, then read the csv files and get the data.
# the file name with 'pre_VRP.csv' will be save in a list called pre_VRP_list
# the file name with 'post_VRP.csv' will be save in a list called post_VRP_list
# each list will contain 1: the name of the subject, 2: the min value of the first column, 
# 3: the max value of the first column, 4: the min value of the second column, 5: the max value of the second column
# the first row of the list will be 1: name, 2: min_MIDI, 3: max_MIDI, 4: min_dB, 5: max_dB


import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# the path of the folder
# path = '/Volumes/voicelab/Huanchen/Thyrovoice/bysubject_vrp_cycle5/'
path = r'L:\Huanchen\Thyrovoice\bysubject_vrp_cycle5' # overlap folder, colomn from 3 to 9
# path = r'L:\Huanchen\Thyrovoice\audio' # non-overlap folder, colomn from 4 to 10
metrics_name = ['Crest', 'SB', 'CPPs', 'Entropy', 'dEGGmax', 'Qcontact']
def collect_VRP_data_v1(path):
    """ Collect VRP data from CSV files in a given folder and its subfolders. For a common folder structure."""
    # Initialize lists to hold filenames and data
    pre_VRP_list = []
    post_VRP_list = []
    pre_VRP_data = []
    post_VRP_data = []
    pre_name = []
    post_name = []

    # Iterate over subfolders to find relevant CSV files
    for folder_name in os.listdir(path):
        if folder_name != '.DS_Store':
            subfolder = os.listdir(os.path.join(path, folder_name))
            for filename in subfolder:
                if filename.endswith('pre_VRP.csv'):
                    pre_VRP_list.append(f"{folder_name}/{filename}")
                elif filename.endswith('pos_VRP.csv'):
                    post_VRP_list.append(f"{folder_name}/{filename}")

    # Read pre_VRP CSV files
    for filepath in pre_VRP_list:
        with open(os.path.join(path, filepath), 'r') as f:
            reader = csv.reader(f, delimiter=';')
            data = list(reader)
            data.pop(0)  # Remove header
            pre_VRP_data.append(data)

    # Read post_VRP CSV files
    for filepath in post_VRP_list:
        with open(os.path.join(path, filepath), 'r') as f:
            reader = csv.reader(f, delimiter=';')
            data = list(reader)
            data.pop(0)  # Remove header
            post_VRP_data.append(data)

    # Extract subject names from pre_VRP filenames
    for filepath in pre_VRP_list:
        pre_name.append(filepath[:6])

    # Extract subject names from post_VRP filenames
    for filepath in post_VRP_list:
        post_name.append(filepath[:6])

    return pre_VRP_data, post_VRP_data, pre_name, post_name

def collect_VRP_data_v2(path):
    """ 
    Collect VRP data from CSV files in a given folder, this is for the csv that are overlapping
    where the path is /Volumes/voicelab/Huanchen/Thyrovoice/bysubject_vrp_cycle5/
    """
     # Initialize lists to hold filenames and data
    pre_VRP_list = []
    post_VRP_list = []
    pre_VRP_data = []
    post_VRP_data = []
    pre_name = []
    post_name = []

    # iterate the folder and find matched csv files
    for filename in os.listdir(path):
        # if filename contains pre and 'k=2', then it is a pre_VRP file
        if 'pre' in filename and 'k=2' in filename:
            pre_VRP_list.append(filename)
        # if filename contains post and 'k=2', then it is a post_VRP file
        elif 'post' in filename and 'k=2' in filename:
            post_VRP_list.append(filename)
    
    # Read pre_VRP CSV files
    for filepath in pre_VRP_list:
        with open(os.path.join(path, filepath), 'r') as f:
            reader = csv.reader(f, delimiter=';')
            data = list(reader)
            data.pop(0)  # Remove header
            # convert to float
            data = [[float(j) for j in i] for i in data]
            pre_VRP_data.append(data)

    # Read post_VRP CSV files
    for filepath in post_VRP_list:
        with open(os.path.join(path, filepath), 'r') as f:
            reader = csv.reader(f, delimiter=';')
            data = list(reader)
            data.pop(0)  # Remove header
            data = [[float(j) for j in i] for i in data]
            post_VRP_data.append(data)

    # Extract subject names from pre_VRP filenames
    for filepath in pre_VRP_list:
        pre_name.append(filepath[:6])

    # Extract subject names from post_VRP filenames
    for filepath in post_VRP_list:
        post_name.append(filepath[:6])

    return pre_VRP_data, post_VRP_data, pre_name, post_name

def collect_VRP_data_v3(path, list_of_patients):
    """ 
    Collect VRP data from CSV files in a given folder, this is for the csv that are overlapping
    where the path is /Volumes/voicelab/Huanchen/Thyrovoice/bysubject_vrp_cycle5/
    DIFFERENCE from v2: select the patients by criteria, such as total or partial.
    """
     # Initialize lists to hold filenames and data
    pre_VRP_list = []
    post_VRP_list = []
    pre_VRP_data = []
    post_VRP_data = []

    if list_of_patients:
        if len(list_of_patients) == 1:
            # for later cases
            pass
        else:
            # iterate the folder and find matched csv files with the list of patients
            for i in range(len(list_of_patients)):
                patient_pre_VRP_list = []
                patient_post_VRP_list = []
                for filename in os.listdir(path):
                    name = filename[:6]
                    # if filename contains pre and 'k=2', then it is a pre_VRP file
                    if 'pre' in filename and 'k=2' in filename and name in list_of_patients[i]:
                        patient_pre_VRP_list.append(filename)
                    # if filename contains post and 'k=2', then it is a post_VRP file
                    elif 'post' in filename and 'k=2' in filename and name in list_of_patients[i]:
                        patient_post_VRP_list.append(filename)
                pre_VRP_list.append(patient_pre_VRP_list)
                post_VRP_list.append(patient_post_VRP_list)

    for i in range(len(list_of_patients)):
        patient_pre_VRP_data = []
        patient_post_VRP_data = []
        # Read pre_VRP CSV files
        for filepath in pre_VRP_list[i]:
            with open(os.path.join(path, filepath), 'r') as f:
                reader = csv.reader(f, delimiter=';')
                data = list(reader)
                data.pop(0)  # Remove header
                # convert to float
                data = [[float(j) for j in i] for i in data]
                patient_pre_VRP_data.append(data)
        pre_VRP_data.append(patient_pre_VRP_data)

        # Read post_VRP CSV files
        for filepath in post_VRP_list[i]:
            with open(os.path.join(path, filepath), 'r') as f:
                reader = csv.reader(f, delimiter=';')
                data = list(reader)
                data.pop(0)  # Remove header
                data = [[float(j) for j in i] for i in data]
                patient_post_VRP_data.append(data)
        post_VRP_data.append(patient_post_VRP_data)

    return pre_VRP_data, post_VRP_data

def calculate_and_save_metrics(pre_VRP_data, post_VRP_data, pre_name, post_name):
    """ Calculate metrics from VRP data and save to CSV file. 
    metrics saved for each subject"""
    pre_metrics = []
    post_metrics = []

    # Calculate weighted averages for pre_VRP_data
    for i in pre_VRP_data:
        metrics = np.array([[float(j[k]) for k in range(4, 10)] for j in i])
        metrics = np.average(metrics, axis=0, weights=metrics[:, 2])
        pre_metrics.append(metrics.tolist())

    # Calculate weighted averages for post_VRP_data
    for i in post_VRP_data:
        metrics = np.array([[float(j[k]) for k in range(4, 10)] for j in i])
        metrics = np.average(metrics, axis=0, weights=metrics[:, 2])
        post_metrics.append(metrics.tolist())

    # Insert subject names
    for i in range(len(pre_name)):
        pre_metrics[i].insert(0, pre_name[i])
        post_metrics[i].insert(0, post_name[i])

    # Add headers
    pre_metrics.insert(0, ['prename', 'Crest', 'SB', 'CPPs', 'Entropy', 'dEGGmax', 'Qcontact'])
    post_metrics.insert(0, ['postname', 'Crest', 'SB', 'CPPs', 'Entropy', 'dEGGmax', 'Qcontact'])

    return pre_metrics, post_metrics

def main():

    # pre_metrics, post_metrics = calculate_and_save_metrics(pre_VRP_data, post_VRP_data, pre_name, post_name)
    pre_VRP_data, post_VRP_data, pre_name, post_name = collect_VRP_data_v2(path)
    pre_metrics = []
    post_metrics = []

    # from pre_VRP_data and post_VRP_data, save the all the metrics data into only one np list in pre_metrics and post_metrics without averaging:
    # pre_metrics and post_metrics should contain only one list
    for i in pre_VRP_data:
        metrics = np.array([[float(j[k]) for k in range(3, 9)] for j in i])
        pre_metrics.append(metrics.tolist())

    for i in post_VRP_data:
        metrics = np.array([[float(j[k]) for k in range(3, 9)] for j in i])
        post_metrics.append(metrics.tolist())

    pre_metrics = [inner for outer in pre_metrics for inner in outer]
    post_metrics = [inner for outer in post_metrics for inner in outer]

    # ######## below is muliply the metrics by the count, i.e. if the count is 3, then append 3 times of the metrics to the list
    # for i in pre_VRP_data:    
    #     metrics = np.array([[float(j[k]) for k in range(2, 9)] for j in i])
    #     # for each item in metrics, the first col is the count, append the count times of metrics to pre_metrics
    #     for j in range(len(metrics)):
    #         for k in range(int(metrics[j][0])):
    #             pre_metrics.append(metrics[j, 1:].tolist())

    # for i in post_VRP_data:
    #     metrics = np.array([[float(j[k]) for k in range(2, 9)] for j in i])
    #     for j in range(len(metrics)):
    #         for k in range(int(metrics[j][0])):
    #             post_metrics.append(metrics[j, 1:].tolist())

    # save pre_metrics and post_metrics into csv files, iterate each element is one line
    # with open('pre_metrics.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     for i in pre_metrics:
    #         for j in i:
    #             writer.writerow(j)

    # with open('post_metrics.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     for i in post_metrics:
    #         for j in i:
    #             writer.writerow(j)

    # plot violin plot for each metrics in pre and post, pre is blue, post is orange, 
    # 6 metrics, 6 violin plots, pre is on the left, post is on the right

    # for i in range(6):
    #     plt.subplot(2, 3, i+1)
    #     # plot the first column of pre_metrics and post_metrics
    #     # only plot half of the violin, the left half is the pre, the right half is the post
    #     plt.violinplot([j[i] for j in pre_metrics], positions=[0.8], showmeans=True, showextrema=True)
    #     plt.violinplot([j[i] for j in post_metrics], positions=[1.2], showmeans=True, showextrema=True)
    #     plt.xticks([0.5, 1.5], ['pre', 'post'])
    #     plt.title(metrics_name[i])
        
    #     if i == 0 or i == 3:
    #         plt.ylabel('value')
    # plt.show()

    # calculate the difference and significance between pre and post for the same colomn using all the subjects.
    # the result will be saved in a list called difference
    difference = []
    for i in range(len(pre_metrics)):
        difference.append([pre_metrics[i][j] - post_metrics[i][j] for j in range(len(pre_metrics[i]))])



    # calculate the mean and std of the difference by columns, saved in mean and std
    # mean has 6 elements, each element is the mean of the difference of each column
    diff_mean = np.mean(difference, axis=0)
    diff_std = np.std(difference, axis=0)    


    mean_pre = np.mean(pre_metrics, axis=0)
    std_pre = np.std(pre_metrics, axis=0)

    mean_post = np.mean(post_metrics, axis=0)
    std_post = np.std(post_metrics, axis=0)

    # calculate the p value of the difference by column, saved in p_value
    p_value = []
    for i in range(len(difference[0])):
        p_value.append(stats.ttest_1samp([j[i] for j in difference], 0)[1])

    # calculate the confidence interval of the difference by column, saved in confidence_interval
    confidence_interval = []
    for i in range(len(difference[0])):
        confidence_interval.append(stats.t.interval(0.95, len(difference)-1, loc=np.mean([j[i] for j in difference]), scale=stats.sem([j[i] for j in difference])))

    # and keep the decimal to 5 digits
    diff_mean = [round(i, 5) for i in diff_mean]
    diff_std = [round(i, 5) for i in diff_std]
    mean_pre = [round(i, 5) for i in mean_pre]
    std_pre = [round(i, 5) for i in std_pre]
    mean_post = [round(i, 5) for i in mean_post]
    std_post = [round(i, 5) for i in std_post]
    p_value = [round(i, 5) for i in p_value]
    confidence_interval = [[round(i[0], 5), round(i[1], 5)] for i in confidence_interval]

    # save the results into a csv file
    output_filename = 'VRP_metrics_non_overlap_statistics.csv'
    # first column is the name of the metrics, i.e. Crest, SB, CPPs, Entropy, dEGGmax, Qcontact
    # second column is the pre mean, third column is the pre std, fourth column is the post mean, fifth column is the post std, sixth column is the difference mean, seventh column is the difference std, eighth column is the p value

    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'pre_mean', 'pre_std', 'post_mean', 'post_std', 'diff_mean', 'diff_std', 'p_value', 'confidence_interval'])
        writer.writerow(['Crest', mean_pre[0], std_pre[0], mean_post[0], std_post[0], diff_mean[0], diff_std[0], p_value[0], confidence_interval[0]])
        writer.writerow(['SB', mean_pre[1], std_pre[1], mean_post[1], std_post[1], diff_mean[1], diff_std[1], p_value[1], confidence_interval[1]])
        writer.writerow(['CPPs', mean_pre[2], std_pre[2], mean_post[2], std_post[2], diff_mean[2], diff_std[2], p_value[2], confidence_interval[2]])
        writer.writerow(['Entropy', mean_pre[3], std_pre[3], mean_post[3], std_post[3], diff_mean[3], diff_std[3], p_value[3], confidence_interval[3]])
        writer.writerow(['dEGGmax', mean_pre[4], std_pre[4], mean_post[4], std_post[4], diff_mean[4], diff_std[4], p_value[4], confidence_interval[4]])
        writer.writerow(['Qcontact', mean_pre[5], std_pre[5], mean_post[5], std_post[5], diff_mean[5], diff_std[5], p_value[5], confidence_interval[5]])



    # Combine pre_metrics and post_metrics
    # metrics = []
    # for i in range(len(pre_metrics)):
    #     metrics.append(pre_metrics[i] + post_metrics[i])

    # output_filename = 'VRP_metrics.csv'
    # # Save to CSV
    # with open(output_filename, 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(metrics)

if __name__ == "__main__":
    main()

def process_and_save_VRP_data_MIDI_dB(pre_VRP_data, post_VRP_data, pre_name):
    def process_data(VRP_data):
        VRP_MIDI = []
        VRP_dB = []
        VRP_MIDI_avg = []
        VRP_MIDI_std = []
        VRP_dB_avg = []
        VRP_dB_std = []

        for i in VRP_data:
            MIDI = []
            dB = []
            for j in i:
                MIDI.append(float(j[0]))
                dB.append(float(j[1]))

            VRP_MIDI.append([min(MIDI), max(MIDI)])
            VRP_dB.append([min(dB), max(dB)])

            VRP_MIDI_avg.append(np.mean(MIDI))
            VRP_MIDI_std.append(np.std(MIDI))
            VRP_dB_avg.append(np.mean(dB))
            VRP_dB_std.append(np.std(dB))

        VRP = []
        for i in range(len(VRP_MIDI)):
            VRP.append([pre_name[i], VRP_MIDI[i][0], VRP_MIDI[i][1], VRP_dB[i][0], VRP_dB[i][1]])

        for i in range(len(VRP_MIDI_avg)):
            VRP[i].extend([VRP_MIDI_avg[i], VRP_MIDI_std[i], VRP_dB_avg[i], VRP_dB_std[i]])

        return VRP

    pre_VRP = process_data(pre_VRP_data)
    post_VRP = process_data(post_VRP_data)

    pre_VRP.insert(0, ['name', 'min_MIDI', 'max_MIDI', 'min_dB', 'max_dB', 'avg_MIDI', 'std_MIDI', 'avg_dB', 'std_dB'])
    post_VRP.insert(0, ['name', 'min_MIDI', 'max_MIDI', 'min_dB', 'max_dB', 'avg_MIDI', 'std_MIDI', 'avg_dB', 'std_dB'])

    with open('pre_VRP.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(pre_VRP)

    with open('post_VRP.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(post_VRP)

# save mean and std of MIDI, dB
# process_and_save_VRP_data_MIDI_dB(pre_VRP_data, post_VRP_data, pre_name)