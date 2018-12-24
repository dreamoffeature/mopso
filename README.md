# 多目标粒子群算法简单实现

 * [算法流程](#算法流程) 
 
 （1）初始化粒子数量、迭代次数、存档阈值；初始化粒子速度、位置、适应度值、pbest、gbest、存档；初始化惯性因子、速度因子<br>

   初始化的pbest为粒子本身；存档即将非劣解存起来，非劣解就是无法严格对比出好坏，即有些目标好，有些目标差；gbest即从存档中随机选择一个，拥挤度越高被选择的概率越低<br>
   拥挤度计算公式：
   ![密度计算](https://i.imgur.com/CebAhWp.png)
 
 （2）更新速度、位置、存档、pbest、gbest、拥挤度<br>
    ![速度更新公式](https://i.imgur.com/QzAj0kj.png)<br>
    ![位置更新公式](https://i.imgur.com/BU5iFFR.png)<br>
