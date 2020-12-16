import matplotlib.pyplot as plt
import numpy as np

####################################
#UTILS
################################
def max_groupes(grouped_values):
    fmax = -1
    for values in grouped_values:
        amax = max(values)
        if fmax < amax:
            fmax = amax
    return fmax


######################################
#MAIN FUNCTIONS
######################################

#altezza istogrammi, nomi istrogrammi, titolo png, label x, label y, valore minimo y, valore massimo y
def draw_histograms(values, names, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, COLOR=None):

    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)
    
    len_names = len(names)
    len_values = len(values)

    if len_names != len_values:
        print("ERROR: len_names != len_values")
        return

    x_pos = np.arange(len_names)
    if COLOR != None:
        plt.bar(x_pos, values, width = 0.5, color=COLOR)
    else:
        plt.bar(x_pos, values, width = 0.5)
    plt.xticks(x_pos, names, rotation= '45')


    plt.title(TITLE, fontsize=18, y=1.03)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    #locs, labels = plt.yticks()
    #print(locs)
    #yint = []
    #for each in locs:
    #    yint.append(int(each))
    #plt.yticks(yint) #serve per decidere che valori mettere sulle y


    plt.show()
    plt.close()


def draw_grouped_histograms(grouped_values, names, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, legend_labels, colors=None):
    
    WIDTH = 0.35
    DISTANCE_BETWEEN_GROUPS = 0.15
    START_DISTANCE = DISTANCE_BETWEEN_GROUPS


    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)


    len_names = len(names)
    num_histo_per_group = len(grouped_values)

    if len(legend_labels) != num_histo_per_group:
        print("len(legend_labels) != num_histo_per_group")
        return

    group_space = num_histo_per_group * WIDTH + DISTANCE_BETWEEN_GROUPS
    x_pos = np.arange(START_DISTANCE, group_space * len_names, group_space)


    for i in range(0, num_histo_per_group):
        if len(grouped_values[i]) != len_names:
            print("ERROR: grouped_values != len_names")
            return
        if colors != None:
            plt.bar(x_pos + WIDTH*i, grouped_values[i], width=WIDTH, label=legend_labels[i], color=colors[i])
        else:
            plt.bar(x_pos + WIDTH*i, grouped_values[i], width=WIDTH, label=legend_labels[i])


    if num_histo_per_group % 2 == 0:
        number = num_histo_per_group/2 * WIDTH - WIDTH/2
        plt.xticks(x_pos + number, names, rotation= '45')
    else:
        number = int(num_histo_per_group / 2) * WIDTH #+ WIDTH/2
        plt.xticks(x_pos + number, names, rotation= '45')


    ax.legend()

    plt.title(TITLE, fontsize=18, y=1.03)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    plt.show()
    plt.close()


def draw_lines(y_number_values, x_number_values, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, COLOR=None, COLOR_POINT=None):

    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)
    

    len_x = len(x_number_values)
    len_y = len(y_number_values)

    if len_x != len_y:
        print("ERROR: len_x != len_y")
        return

    #x_pos = range(0, len_x)
    x_pos = np.arange(len_x)

    if COLOR != None and COLOR_POINT != None:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, color=COLOR, marker = 'o', markerfacecolor = COLOR_POINT)
    elif COLOR != None:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, color=COLOR, marker = 'o')
    elif COLOR_POINT != None:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, marker = 'o', markerfacecolor = COLOR_POINT)
    else:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, marker = 'o')

    plt.xticks(x_pos, x_number_values, rotation= '45')

    plt.title(TITLE, fontsize=18, y=1.03)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    plt.tick_params(axis='both', labelsize=12)

    plt.show()
    plt.close()


