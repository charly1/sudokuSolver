#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 20:47:16 2020

@author: charly
"""
import numpy as np
import copy

SIZE_GRID = 9
                
class SodukuSolver():
    def __init__(self,grid):
        self.grid = grid
        self.gridPos = self.generateGridPossibleNumbers()
        
    def solve(self):
        if self.testIfGridvalid():
            return np.array([])
        
        counterIter = 0
        numUnknown = self.getNumberOfUnknownNumbers()
        while numUnknown != 0:
            self.removePossiblenumbers()
            self.findIsolatedNumbers()
            self.syncGrids()
            counterIter += 1
            newNumUnknown = self.getNumberOfUnknownNumbers()
            if numUnknown == newNumUnknown:
                newGrid = self.generateNewGridBasedOnTry()
                for m in range(len(newGrid)):
                    gridTmp = newGrid[m]
                    s = SodukuSolver(gridTmp)
                    gridTmp = s.solve()
                    if gridTmp.size > 0:
                        numUnknown = 0
                        self.grid = gridTmp
                        break
            else:
                numUnknown = newNumUnknown
        print("Done in ",counterIter," iterations")
        return self.grid
        
    def generateNewGridBasedOnTry(self):
        nbCopy = 2
        newGrid = []
        for i in range(SIZE_GRID):
            vectK = np.where(np.sum(self.gridPos[i,:,:]>0,axis=0) == nbCopy)[0]
            if vectK.size > 0:
                k = vectK[0]
                vectJ = np.where(self.gridPos[i,:,k] == k+1)[0]
                newGrid = []
                for j in vectJ:
                    gridTmp = copy.copy(self.grid)
                    gridTmp[i,j] = k+1
                    newGrid.append(gridTmp)
                    break
                break
        
        if newGrid == []:
            for j in range(SIZE_GRID):
                vectK = np.where(np.sum(self.gridPos[:,j,:]>0,axis=0) == nbCopy)[0]
                if vectK.size > 0:
                    k = vectK[0]
                    vectI = np.where(self.gridPos[:,j,k] == k+1)[0]
                    newGrid = []
                    for j in vectI:
                        gridTmp = copy.copy(self.grid)
                        gridTmp[i,j] = k+1
                        newGrid.append(gridTmp)
                        break
                    break
                    
        return newGrid
            
        
    def testIfGridvalid(self):
        self.syncGrids()
        flagError = False

        #Along x axis
        for i in range(SIZE_GRID):
            vectComp = np.zeros(9)
            for j in range(SIZE_GRID):
                num = self.grid[i,j]
                if num!=0:
                    if vectComp[num-1] == 0:
                        vectComp[num-1] += 1
                    else:
                        flagError = True
                        break
            if flagError == True:
                break
        
        #Along y axis
        for j in range(SIZE_GRID):
            vectComp = np.zeros(9)
            for i in range(SIZE_GRID):
                num = self.grid[i,j]
                if num!=0:
                    if vectComp[num-1] == 0:
                        vectComp[num-1] += 1
                    else:
                        flagError = True
                        break
            if flagError == True:
                break
            
        #Along square
        x=[0,0,0,3,3,3,6,6,6]
        y=[0,3,6,0,3,6,0,3,6]
        for k in range(SIZE_GRID):
            xMin,xMax,yMin,yMax = self.getLimiteSquare(x[k],y[k])
            vectComp = np.zeros(9)
            for i in range(xMin,xMax):
                for j in range(yMin,yMax):
                    num = self.grid[i,j]
                    if num!=0:
                        if vectComp[num-1] == 0:
                            vectComp[num-1] += 1
                        else:
                            flagError = True
                            break
                if flagError == True:
                    break
            if flagError == True:
                break
        
        if flagError == True:
            print("Error: Grid not valid")
        return flagError
                
        
    def findIsolatedNumbers(self):
        self.findIsolatedInSquare()
        self.findIsolatedInLine()
        self.findIsolatedInCol()
        
    def findIsolatedInLine(self):
        for i in range(SIZE_GRID):
            vectCount = np.sum((self.gridPos[i,:,:] > 0),axis=0)
            for k in range(len(vectCount)):
                m = vectCount[k]
                if m == 1:
                    j = np.where(self.gridPos[i,:,:] == k+1)[0][0]
                    self.gridPos[i,j,:] = np.zeros(9)
                    self.gridPos[i,j,k] = k+1
                    
    def findIsolatedInCol(self):
        for j in range(SIZE_GRID):
            vectCount = np.sum((self.gridPos[:,j,:] > 0),axis=0)
            for k in range(len(vectCount)):
                m = vectCount[k]
                if m == 1:
                    i = np.where(self.gridPos[:,j,:] == k+1)[0][0]
                    self.gridPos[i,j,:] = np.zeros(9)
                    self.gridPos[i,j,k] = k+1
                    
    def findIsolatedInSquare(self):
        x=[0,0,0,3,3,3,6,6,6]
        y=[0,3,6,0,3,6,0,3,6]
        for k in range(SIZE_GRID):
            xMin,xMax,yMin,yMax = self.getLimiteSquare(x[k],y[k])
            vectCount = np.sum(np.sum((self.gridPos[xMin:xMax,yMin:yMax,:] > 0),axis=0),axis=0)
            for n in range(len(vectCount)):
                m = vectCount[n]
                if m == 1:
                    idx = np.where(self.gridPos[xMin:xMax,yMin:yMax,:].reshape((SIZE_GRID,SIZE_GRID)) == n+1)[0][0]
                    j = idx%3
                    i = int((idx-j)/3)
                    self.gridPos[i+x[k],j+y[k],:] = np.zeros(9)
                    self.gridPos[i+x[k],j+y[k],n] = n+1
        
        
        
    def __str__(self,grid=np.array([])):
        self.syncGrids()
        strToPrint = ""
        if grid.size==0:
            grid = self.grid
        strToPrint += "Number of unknown numbers:"+str(self.getNumberOfUnknownNumbers())+"\n"
        fullLine1 = "-----------------------------------------\n"
        fullLine2 = "||           ||           ||           ||\n"
        for j in range(SIZE_GRID):
            if j%3 == 0:
                strToPrint += fullLine1
            else:
                strToPrint += fullLine2
            str1 = "|| "+str(grid[0,j])+"   "+str(grid[1,j])+"   "+str(grid[2,j])+" || "
            str2 = str(grid[3,j])+"   "+str(grid[4,j])+"   "+str(grid[5,j])+" || "
            str3 = str(grid[6,j])+"   "+str(grid[7,j])+"   "+str(grid[8,j])+" ||"
            strToPrint += (str1+str2+str3).replace("0"," ")+"\n"
        strToPrint += fullLine1
        return strToPrint

        
    def syncGrids(self):
        for i in range(SIZE_GRID):
            for j in range(SIZE_GRID):
                if np.count_nonzero(self.gridPos[i,j,:]) == 1:
                    k = np.where((self.gridPos[i,j,:]>0)==True)[0][0]
                    self.grid[i,j] = k+1
        
    def getNumberOfUnknownNumbers(self):
        counter = 0
        for i in range(SIZE_GRID):
            for j in range(SIZE_GRID):
                if self.grid[i,j] == 0:
                    counter += 1
        return counter
        
        
    def generateGridPossibleNumbers(self):
        gridPos = np.zeros((9,9,9))
        
        for i in range(SIZE_GRID):
            for j in range(SIZE_GRID):
                if self.grid[i,j] != 0:
                    gridPos[i,j,self.grid[i,j]-1] = self.grid[i,j]
                else:
                    for k in range(SIZE_GRID):
                        gridPos[i,j,k] = k+1
        return gridPos
    
    def removePossiblenumbers(self):
        for i in range(SIZE_GRID):
            for j in range(SIZE_GRID):
                if self.grid[i,j] != 0:
                    self.removeNumberInLine(i,j)
                    self.removeNumberInCol(i,j)
                    self.removeNumberInSquare(i,j)
                    
    def removeNumberInLine(self,x,y):
        num = self.grid[x,y]-1
        for i in range(SIZE_GRID):
            if i != x:
                self.gridPos[i,y,num] = 0
            
    def removeNumberInCol(self,x,y):
        num = self.grid[x,y]-1
        for j in range(SIZE_GRID):
            if j != y:
                self.gridPos[x,j,num] = 0
            
    def removeNumberInSquare(self,x,y):
        num = self.grid[x,y]-1
        xMin,xMax,yMin,yMax = self.getLimiteSquare(x,y)
        for i in range(xMin,xMax):
            for j in range(yMin,yMax):
                if i != x and j != y:
                    self.gridPos[i,j,num] = 0
            
    def getLimiteSquare(self,x,y):
        if x < 3:
            xMin = 0
            xMax = 3
        elif x < 6:
            xMin = 3
            xMax = 6
        else:
            xMin = 6
            xMax = 9
            
        if y < 3:
            yMin = 0
            yMax = 3
        elif y < 6:
            yMin = 3
            yMax = 6
        else:
            yMin = 6
            yMax = 9
        return xMin,xMax,yMin,yMax
    
if __name__ == '__main__':
    gridEasy = np.transpose(np.array([[0,0,0,0,0,8,5,3,6],
                                      [0,0,0,4,0,1,0,0,0],
                                      [0,0,0,0,7,0,1,0,0],
                                      [1,3,0,0,0,0,7,0,5],
                                      [4,0,7,8,0,2,0,0,0],
                                      [6,8,0,0,0,0,4,0,3],
                                      [0,0,0,0,6,0,8,0,0],
                                      [0,0,0,2,0,9,0,0,0],
                                      [0,0,0,0,0,7,3,4,9]]))
    
    gridHard = np.transpose(np.array([[8,0,1,0,0,2,3,7,0],
                                      [0,0,3,6,0,5,9,0,0],
                                      [0,0,4,0,0,0,0,0,0],
                                      [2,0,0,1,0,0,8,0,0],
                                      [0,0,0,0,2,0,0,0,6],
                                      [3,0,0,9,0,0,5,0,0],
                                      [0,0,8,0,0,0,0,0,0],
                                      [0,0,2,5,0,1,7,0,0],
                                      [5,0,9,0,0,3,2,1,0]]))
    
    gridExtr = np.transpose(np.array([[0,2,0,0,1,0,0,0,0],
                                      [0,0,6,2,4,3,0,0,1],
                                      [0,0,0,7,0,8,0,6,0],
                                      [0,3,5,0,0,0,6,7,0],
                                      [1,6,0,0,0,0,0,3,2],
                                      [0,4,9,0,0,0,5,1,0],
                                      [0,5,0,9,0,4,0,0,0],
                                      [9,0,0,1,3,2,8,0,0],
                                      [0,0,0,0,7,0,0,4,0]]))

    s = SodukuSolver(gridHard)
    print(s)
    s.solve()
    print(s)
        
