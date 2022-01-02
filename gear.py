
class Spurgear():
  from math import pi,sin
  import numpy as np
  import pandas as pd
  import joblib
  from scipy.interpolate import interp1d
  from sklearn.preprocessing import PolynomialFeatures
  from sklearn.linear_model import LinearRegression
  
  def __init__(self,condition,alpha,Power,Sigma_01,Sigma_02,Cs,N1,N2,z1,z2,E1,E2,i =0,m=1.25):
      self.alpha = alpha
      self.P = Power
      self.N1 = N1
      self.N2 = N2
      self.z1 = z1
      self.z2 = z2
      self.m = m
      self.Sigma_01 = Sigma_01
      self.Sigma_02 = Sigma_02
      self.i = i
      self.condition = condition
      self.Cs = Cs
      self.E1 = E1
      self.E2 = E2
      self.__prepare__()

  def __prepare__(self):
    if self.N2 == 0:
      if self.z2 == 0:
        self.N2 = self.N1/self.i
      else:
        self.i = self.z2/self.z1
        self.N2 = self.N1/self.i
    elif self.z2 ==0:
      if self.N2 == 0:
        self.z2 = self.z1*self.i
      else:
        self.i = self.N1/self.N2
        self.z2 = self.z1*self.i
    
  
  def __weaker_mem__(self):
    if self.alpha == 1:
      self.y1 = 0.124 - 0.684/self.z1
      self.y2 = 0.124 - 0.684/self.z2
    elif self.alpha == 2:
      self.y1= 0.154-0.912/self.z1
      self.y2= 0.154-0.912/self.z2
    elif self.alpha == 3:
      self.y1 = 0.175 - .95/self.z1
      self.y2 = 0.175 - .95/self.z2
    if self.Sigma_01*self.y1 < self.Sigma_02*self.y2:
      self.sigma = self.Sigma_01
      self.y = self.y1
      return True
    else:
      self.sigma = self.Sigma_02
      self.y = self.y2
      return False

  def tangential_tooth_load(self):
    v_p_m=self.pi*self.z1*self.N1/60000
    v_g_m=self.pi*self.z2*self.N2/60000
    weaker_member = self.__weaker_mem__()
    if weaker_member:
      self.teeth = self.z1
      self.rpm = self.N1
      self.Ft_tan = 1000*self.P*self.Cs/v_p_m
      return self.Ft_tan
    else:
      self.teeth = self.z2
      self.rpm = self.N2
      self.Ft_tan = 1000*self.P*self.Cs/v_g_m
      return self.Ft_tan

  def lewis_tangential(self):
    self.Ft_lewis = self.sigma * 10 * self.y * self.pi
    return self.Ft_lewis

  def m3Kv(self):
    self.tangential_tooth_load()
    self.lewis_tangential()
    self.m3_Kv = self.Ft_tan/self.Ft_lewis
    return self.m3_Kv
  
  def pitch_line_velocity(self):
    self.V_m = (self.pi * self.teeth * self.rpm)/60000
    return self.V_m

  def module(self):
    mod = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 25, 32, 40, 50, 60, 80, 100]
    self.m3Kv()
    self.pitch_line_velocity()
    for m in mod:
      self.Vm = self.V_m * m
      if self.Vm <= 8:
        Cv = 3.05/(3.05 + self.Vm)
      elif self.Vm <= 13:
        Cv = 4.58/(4.58 + self.Vm)
      elif self.Vm <= 20:
        Cv = 6.1/(6.1 + self.Vm)
      else:
        Cv = 0.7625/(1.0167 + self.Vm)
      if (m ** 3) * Cv >= self.m3_Kv:
        break
    self.Ft = self.Ft_tan/m
    self.Ft_lew = self.Ft_lewis *Cv*m*m
    self.m = m
    self.Cv = Cv
    self.b = 10 * m
    self.d1 = self.z1*m
    self.d2 = self.z2 * m
    return self.m
  
  def check_for_stress(self):
    self.module()
    sigma_allowable = self.sigma * self.Cv
    sigma_induced = self.Ft_tan/(self.m * 10 * self.m * self.y * self.pi * self.m)
    if sigma_allowable > sigma_induced:
      return 'The gears are safe'
    else:
      return 'Change material of gears'

  def __error1__(self):
    self.module()
    lin_reg2 = self.joblib.load('linear_model.sav')
    poly_reg = self.joblib.load('polynomial_preprocess.sav')
    self.e = lin_reg2.predict(poly_reg.fit_transform(self.np.array([[self.Vm]])))[0,0]

  def dynamic_fac(self):
    er = self.pd.read_csv('Deformationfactor.csv')
    t1 =[c for c in er.columns]
    t1 = [float(i) for i in t1[2:]]
    t = er.query(f'Material1 == {self.condition}').query(f'Toothform == {self.alpha}').to_numpy()
    self.__error1__()
    y = t[0,2:]
    C_interp = self.interp1d(t1,y)
    self.C = C_interp(self.e)
    return self.C



  def dynamic_load(self):
    self.module()
    self.dynamic_fac()
    self.Fd= self.Ft + 20.67*self.Vm*(self.C* self.b + self.Ft)/(20.67* self.Vm+ (self.C* self.b + self.Ft)**(1/2))
    return self.Fd
  
  def ang(self):
    angles = {1:self.pi*14.5/180,2:self.pi*20/180,3:self.pi*20/180}
    self.angle = angles[self.alpha]

  def __s_fac__(self):
    self.ang()
    load_factor_k=self.sin(self.angle)*(1/self.E1 + 1/self.E2)/1.4
    wear_load=self.d1*self.b*(2*self.z2/(self.z1+self.z2))
    self.s_fac_val=(self.Fd/(wear_load*load_factor_k))**.5

  def BHN(self):
    self.module()
    self.dynamic_load()
    self.__s_fac__()
    bhntable = self.pd.read_csv('S_fac&BHN.csv')
    t = bhntable[bhntable['s_fac'] >= self.s_fac_val].iloc[0,:]
    self.BHN1 = t['BHN']
    self.BHN2 = t['BHN2']
    return (self.BHN1,self.BHN2)


  

  