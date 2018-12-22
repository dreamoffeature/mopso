
#encoding: utf-8
import numpy as np
import random
 
class mesh_crowd(object): 
    def __init__(self,curr_archiving_in,curr_archiving_fit,mesh_div,min_,max_,particals):
        self.curr_archiving_in = curr_archiving_in #存档中所有粒子坐标
        self.curr_archiving_fit = curr_archiving_fit #所有粒子适应度值
        self.mesh_div = mesh_div #�等分因子，默认为10
             
        
        self.num_ = self.curr_archiving_in.shape[0] #存档中粒子数目
        
        self.particals = particals  #粒子群数量
        
        self.id_archiving = np.zeros((self.num_)) #粒子编号
        self.crowd_archiving = np.zeros((self.num_)) #拥挤度矩阵，用于记录当前网格的粒子数量
        self.gbest_in = np.zeros((self.particals,self.curr_archiving_in.shape[1])) #初始化gbest坐标
        self.gbest_fit = np.zeros((self.particals,self.curr_archiving_fit.shape[1])) #初始化gbest适应度ֵ
        self.min_ = min_
        self.max_ = max_
 
    def cal_mesh_id(self,in_):
        #计算网格编号id
        #首先，将每个维度按照等分因子进行等分离散化，
        #获取粒子在各维度上的编号。按照10进制将每一个维度编号等比相加（如果用户自定义了mesh_div_num的值，则按照自定义），计算出值ֵ
        id_ = 0
        for i in range(self.curr_archiving_in.shape[1]):
            id_dim = int((in_[i]-self.min_[i])*self.mesh_div/(self.max_[i]-self.min_[i]))#self.num_
            id_ = id_ + id_dim*(self.mesh_div**i)
        return id_
 
    def divide_archiving(self):
        #对每个粒子定义网格编号
        for i in range(self.num_):
            self.id_archiving[i] = self.cal_mesh_id(self.curr_archiving_in[i])
 
    def get_crowd(self):
        index_ = (np.linspace(0,self.num_-1,self.num_)).tolist()  #定义一个数组存放粒子集的索引号，用于辅助计算
        index_ = map(int, index_)
        while(len(index_) > 0):
            index_same = [index_[0]] #存放本次子循环中与index[0]粒子具有相同网格id所有检索位
            for i in range(1,len(index_)):
                if self.id_archiving[index_[0]] == self.id_archiving[index_[i]]:
                    index_same.append(index_[i])
            number_ = len(index_same) #本轮网格中粒子数
            for i in index_same: #更新本轮网格id下的所有粒子的拥挤度
                self.crowd_archiving[i] = number_
                index_.remove(i) #删除本轮网格所包含的粒子对应的索引号，避免重复计算
 
class get_gbest(mesh_crowd):
    def __init__(self,curr_archiving_in,curr_archiving_fit,mesh_div_num,min_,max_,particals):
        super(get_gbest,self).__init__(curr_archiving_in,curr_archiving_fit,mesh_div_num,min_,max_,particals)
        self.divide_archiving()
        self.get_crowd()
 
    def get_probability(self):
        for i in range(self.num_):
            self.probability_archiving = 1.0/(self.crowd_archiving**3)#10/
        self.probability_archiving = self.probability_archiving/np.sum(self.probability_archiving) #归一化，粒子被选择概率为1
 
    def get_gbest_index(self):
        random_pro = random.uniform(0.0,1.0) #有点像轮盘赌，概率越高（拥挤度小），被选择的概率越大
        for i in range(self.num_): 
            if random_pro <= np.sum(self.probability_archiving[0:i+1]):
                return i #返回检索值ֵ
 
    def get_gbest(self):
        self.get_probability()
        for i in range(self.particals):
            gbest_index = self.get_gbest_index()
            self.gbest_in[i] = self.curr_archiving_in[gbest_index] #gbest坐标
            self.gbest_fit[i] = self.curr_archiving_fit[gbest_index] #gbest适应度ֵ
        return self.gbest_in,self.gbest_fit
 
class clear_archiving(get_gbest):
    def __init__(self,curr_archiving_in,curr_archiving_fit,mesh_div_num,min_,max_,particals):
        super(get_gbest,self).__init__(curr_archiving_in,curr_archiving_fit,mesh_div_num,min_,max_,particals)
        self.divide_archiving()
        self.get_crowd()
 
    def get_probability(self):
        for i in range(self.num_):
            self.probability_archiving = self.crowd_archiving/sum(self.crowd_archiving)
 
    def get_clear_index(self): #按概率清除粒子，拥挤度高的粒子被清除的概率越高
        len_clear = (self.curr_archiving_in).shape[0] - self.thresh #�#需要清除掉的粒子数量
        clear_index = []
        while(len(clear_index)<len_clear):
            random_pro = random.uniform(0.0,np.sum(self.probability_archiving)) #生成0-1的随机数
            for i in range(self.num_): 
                if random_pro <= np.sum(self.probability_archiving[0:i+1]):
                    if i not in clear_index:
                        clear_index.append(i) #记录检索值ֵ
                        break
        return clear_index
 
    def clear_(self,thresh):
        self.thresh = thresh
        #self.archiving_size = archiving_size
        self.get_probability()
        clear_index = self.get_clear_index()
        #gbest_index=self.get_gbest_index()
        self.curr_archiving_in = np.delete(self.curr_archiving_in,clear_index,axis=0) #删除存档中部分粒子
        self.curr_archiving_fit = np.delete(self.curr_archiving_fit,clear_index,axis=0) #删除存档中粒子适应度ֵ
        return self.curr_archiving_in,self.curr_archiving_fit
