import matplotlib
import matplotlib.pyplot as plt
import numpy as np


SAVE = True
PRINT = False

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
def draw_histograms(values, names, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, COLOR=None, PATH=None, ISLABEL=True, ISSCIE=True):

    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.1)

    len_names = len(names)
    len_values = len(values)

    if len_names != len_values:
        print("ERROR: len_names != len_values")
        plt.close()
        return

    x_pos = np.arange(len_names)
    if COLOR != None:
        plt.bar(x_pos, values, width = 0.5, color=COLOR)
    else:
        plt.bar(x_pos, values, width = 0.5)
    plt.xticks(x_pos, names, rotation= '45')

    if ISLABEL:
        for i, y in enumerate(values):
            if ISSCIE:
                plt.text(i, y + 0.02*YTOP, f"{y:.1g}", ha='center', fontweight='bold')
            else:
                plt.text(i, y + 0.02*YTOP, f"{y:.1f}", ha='center', fontweight='bold')


    plt.title(TITLE, fontsize=18, y=1.13)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    #locs, labels = plt.yticks()
    #print(locs)
    #yint = []
    #for each in locs:
    #    yint.append(int(each))
    #plt.yticks(yint) #serve per decidere che valori mettere sulle y

    if SAVE and PATH != None:
        #plt.savefig(PATH, bbox_inches='tight', dpi=150)
        plt.savefig(PATH, bbox_inches='tight')
    if PRINT:
        plt.show()
    plt.close()


def draw_grouped_histograms(grouped_values, names, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, legend_labels, colors=None, PATH=None):

    WIDTH = 0.35
    DISTANCE_BETWEEN_GROUPS = 0.15
    START_DISTANCE = DISTANCE_BETWEEN_GROUPS


    ax = plt.subplot(111)
    #ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)


    len_names = len(names)
    num_histo_per_group = len(grouped_values)

    if len(legend_labels) != num_histo_per_group:
        print("len(legend_labels) != num_histo_per_group")
        plt.close()
        return

    if colors != None and len(colors) != num_histo_per_group:
        print("len(colors) != num_histo_per_group")
        plt.close()
        return

    group_space = num_histo_per_group * WIDTH + DISTANCE_BETWEEN_GROUPS
    x_pos = np.arange(START_DISTANCE, group_space * len_names, group_space)


    for i in range(0, num_histo_per_group):
        if len(grouped_values[i]) != len_names:
            print("ERROR: grouped_values != len_names")
            plt.close()
            return

        #width_list = [WIDTH]*len_names
        if colors != None:
            plt.bar(x_pos + WIDTH*i, grouped_values[i], width=WIDTH, label=legend_labels[i], color=colors[i])
        else:
            plt.bar(x_pos + WIDTH*i, grouped_values[i], width=WIDTH, label=legend_labels[i])

        #for j, y in enumerate(grouped_values[i]):
        #    positions = x_pos + WIDTH*i
        #    plt.text(positions[j], y + 0.02*YTOP, f"{y:.1g}", ha='center', fontweight='bold')

    if num_histo_per_group % 2 == 0:
        number = num_histo_per_group/2 * WIDTH - WIDTH/2
        plt.xticks(x_pos + number, names, rotation= '45')
    else:
        number = int(num_histo_per_group / 2) * WIDTH #+ WIDTH/2
        plt.xticks(x_pos + number, names, rotation= '45')


    ax.legend()

    plt.title(TITLE, fontsize=18, y=1.2)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    if SAVE and PATH != None:
        plt.savefig(PATH, bbox_inches='tight')
    if PRINT:
        plt.show()
    plt.close()


def draw_grouped_lines(y_grouped_number_values, x_number_values, TITLE, XLABEL, YLABEL,YBOTTOM=None,YTOP=None, colors=None, PATH=None,markers=None,legend=None,y_grouped_tick_labels=None,x_tick_labels=None,marker_labels=None):

    ax = plt.subplot(111)
    if YBOTTOM != None and YTOP != None:
      ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.margins(0.05)
    ax.yaxis.set_label_coords(0, 1.1)

    len_x = len(x_number_values)

    number_grouped = len(y_grouped_number_values)

    if colors != None and len(colors) != number_grouped:
        print("len(colors) != num_histo_per_group")
        plt.close()
        return
    if markers!=None:
        len_m=len(markers)
        if len_m != number_grouped:
            print("number of markers does not match the number of groups")
            return

    for i in range(0, number_grouped):
        if markers!=None:
            chosen_marker=markers[i]
        else:
            chosen_marker='o'


        if legend!=None:
          chosen_label=legend[i]
        else:
          chosen_label=None

        y_number_values = y_grouped_number_values[i]

        len_y = len(y_number_values)
        if len_x != len_y:
            print(f"ERROR: len_x ({len_x}) != len_y ({len_y})")
            plt.close()
            return


        if colors != None:
            plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, color=colors[i], marker = chosen_marker,label=chosen_label)
        else:
            plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, marker = chosen_marker,label=chosen_label)
        if marker_labels != None:
          for index in range(0,len(marker_labels[i])):
            plt.text(x_number_values[index],y_number_values[index],marker_labels[i][index])

    if y_grouped_tick_labels!=None:
      y_ticks_pos=list(filter(lambda x: x!=None,np.array(y_grouped_number_values).flatten()))
      y_ticks_labels=list(filter(lambda x:x!=None,np.array(y_grouped_tick_labels).flatten()))
      plt.yticks(y_ticks_pos,y_ticks_labels)

    #if COLOR != None and COLOR_POINT != None:
    #    plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, color=COLOR, marker = 'o', markerfacecolor = COLOR_POINT)
    #elif COLOR != None:
    #    plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, color=COLOR, marker = 'o')
    #elif COLOR_POINT != None:
    #    plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, marker = 'o', markerfacecolor = COLOR_POINT)
    #else:
    #    plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, marker = 'o')


    if legend!=None:
      plt.legend()

    if x_tick_labels != None:
      plt.xticks(x_number_values,x_tick_labels)
    else:
      plt.xticks(x_number_values, x_number_values, rotation= '45')

    plt.title(TITLE, fontsize=18, y=1.13)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12,rotation=0)

    plt.tick_params(axis='both', labelsize=12)

    if SAVE and PATH != None:
        plt.savefig(PATH, bbox_inches='tight')
    if PRINT:
        plt.show()
    plt.close()


def draw_lines(y_number_values, x_number_values, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, COLOR=None, COLOR_POINT=None, PATH=None):

    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)


    len_x = len(x_number_values)
    len_y = len(y_number_values)

    if len_x != len_y:
        print("ERROR: len_x != len_y")
        plt.close()
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

    plt.title(TITLE, fontsize=18, y=1.13)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    plt.tick_params(axis='both', labelsize=12)

    if SAVE and PATH != None:
        plt.savefig(PATH, bbox_inches='tight')
    if PRINT:
        plt.show()
    plt.close()

def draw_lines_scatterplot(y_number_values, x_number_values, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, COLOR=None, COLOR_POINT=None, PATH=None):

    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)


    len_x = len(x_number_values)
    len_y = len(y_number_values)

    if len_x != len_y:
        print("ERROR: len_x != len_y")
        plt.close()
        return

    #x_pos = range(0, len_x)
    x_pos = np.arange(0.0, len_x, len_x*0.19)

    if COLOR != None and COLOR_POINT != None:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, color=COLOR, marker = 'o', markerfacecolor = COLOR_POINT)
    elif COLOR != None:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, color=COLOR, marker = 'o')
    elif COLOR_POINT != None:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7, marker = 'o', markerfacecolor = COLOR_POINT)
    else:
        plt.plot(x_number_values, y_number_values, '.-b', linewidth=1, markersize=7)

    plt.xticks(x_pos)

    plt.title(TITLE, fontsize=18, y=1.13)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    plt.tick_params(axis='both', labelsize=12)

    if SAVE and PATH != None:
        plt.savefig(PATH, bbox_inches='tight')
    if PRINT:
        plt.show()
    plt.close()


def draw_scatterplot(y_number_values, x_number_values, labels, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, colors=None, PATH=None):
    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)

    len_x = len(x_number_values)
    len_y = len(y_number_values)

    if len_x != len_y:
        print("ERROR: len_x != len_y")
        plt.close()
        return

    ax.scatter(x = x_number_values, y = y_number_values)

    #if len(labels) != len_x:
    #    print("ERROR: len(labels) != len_y")
    #    plt.close()
    #    return

    #for i in range(0, len_x):
    #    x = x_number_values[i]
    #    y = y_number_values[i]
    #    ax.text(x+0.1, y+0.1, labels[i], fontsize=12)

    plt.title(TITLE, fontsize=18, y=1.13)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    if SAVE and PATH != None:
        plt.savefig(PATH, bbox_inches='tight')
    if PRINT:
        plt.show()
    plt.close()


def draw_classes_scatterplot(y_number_values, x_number_values, labels, TITLE, XLABEL, YLABEL, YBOTTOM, YTOP, colors=None, PATH=None):
    MARKERS = ["o", "+", "x", "s"]
    #MARKERS = None


    ax = plt.subplot(111)
    ax.set_ylim(bottom=YBOTTOM, top=YTOP)
    ax.yaxis.set_label_coords(-0.03, 1.02)


    num_classes = len(y_number_values)
    if num_classes != len(x_number_values):
        print("num_classes != len(x_number_values)")
        plt.close()
        return

    if len(labels) != num_classes:
        print("len(labels) != num_classes")
        plt.close()
        return

    for i in range(0, num_classes):
        len_x = len(x_number_values[i])
        len_y = len(y_number_values[i])

        if len_x != len_y:
            print("ERROR: len_x != len_y")
            plt.close()
            return

        if MARKERS == None:
            ax.scatter(x = x_number_values[i], y = y_number_values[i], label=labels[i], alpha=0.8)
        else:
            ax.scatter(x = x_number_values[i], y = y_number_values[i], marker=MARKERS[i], label=labels[i], alpha=0.8)

    #if len(labels) != len_x:
    #    print("ERROR: len(labels) != len_y")
    #    plt.close()
    #    return

    #for i in range(0, len_x):
    #    x = x_number_values[i]
    #    y = y_number_values[i]
    #    ax.text(x+0.1, y+0.1, labels[i], fontsize=12)

    ax.legend()

    plt.title(TITLE, fontsize=18, y=1.13)
    plt.xlabel(XLABEL, fontsize=12)
    plt.ylabel(YLABEL, fontsize=12, rotation=0)

    if SAVE and PATH != None:
        plt.savefig(PATH, bbox_inches='tight')
    if PRINT:
        plt.show()
    plt.close()
