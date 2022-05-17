import inspect
from statistics import mean
from sys import orig_argv
import pandas as pd
import numpy as np


def get_weights(array):
    ori = np.array(array)
    trans = ori.transpose()
    sum_cols = [sum(col) for col in trans]
    new = np.array([trans[index]/sum_cols[index]
                    for index in range(trans.shape[0])]).transpose()
    weights = [mean(row) for row in new]
    return np.array(weights)


class MVDM():
    def rotate(self):
        temp = list(zip(*self.values))
        temp2 = []
        for item in temp:
            temp2.append(list(item))
        return temp2

    def report(self, answer):
        cols = self.situations.copy()
        cols.append('P')
        df = pd.DataFrame(data=answer['values'],
                          columns=cols, index=self.options)
        print(answer['Type'].upper().center(60, '-'))
        print(df.to_markdown())
        print(f"Target value: {answer['target_value']}")
        print(f"Option: {answer['Option']}")

    def __init__(self, name='New Solver', options=None, situations=None, values=None):
        self.name = name
        self.options = options
        self.situations = situations
        self.values = values
        print(f'{name} initialized!')

    def set_options(self, options):
        self.options = options

    def set_situations(self, situations):
        self.situations = situations

    def set_values(self, values):
        self.values = values

    def get_values(self):
        return self.values

    def Maximax(self):
        listP = []
        tempV = self.values
        details = []
        print(tempV)

        for value in tempV:
            temp = value.copy()
            temp.append(max(value))
            details.append(temp)
            listP.append(max(value))

        maxP = max(listP)

        for i in range(len(listP)):
            if listP[i] == maxP:
                self.report(
                    {"Type": 'Maximax', "Option": self.options[i] + f" i={i+1}", "target_value": maxP, "values": details, })

    def Maximin(self):
        listP = []
        tempV = self.get_values()
        details = []
        print(tempV)
        for value in tempV:
            temp = value.copy()
            temp.append(min(value))
            details.append(temp)
            listP.append(min(value))

        maxP = max(listP)

        for i in range(len(listP)):
            if listP[i] == maxP:
                self.report(
                    {"Type": 'Maximin', "Option": self.options[i] + f" i={i+1}", "target_value": maxP, "values": details})

    def Laplace(self):
        listP = []
        tempV = self.values
        details = []

        for value in tempV:
            temp = value.copy()
            temp.append(sum(value)/len(self.situations))
            details.append(temp)
            listP.append(sum(value)/len(self.situations))
            print(listP)

        maxP = max(listP)
        print(maxP)
        for i in range(len(listP)):
            if listP[i] == maxP:
                self.report(
                    {"Type": 'Laplace', "Option": self.options[i] + f" i={i+1}", "target_value": maxP, "values": details, })

    def Hurwicz(self, alpha):
        listP = []
        tempV = self.values
        details = []

        for value in tempV:
            temp = value.copy()
            temp.append(max(value)*alpha+min(value)*(1-alpha))
            details.append(temp)
            listP.append(max(value)*alpha+min(value)*(1-alpha))

        maxP = max(listP)

        for i in range(len(listP)):
            if listP[i] == maxP:
                self.report({"Type": inspect.stack()[
                            0][3], "Option": self.options[i] + f" i={i+1}", "target_value": maxP, "values": details, })

    def Minimax(self):
        listP = []
        oriV = self.rotate()
        tempV = self.values
        max_i = [max(value) for value in oriV]
        details = []

        for row in tempV:
            temp = [max_i[j]-row[j]
                    for j in range(len(row))]
            temp.append(max([max_i[j]-row[j]
                             for j in range(len(row))]))
            details.append(temp)
            listP.append(max([max_i[j]-row[j]
                              for j in range(len(row))]))

        minP = min(listP)

        for i in range(len(listP)):
            if listP[i] == minP:
                self.report({"Type": inspect.stack()[
                            0][3], "Option": self.options[i] + f" i={i+1}", "target_value": minP, "values": details, })

    def MaxEMV(self, proba):
        listP = []
        tempV = self.values
        details = []
        for row in tempV:
            temp = [proba[j]*row[j]
                    for j in range(len(row))]
            temp.append(sum([proba[j]*row[j]
                             for j in range(len(row))]))
            details.append(temp)
            listP.append(sum([proba[j]*row[j]
                              for j in range(len(row))]))

        maxP = max(listP)

        for i in range(len(listP)):
            if listP[i] == maxP:
                self.report({"Type": inspect.stack()[
                    0][3], "Option": self.options[i] + f" i={i+1}", "target_value": maxP, "values": details, })

    def MinEOL(self, proba):
        listP = []
        tempV = self.values
        oriV = self.rotate()
        max_i = [max(value) for value in oriV]
        details = []

        for row in tempV:
            temp = [(max_i[j]-row[j])*proba[j]
                    for j in range(len(row))]
            temp.append(sum([(max_i[j]-row[j])*proba[j]
                             for j in range(len(row))]))
            details.append(temp)
            listP.append(sum([(max_i[j]-row[j])*proba[j]
                              for j in range(len(row))]))

        minP = min(listP)

        for i in range(len(listP)):
            if listP[i] == minP:
                self.report({"Type": inspect.stack()[
                    0][3], "Option": self.options[i] + f" i={i+1}", "target_value": minP, "values": details, })

    def solveAll(self, alpha, proba):
        self.Maximax()
        self.Maximin()
        self.Laplace()
        self.Hurwicz(alpha=alpha)
        self.Minimax()
        self.MaxEMV(proba=proba)
        self.MinEOL(proba=proba)


class MFDM():
    pass


class AHP():
    def __init__(self, name='AHP Solver', criteria=None, alternatives=None, cvalues=None, avalues=None):
        self.name = name
        self.criteria = criteria
        self.alternatives = alternatives
        self.cvalues = cvalues
        self.avalues = avalues

    def solve(self):
        X = np.array([get_weights(matrix)
                     for matrix in self.avalues]).transpose()
        Y = get_weights(self.cvalues).reshape(len(self.criteria), 1)
        Z = np.matmul(X, Y)
        index = 0
        for i in range(len(Z)):
            if Z[i] == max(Z):
                index = i

        print('alternatives-x-criteria'.upper().center(50, '-'))
        print(pd.DataFrame(data=X, columns=self.criteria,
                           index=self.alternatives).to_markdown())
        print('criteria'.upper().center(50, '-'))
        print(pd.DataFrame(data=Y, columns=[
              'Trong So'], index=self.criteria).to_markdown())
        print('UU TIEN'.upper().center(50, '-'))
        print(pd.DataFrame(data=Z, columns=[
              'Muc do uu tien'], index=self.alternatives).to_markdown())

        print(
            f'\nChon phuong an {self.alternatives[index]}, Muc do uu tien = {Z[index][0]}')
