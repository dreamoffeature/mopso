#encoding: utf-8
import numpy as np
 
def compare_ (fitness_curr,fitness_ref):
#判断当前解是否能被完全支配,false是完全支配
    for i in range(len(fitness_curr)):
        if fitness_curr[i] < fitness_ref[i]:
            return True
    return False
def judge_(fitness_curr,fitness_data,cursor):
#判断当前是否为非劣解
    for i in range(len(fitness_data)):
        if i == cursor:
            continue
        #如果数据集中存在一个解可以完全支配当前解，则当前解为劣解
        if compare_(fitness_curr,fitness_data[i]) == False:
            return False
    return True
 
class Pareto_:
    def __init__(self,in_data,fitness_data):
        self.in_data = in_data  #粒子位置
        self.fitness_data = fitness_data #粒子适应度值
        self.cursor = -1 #当前光标位置
        self.len_ = in_data.shape[0] #粒子数量
        self.bad_num = 0 #非优解个数
    def next(self):
        #返回粒子位置和适应度值ֵ
        self.cursor = self.cursor+1
        return self.in_data[self.cursor],self.fitness_data[self.cursor]
    def hasNext(self):
        #判断是否检查了所有粒子
        return self.len_ > self.cursor + 1 + self.bad_num
    def remove(self):
        #劣解删除
        self.fitness_data = np.delete(self.fitness_data,self.cursor,axis=0)
        self.in_data = np.delete(self.in_data,self.cursor,axis=0)
        #索引减1
        self.cursor = self.cursor-1
        #劣解个数加1
        self.bad_num = self.bad_num + 1
    def pareto(self):
        while(self.hasNext()):
            #获取当前粒子
            in_curr,fitness_curr = self.next()
            #判断当前粒子是否pareto最优
            if judge_(fitness_curr,self.fitness_data,self.cursor) == False :
                self.remove()
        return self.in_data,self.fitness_data
