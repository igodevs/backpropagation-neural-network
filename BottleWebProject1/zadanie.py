from random import random
from csv import reader
from math import exp
import matplotlib.pyplot as plt
import csv



# Aktivacna funkcia
def act_funct(x):
    return 1.0 / (1.0 + exp(-x))

# Derivacna funkcia
def der_act_funct(x):
    return x * (1.0 - x)


# Inicializacia NS
def network(n_inputs, n_first_hidden, n_second_hidden, n_outputs):
    bias = 1
    network = list()
    first_hidden_layer = [{'weights':[random() for i in range(n_inputs + bias)]} for i in range(n_first_hidden)]
    network.append(first_hidden_layer)
    second_hidden_layer = [{'weights':[random() for i in range(n_first_hidden + bias)]} for i in range(n_second_hidden)]
    network.append(second_hidden_layer)
    output_layer = [{'weights': [random() for i in range(n_second_hidden + bias)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network



# Vypocet in
def ini(weights, inp):
    act = weights[-1]
    for i in range(len(weights)-1):
        act += weights[i] * inp[i]
    return act


# Vypocet out
def outi(network, row):
    inp = row
    for layer in network:
        new_inp = []
        for neuron in layer:
            act = ini(neuron['weights'], inp)
            neuron['output'] = act_funct(act)
            new_inp.append(neuron['output'])
        inp = new_inp
    return inp
    #print('Inp: ', inp)


# Backpropagate error and store in neurons
def delta(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        err = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                err.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                #print('Expected_J, ',expected[j])
                err.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = err[j] * der_act_funct(neuron['output'])

# Update network weights with error
def delta_w(network, row, l_rate):
    for i in range(len(network)):
        inp = row[:-1]
        if i != 0:
            inp = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inp)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inp[j]
            neuron['weights'][-1] += l_rate * neuron['delta']


# Train a network for a fixed number of epochs
e = list()
ep = list()
def train_network(network, train, l_rate, n_iteration, n_outputs):
    for epoch in range(n_iteration):
        sum_error = 0
        ep.append(epoch)
        for row in train:
            outputs = outi(network, row)
            #print('Outputs: ', outputs )
            expect = [0 for i in range(n_outputs)]
            #print('Prve: ', expect)
            expect[row[-1]] = 1
            #print('Druhe: ', expect)
            sum_error += sum([((expect[i]-outputs[i])**2)/len(expect) for i in range(len(expect))])
            #print('Sum error: ', sum_error)
            delta(network, expect)
            #print('Delta: ', delta(network, expect))
            delta_w(network, row, l_rate)
            #print('Delta_w: ', delta_w(network, row, l_rate))
        e.append(sum_error)
        print('>iteration=%d, learning_rate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
    print(e)

# Citanie z csv dokumentu
def load_csv(filename):
    data = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[0] == 'x1':
                continue
            if not row:
                continue
            data.append(row)
    return data

# Convert string column to float
def str_column_to_float(data, column):
    for row in data:
         row[column] = float(row[column])

# Convert string column to integer
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup

def clean_row(my_file_name, cleaned_file, remove_words):
    with open(my_file_name, 'r') as infile, \
         open(cleaned_file, 'w') as outfile:
        writer = csv.writer(outfile)
        for row in csv.reader(infile, delimiter='|'):
            column = row
            if not any(remove_word in row for remove_word in remove_words):
                writer.writerow(row)
    infile.close()
    outfile.close()


# Nájdite hodnoty min a max pre každý stĺpec
def dataset_minmax(dataset):
    minmax = list()
    stats = [[min(column), max(column)] for column in dataset]
    return stats

# Zmenenie mnoziny udajov v stlpci v rozsahu 0-1
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)-1):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])


#spustacia funkcia
def zavolaj_funkciu(n_first_hidden, n_second_hidden, n_iteration, file_path):

    cleaned_file = file_path
    dataset = load_csv(cleaned_file)
    for i in range(len(dataset[0])-1):
        str_column_to_float(dataset, i)
    # convert class column to integers
    str_column_to_int(dataset, len(dataset[0])-1)

    n_first_hidden = int(n_first_hidden)
    n_second_hidden = int(n_second_hidden)
    n_iteration = int(n_iteration)

    minmax = dataset_minmax(dataset)
    normalize_dataset(dataset, minmax)

    
    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set([row[-1] for row in dataset]))
    network1 = network(n_inputs, n_first_hidden, n_second_hidden, n_outputs)
    train_network(network1, dataset, 0.1, n_iteration, n_outputs)

    plt.plot(ep,e)
    #plt.xlabel('Iteration')
    #plt.ylabel('error')
    #plt.grid(True)
    plt.savefig('static/img/dsa.png')   # save the figure to file
    
    plt.close("all")

    return 0
