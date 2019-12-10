import random


class u_shaped_mixed_model_assembly_line_balancing():
    def __init__(self, data_file, number_of_model, type, number_of_station):
        self.number_of_model = number_of_model
        self.type = type  # can be I or II
        self.tasks_time = []
        self.cycle_time = 0
        self.number_of_station = number_of_station
        self.number_of_tasks = 0
        self.precedences = []
        self.successors = []
        self.read_data(data_file)
        if self.type is 1:
            self.number_of_station = self.number_of_tasks

    def read_data(self, data_file):
        data = open(data_file)
        data.readline()
        self.number_of_tasks = int(data.readline())
        data.readline()
        data.readline()
        self.cycle_time = int(data.readline())
        data.readline()
        data.readline()
        data.readline()
        data.readline()
        data.readline()
        data.readline()
        for i in range(self.number_of_tasks):
            self.precedences.append([])
            self.successors.append([])
            task_time = data.readline().split(' ')
            model_time = []
            model_time.append(int(task_time[1]))
            for j in range(self.number_of_model-1):
                tmp = abs(int(task_time[1])+random.randint(-100, +100))
                model_time.append(tmp)
            self.tasks_time.append(model_time)
        data.readline()
        data.readline()
        tmp = data.readline()
        while tmp is not '\n':
            tmp = tmp.split(',')
            rel = [int(tmp[0]), int(tmp[1])]
            self.successors[rel[0]-1].append(rel[1]-1)
            self.precedences[rel[1]-1].append(rel[0]-1)
            tmp = data.readline()
        data.close()
