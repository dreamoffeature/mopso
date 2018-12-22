#encoding: utf-8
import random
import numpy as np
import archive
import pareto
def init_designparams(particals,in_min,in_max):
    in_dim = len(in_max)     #输入参数维度
    in_temp = np.zeros((particals,in_dim))
    for i in range(particals):
        for j in range(in_dim):
            in_temp[i,j] = random.uniform(0,1)*(in_max[j]-in_min[j])+in_min[j]    
    return in_temp
def init_v(particals,v_max,v_min):
    v_dim = len(v_max)     #输入参数维度
    v_ = np.zeros((particals,v_dim))
    for i in range(particals):
        for j in range(v_dim):
            v_[i,j] = random.uniform(0,1)*(v_max[j]-v_min[j])+v_min[j]
    return v_
def init_pbest(in_,fitness_):
    return in_,fitness_
def init_archive(in_,fitness_):
    pareto_c = pareto.Pareto_(in_,fitness_)
    curr_archiving_in,curr_archiving_fit = pareto_c.pareto()
    return curr_archiving_in,curr_archiving_fit
def init_gbest(curr_archiving_in,curr_archiving_fit,mesh_div,min_,max_,particals):
    get_g = archive.get_gbest(curr_archiving_in,curr_archiving_fit,mesh_div,min_,max_,particals)
    return get_g.get_gbest()
