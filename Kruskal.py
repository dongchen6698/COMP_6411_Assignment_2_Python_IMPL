import resource
import time
import linecache
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from operator import itemgetter


class DisjointSet(dict):
    def add(self, item):
        self[item] = item

    def find(self, item):
        parent = self[item]

        while self[parent] != parent:
            parent = self[parent]

        self[item] = parent
        return parent

    def union(self, item1, item2):
        self[item2] = self[item1]


class Edge:
    def __init__(self, startpoint, endpoint, weight):
        self.startPoint = int(startpoint) + 1
        self.endPoint = int(endpoint) + 1
        self.weight = int(weight)

    def __str__(self):
        return "(%d, %d) edge cost: %d \n" % (self.startPoint, self.endPoint, self.weight)


def generateEdgeList(result_mst):
    list = []
    for n in result_mst:
        edge = Edge(n[0], n[1], n[2])
        list.append(edge)

    return list


def kruskal(nodesList, edgesList):
    forest = DisjointSet()
    mst = []
    for n in nodesList:
        forest.add(n)

    for e in sorted(edgesList, key=itemgetter(2)):
        n1, n2, _ = e
        t1 = forest.find(n1)
        t2 = forest.find(n2)
        if t1 != t2:
            mst.append(e)
            forest.union(t1, t2)

    return mst


def getNodesList(nodesCount):
    nodesList = []
    for n in range(nodesCount):
        nodesList.append(str(n))

    return nodesList


def getEdgeList(nodesCount, filePath):
    f = open(filePath, 'r')
    graph = [[0 for i in range(nodesCount)] for j in range(nodesCount)]
    edgesList = []
    for a in range(nodesCount):
        valueList = re.findall('\d+', f.readline())
        for b in range(nodesCount):
            graph[a][b] = valueList.pop(0)

    for x in range(nodesCount):
        for y in range(x, nodesCount):
            if graph[x][y] is 0:
                continue
            else:
                edgesList.append((str(x), str(y), graph[x][y]))

    return edgesList


def fromResultToFile(nodesCount,edgeList, durationTime, memory):
    sumStr = ''
    sumValue = 0
    out = open("Result_of_Graph_G_N_%s.txt" % nodesCount, 'w+')
    out.write("Total number of nodes = %s \n" % nodesCount)
    out.write("Total number of edges in the minimum spanning three = %s \n" % str(len(edgeList)))
    out.write("List of edges & their costs: \n")
    for edge in edgeList:
        out.write(str(edge))
        sumStr += str(edge.weight) + " + "
        sumValue += edge.weight
    out.write("Total cost of minimum spanning tree is = Sum of ( %s ) = %s \n" % (sumStr[0:-3], sumValue))
    out.write("Total execution time is = %s milliseconds \n" % (durationTime*1000))
    out.write("Total memory consumption is = %s bytes \n" % memory)
    out.close()


def main(n_nodesCount, n_filePath):
        nodesCount = int(n_nodesCount)
        filePath = n_filePath
        nodes = getNodesList(nodesCount)
        edges = getEdgeList(nodesCount, filePath)

        startTime = time.time()
        result_mst = kruskal(nodes, edges)
        endTime = time.time()
        durationTime = endTime - startTime

        memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        edgelist = generateEdgeList(result_mst)

        fromResultToFile(nodesCount, edgelist , durationTime, memory)
        print("Finish calculate")


class MST_APP:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.linenumber = 1

        self.vertex_n = Label(master=frame, text="Vertex N: ")
        self.vertex_n.grid(row=0, column=0)
        number = ('10', '20', '50', '100', '1000')
        self.numberCombobox = Combobox(frame, value=number, state='readonly')
        self.numberCombobox.grid(row=0, column=1, columnspan=2)

        self.data_file = Label(master=frame, text="Data File: ")
        self.data_file.grid(row=0, column=3)
        file = ('AdjacencyMatrix_of_Graph_G_N_10.txt',
                'AdjacencyMatrix_of_Graph_G_N_20.txt',
                'AdjacencyMatrix_of_Graph_G_N_50.txt',
                'AdjacencyMatrix_of_Graph_G_N_100.txt',
                'AdjacencyMatrix_of_Graph_G_N_1000.txt')
        self.fileCombobox = Combobox(frame, value=file, state='readonly')
        self.fileCombobox.grid(row=0, column=4, columnspan=2)

        self.textArea = ScrolledText(master=frame, undo=True)
        self.textArea.config(state='disabled')
        self.textArea.grid(row=1, column=0, columnspan=6)

        self.algo_list = Label(master=frame, text="Algorithm: ")
        self.algo_list.grid(row=2,column=0)
        algorithm = ['Prim\'s algorithm', 'Kruskal\'s algorithm', 'Boruvka algorithm', 'Hybrid algorithm']
        self.algorithmCombobox = Combobox(frame, value=algorithm, state='readonly')
        self.algorithmCombobox.grid(row=2, column=1, columnspan=2)

        self.startButton = Button(frame, text="Start", command=self.startAction)
        self.startButton.grid(row=2, column=3)

        self.stepButton = Button(frame, text="Step", command=self.stepAction)
        self.stepButton.grid(row=2, column=4)

        self.clearButton = Button(frame, text="Clear", command=self.clearAction)
        self.clearButton.grid(row=2, column=5)

    def startAction(self):
        if self.numberCombobox.current() and self.fileCombobox.current() and self.algorithmCombobox.current() is -1:
            messagebox.showinfo('Message', 'Please confirm to choose the vertex number, data file and algorithm!')
        elif self.numberCombobox.current() is not self.fileCombobox.current():
            messagebox.showinfo('Message', 'Please select the proper vertex number and file!')
        else:
            main(int(self.numberCombobox.get()), self.fileCombobox.get())
            self.textArea.configure(state='normal')
            self.textArea.delete("1.0", "end")
            self.textArea.insert('insert', 'Finish calculate \n')
            self.textArea.configure(state='disabled')
            self.linenumber = 1

    def stepAction(self):
        new_line = linecache.getline('Result_of_Graph_G_N_%s.txt' % self.numberCombobox.get(), self.linenumber)
        if new_line is not '':
            self.textArea.configure(state='normal')
            self.textArea.insert('insert', new_line)
            self.textArea.configure(state='disabled')
            self.linenumber += 1
        else:
            result = messagebox.askquestion("Inform", "One more time ?", icon='warning')
            if result == 'yes':
                self.textArea.configure(state='normal')
                self.textArea.delete("1.0", "end")
                self.textArea.configure(state='disabled')
                self.linenumber = 1

    def clearAction(self):
        self.textArea.configure(state='normal')
        self.textArea.delete("1.0", "end")
        self.textArea.configure(state='disabled')
        self.linenumber = 1



def MST_GUI():
    root = Tk()
    root.title = 'MST_GUI of Python'
    MST_APP(root)
    root.mainloop()

if __name__ == '__main__':
    MST_GUI()








