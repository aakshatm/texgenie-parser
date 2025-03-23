# Evolutionary Inspired Approach for Mental Stress Detection using EEG Signal  

Lakhan Dev Sharma1 devsharmalakhan@gmail.com Vijay Kumar Bohat $^2$ vijay.bohat@gmail.com Maria Habib $^3$ , Ala’ M. Al-Zoubi4 5, Hossam Faris $^{3,4}$ ,6 ,7, Ibrahim Aljarah $^4$ maria.habib@altibbi.com, ala.m.zoubi@gmail.com, hossam.faris@ju.edu.jo,i.aljarah@ju.edu.jo,  

1 School of Electronics Engineering, VIT-AP University, India $^2$ Department of Computer Science & Engineering, Netaji Subhas University of Technology, Delhi, India $^{3}$ Altibbi (https://altibbi.com), Amman, Jordan. 4Information Technology Department, The University of Jordan. Amman, Jordan.  

5School of Science, Technology and Engineering, University of Granada, Granada, Spain 6School of Computing and Informatics, Al Hussein Technical University, Amman, Jordan, $^7$ Research Centre for Information and Communications Technologies of the University of Granada (CITIC-UGR), University of Granada, Granada, Spain  

# Abstract  

Stress is a pensive issue in our competitive world and it has a huge impact on physical and mental health. Severe health issues may arise due to long exposure of stress. 

Keywords: Mental stress, Electroencephalogram, Stationary Wavelet Transform, Evolutionary Inspired, Whale Optimization Algorithm, Support Vector Machine.  

# 1. Introduction  

# 1.1. Motivation  

Stress in general terms has been perceived as a state, where an individual feel troubled and attempts to meet the social and psychological demands. These demands can arise due to change in financial, relationship, work and other similar conditions in which an individual feels pressurized. 

Traditionally, subjective methods like interviews and questionnaires are used for assessing stress (Sharma & Gedeon (2012)). 

# 1.2. Related Work  

Apart from effecting brain and nervous system stress can bring changes in heart rate variability (HRV), respiration, blood pressure, and skin conductance (Wielgosz et al. (2016); Paiva et al. (2016); He et al. (2019); Healey & Picard (2005)). Researchers have proposed various techniques for stress detection using bio-signals like: electrocardiogram (ECG), Galvanic Skin Response (GSR), and electroencephalography (EEG).  

# 2. Database  

This section discusses the database used for this research work and protocol adopted during signal recording. 

![](images/b92d712fcf89518a10c69122e1cfe2f27d2373e33993274427d2dc4380668c54.jpg)  
Figure 1: 10–20 EEG electrode positions (Used leads are marked blue).  

# 3. Background  

# 3.0.1. Support vector machine (SVM)  

SVM is a well-established mathematical and supervised machine learning algorithm proposed by Boser et al. in 1992. It has been deeply considered by the research community to address plenty of problems in various fields like in medicine, engineering, text classification, image segmentation, and pattern recognition (Huang et al. (2018); Ord6nez et al. (2019); Faris et al. (2018); Aljarah et al. (2018); Ala’M et al. (2021); Obiedat et al. (2021)).  

Generally speaking, given a classification problem with data of $d$ -dimensional variables, where the data can be represented as $[(x_{1},y_{1}),(x_{2},y_{2}),....(x_{m},y_{m})]$ where, $x\in$ $\Re^{d}$ and $y\in\{-1,+1\}$ . The aim is to find the decision-plane function $f(x)$ that maximizes the marginal distance.  

Given, a linearly separable data, $f(x)$ is represented by Eq. 1.  

$$
f(x):w^{T}\cdot x+b=0
$$  

Where, $(w)$ presents the hyperplane’s weight vector, and $(b)$ is a threshold. By knowing that $y\in\{-1,+1\}$ , then the training data should obey Eqs. 2 and 3.  

$$
w^{T}\cdot x_{i}+b\geq1,y_{i}=+1
$$  

$$
w^{T}\cdot x_{i}+b\leq-1,~y_{i}=-1
$$  

However, since the distance between a boundary and the decision-plane that is in the middle is $\left({\frac{1}{\left|\left|w\right|\right|}}\right)$ . Therefore, the objective is to maximize the distance $\left({\frac{2}{\left|\left|w\right|\right|}}\right)$ or to minimize $\left({\frac{||w||^{2}}{2}}\right)$ as shown by Eq. 4 (the primal form), where $||w||=\sqrt{w^{T}w}$ . Thereby, to classify a new data point $(a)$ , then the final decision is given by Eq. 5.  

$$
M i n.~\frac{||w||^{2}}{2}
$$  

$$
f(a)=s g n(w^{T}\cdot a+b)
$$  

In contrast, considering non-separable data results in integrating a new penalizing parameter which is the slack variable $(\zeta_{i})$ . Subsequently, the objective function is adjusted as in Eq. 6 by considering the potential errors, where (C) is a regularization parameter between the margin and slack penalty coefficient.  

$$
\begin{array}{c}{{M i n.\frac{\lvert|w\rvert|^{2}}{2}+C\displaystyle\sum_{i=1}^{n}\zeta_{i},}}\ {{s.t.y_{i}(w^{T}\cdot x_{i}+b)\geq1-\zeta_{i}}}\ {{i=1,....n,\zeta_{i}\geq0}}\end{array}
$$  
A remarkable aspect of SVM algorithm is the integration of kernel functions to handle the non-linearly separable data. It transforms the data into a multi-dimensional space to capture the non-linear relationship within the data by linear-hyperplanes existed in the higher spaces. SVM algorithm adopts various kinds of kernels, like the linear kernel, and the Radial Basis Function (RBF). For instance, the RBF kernel can be used to deal with nonlinear variables and search for non-linear decision boundaries. The RBF kernel is defined by Eq. 7, where, $(\gamma)$ is the gamma coefficient.  
 

# 3.0.2. Whale Optimization Algorithm  

The WOA algorithm is a nature-inspired metaheuristic and stochastic optimization algorithm that was developed by Mirjalili $\&$ Lewis (2016). Mainly, the proposal of WOA is inspired by the intelligent social behavior of Humpback whales and their attacking strategy which is known by the bubble-net. Humpbacks attack the preys (supposing a school of fishes close to the surface of the sea) in a spiral way, while creating bubbles during the path toward the preys.  



$$
\vec{D}=|\vec{C}\cdot\vec{X^{*}(t)}-\vec{X(t)}|
$$  

$$
\vec{X}(t+1)=\vec{X^{*}(t)}-\vec{A}\cdot\vec{D}
$$  

![](images/ab40e7534200a28ad0392017099aeeaafed80ecd772ea2abf9eef4ad45a1a838.jpg)  
Figure 2: A description of SVM algorithm. (a) where it utilizes the support vectors near the class boundary to maximize the margins. (b) non-optimal hyperplanes. (c) non-linearly separable data.  


$$
\overset{\vartriangle}{\vec{A}}=2\vec{a}\cdot\vec{r}-\vec{a}
$$  

$$
{\vec{C}}=2\cdot{\vec{r}}
$$  

Typically, the bubble-net attacking strategy can be formulated by two approaches; the shrinking encircling method, and the spiral updating position. The former is accomplished by decreasing the value of $\vec{a}$ . In contrast, in the latter; the distance between a whale at location (X,Y) and the prey in $(X^{*},Y^{*})$ is modelled by a function that imitates the helix-shaped movement of Humpbacks, as shown by Eq. 12. Where, $\vec{D}^{'}$ is given by Eq. 13, $b$ is a constant for specifying the shape of the logarithmic spiral, and $\textit{l}$ is a random number $\in[-1,1]$ .  

$$
\vec{X}(t+1)=\vec{D}^{^{\prime}}\cdot e^{b l}\cdot c o s(2\pi l)+\vec{X^{*}(t)}
$$  

$$
\vec{D^{'}}=|\vec{X^{*}}(t)-\vec{X(t)}|
$$  

Modeling the Humpback whales to use the two attacking approaches simultaneously require a threshold parameter $(p)$ to be integrated. For which, the resulting model is characterized by Eq. 14.  

$$
\begin{array}{r}{\vec{X}(t+1)=\left\{\begin{array}{l l}{\vec{X}^{*}(t)-\vec{A}\cdot\vec{D}}&{i f p<0.5}\ {\vec{D}^{'}\cdot e^{b l}\cdot c o s(2\pi l)+X^{*}(t)}&{i f p\geq0.5}\end{array}\right.}\end{array}
$$  



$$
\vec{D}=|\vec{C}\cdot\vec{X}_{r a n d}-\vec{X}|
$$  
  

# Algorithm 1 Pseudo-code of WOA  

Initialize the WOA population $X_{i}(i=1,2,\dots,n)$   
Calculate the fitness of each search agent, and set $\vec{X^{*}}$   
as the best   
while $t<M a x$ iterations) do for (each search agent) do Update $\vec{a}$ , $\vec{A},\bar{\vec{C}},1$ p if $\left(p<0.5\right)$ then if $(|\vec{A}|<1)$ then Update the agent’s position according to   
Eq. 9 else if $(|\vec{A}|\ge1)$ then Select random search agent $\left(X_{r a n d}^{\rightarrow}\right)$ Update the agent’s position according to   
Eq. 15 end if else if $\mathit{\check{p}}\geq0.5\$ then Update the agent’s position according to Eq.   
12 end if end for Check the lower and upper bounds of search agents Calculate the fitness of all search agents Update $\vec{X^{*}}$ if there is a better solution $t=t+1$   
end while  

return $\vec{X^{*}}$  

$$
\vec{X}(t+1)=\vec{X}_{r a n d}-\vec{A}\cdot\vec{D}
$$  

