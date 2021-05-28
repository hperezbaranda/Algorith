#! /usr/bin/python
# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import numpy as np



class Node:

    def __init__(self, point):
        self.location  = point
        self.leftChild = None
        self.rightChild = None

    def __str__(self):
        # print self.leftChild,

        # print self.rightChild,
        # print self.name
        return self.location

def kdtree(pointList, depth=0):
    if not pointList:
        return

    # Select axis based on depth so that axis cycles through all valid values
    k = len(pointList[0]) # assumes all points have the same dimension
    axis = depth % k

    # Sort point list and choose median as pivot element
    pointList.sort(key=lambda x:x[axis])

    median = int(len(pointList)/2) # choose median

    # Create node and construct subtrees
    node = Node(pointList[median])
    node.leftChild = kdtree(pointList[0:median], depth+1)
    node.rightChild = kdtree(pointList[median+1:], depth+1)
    return node

def kdInsert(point, tree,depth=0):


    if tree is None:
        tree = Node(point)
    elif point is not tree.location:
        k = len(point)
        axis = depth % k
        if int(int(point[axis])) > tree.location[axis]:
            if tree.rightChild is None:
                tree.rightChild = Node(point)
            else:
                tree.rightChild = kdInsert(point, tree.rightChild, depth + 1)
        else:
            if tree.leftChild is None:
                tree.leftChild = Node(point)
            else:
                tree.leftChild = kdInsert(point, tree.leftChild,depth + 1)

    return tree

def maior(tree, axis):
    if tree == None:
        return None
    elif tree.rightChild == tree.leftChild == None:
        return tree.location
    elif tree.rightChild is None:
        return max(tree.location, \
            maior(tree.leftChild, axis), \
            key=lambda x: x[axis])
    elif tree.leftChild is None:
        return max(tree.location, \
            maior(tree.rightChild, axis), \
            key=lambda x: x[axis])
    else:
        return max(tree.location, \
            maior(tree.rightChild, axis), \
            maior(tree.rightChild, axis), \
            key=lambda x: x[axis])

def minor(tree, axis):
    if tree == None:
        return None
    elif tree.rightChild == tree.leftChild == None:
        return tree.location
    elif tree.rightChild is None:
        return min(tree.location, \
            minor(tree.leftChild, axis), \
            key=lambda x: x[axis])
    elif tree.leftChild is None:
        return min(tree.location, \
            minor(tree.rightChild, axis), \
            key=lambda x: x[axis])
    else:
        return min(tree.location, \
            minor(tree.rightChild, axis), \
            minor(tree.rightChild, axis), \
            key=lambda x: x[axis])

def remove(point, tree, depth=0):
    k = len(point)
    axis = depth % k

    if tree is None:
        return  None
    else:
        if point == tree.location:
            if tree.leftChild == None and tree.rightChild == None:
                return None
            else:
                if tree.rightChild is not None:
                    #Hacerlo por la izq
                    tmp_point = minor(tree.rightChild, axis)
                    tree.location = tmp_point
                    tree.rightChild = remove(tmp_point, tree.rightChild, depth + 1)

                else:
                    # Hacerlo por la der
                    tmp_point = maior(tree.leftChild, axis)
                    tree.location = tmp_point
                    tree.leftChild = remove(tmp_point, tree.leftChild, depth + 1)

        elif int(point[axis]) > tree.location[axis]:
            tree.rightChild = remove(point, tree.rightChild, depth+1)
        elif int(point[axis]) <= tree.location[axis]:
            tree.leftChild = remove(point, tree.leftChild, depth+1)

    return tree

def nn_search(point, tree, bp=0, best=float('Inf'), depth=0):
    k = len(point)
    axis = depth % k

    tmp_best = pow((int(point[0])-tree.location[0]),2)+pow((int(point[1])-tree.location[1]),2)

    if tmp_best < best:
        best = tmp_best
        bp = tree.location

    if tree.location[axis]<= int(int(point[axis])):
        search_first = 1
    else:
        search_first = 0
    if search_first == 0:
        if int(point[axis]) - best <= tree.location[axis] and tree.leftChild is not None:
            bp, best =nn_search(point, tree.leftChild, bp, best, depth + 1)
        if int(point[axis]) + best > tree.location[axis] and tree.rightChild is not None:
            bp, best=nn_search(point, tree.rightChild, bp, best, depth + 1)
    else:
        if int(point[axis]) + best > tree.location[axis] and tree.rightChild is not None:
            bp, best = nn_search(point, tree.rightChild, bp, best, depth + 1)
        if int(point[axis]) - best <= tree.location[axis] and tree.leftChild is not None:
            bp, best =nn_search(point, tree.leftChild, bp, best, depth + 1)

    return bp,best

def inorder(tree,lista):
    if tree.leftChild == tree.rightChild is None:
        lista.append(tree.location)
    else:
        if tree.leftChild is not None:
            inorder(tree.leftChild,lista)
        lista.append(tree.location)
        if tree.rightChild is not None:
            inorder(tree.rightChild,lista)

def balancear(tree):
    li = []
    inorder(tree,li)
    return kdtree(li)

def plotLinha(tree,x1,x2,y1,y2, xmin,xmax,ymax,depth=0):
    k = len(tree.location)
    axis = depth % k
    porcentx = lambda x: round(float(x-xmin)/float(xmax-xmin),2)
    porcenty = lambda y: round(float(y-0-1)/float(ymax-0-1),2)

    # li = []
    # inorder(tree, li)
    if axis == 0:
        # plt.axvline(tree.location[0], porcenty(y1), porcenty(y2),color='b')
        plt.plot([tree.location[0]]*2,[-1,y2], color='b')
    else:
        plt.plot([x1,x2], [tree.location[1]]*2, color='r')
        # plt.axhline(tree.location[1], porcentx(x1), porcentx(x2),color='r')

    if tree.leftChild is not None:
        if  axis == 0:
            plotLinha(tree.leftChild, x1, tree.location[0], y1, y2, xmin, xmax, ymax, depth + 1)
        else:
            plotLinha(tree.leftChild, x1, x2, y1, tree.location[1], xmin, xmax, ymax, depth + 1)
    elif tree.rightChild is not None:
        if axis ==0:
            plotLinha(tree.rightChild, tree.location[0], x2, y1, y2, xmin,xmax,ymax,depth+1)
        else:
            plotLinha(tree.rightChild,x1,x2,tree.location[1],y2, xmin,xmax,ymax,depth+1)


def plotTree(tree,point,near):
    plt.figure("Kd-tree",figsize=(16,8))
    # plt.figure()
    li = []
    inorder(tree,li)
    plt.grid(True)
    plt.plot([point[0],near[0]],[point[1],near[1]])
    for i in li:
        plt.plot(i[0],i[1],'ro')
    plt.plot(point[0],point[1],'bs',color="green")

    x1 = min(li,key = lambda i:i[0])[0]
    x2 = max(li,key = lambda i:i[0])[0]
    y1 = min(li, key=lambda i: i[1])[1]
    y2 = max(li, key=lambda i: i[1])[1]

    plt.axis((x1-1,x2+1,y1-1,20))
    plt.tight_layout()
    plt.xticks(np.arange(x1,x2+1, 1.0))
    plt.yticks(np.arange(y1-1, 20, 1.0))
    #plotLinha(tree, x1-1, x2+1, y1-1, 20,x1,x2,y2)
    plt.show()



if __name__ == '__main__':
    """Alocação de Companheiro"""


    assignment = None

    init = open("init")
    lista = init.readlines()
    trabalhador = {}
    for i in lista:
        linha = i.strip().split(" ")
        ppoint = (int(linha[1]),int(linha[2]))
        trabalhador[ppoint]=linha[0]
        assignment = kdInsert(ppoint,asignment)

    assignment = balancear(assignment) # Equilibrar a Arvore
    #print asignment.leftChild.leftChild

    print("Alocação de Companheiro")
    print("Nesta empresa que já tem 10 trabalhadores procuramos companheros de trabalhos para os calouros segum sua condiçao ")
    no_exit = True
    while no_exit:
        print("1- Inserir um novo trabalhador \n"
              "2- Procurar companhero para um candidato \n"
              "3- Exit")

        option = int(input("opçao: "))

        no_exit = False if option == 3 else True
        if not no_exit:
            break

        if(option == 2):
            print( "Para procurar um companhero precisamos conheçer do candidato:")
            year = input("quantos anos tem: ")
            kids = input("quantas crianças tem: ")
            team = nn_search((year,kids),assignment)

            if team is not None:
                print("\nO posible companhero é: {}%s{}\n".format('\033[32m','\033[0m') %trabalhador[team[0]])
                plotTree(assignment,(year,kids),team[0])
            else:
                print( "\n No tem companhero\n")


        elif option == 1:
            name = input("Qual é o nome do novo trabalhador: ")
            year = input("quantos anos tem: ")
            kids = input("quantas crianças tem: ")
            point = (year, kids)
            assignment = kdInsert(point, assignment)
            print

        else:
            print( "Opção não valida\n")
