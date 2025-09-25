#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 12:05:59 2025

@author: facu
"""
#%% Módulos necesarios
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from reportlab.lib import colors

#%% Configuracion CrearReporte
from config_reporte import *
from version0 import Medicion, Instrument, Client, Equipo, CrearReporte

# %%Genero bodeplots de fase y modulo
import numpy as np
from scipy import signal as sig
def graficar_H (H1, n=500):
    if(type(H1)!=None):
        w, mag_db, phase_deg = sig.bode(H1, n)  # w en rad/s
        fig, axes = plt.subplots(2,1)
        axes[0].semilogx(w, mag_db)
        axes[0].set_ylabel('Magnitud (dB)')
        axes[1].semilogx(w,phase_deg)
        axes[1].set_ylabel('Fase (deg)')
        axes[0].set_xlabel('Frecuencia (rad/s)')
        axes[1].set_xlabel('Frecuencia (rad/s)')
        axes[0].grid(True)
        axes[1].grid(True)
        plt.show()
        return axes
    else:
        raise TypeError("No es T.F.")

r=0;r1=1;r3=2;r4=3;r5=4
res=[20.,1.,1.,1.,1.]
c=0;c2=1
cap=[1.,1.]

res=np.array(res);
cap=np.array(cap);
num_des = np.array([ 1/(res[r]*cap[c]) *(1+res[r4]/res[r5]), 0.] )
den_des = np.array([ 1., 1/(res[r]*cap[c]), res[r4]/(res[r1]*res[r3]*res[r4]*cap[c2])*1/cap[c]])
H1_des = sig.TransferFunction( num_des, den_des )

axes1 = graficar_H(H1_des)
    
n=3
att_min=16
att_max=0.5
wc=1
ws=3
H_C_ba=sig.cheby1(n, att_max, wc, btype='lowpass', analog=True, output='ba', fs=None)
H_C = sig.TransferFunction(H_C_ba[0],H_C_ba[1])

axes2 = graficar_H(H_C)

# %%Valores a utilizar

name =["NOTCHN'T","CHEBY"]
RL = [1, 2]
n_points = [100, 100]
v_alim = [5,5]
v_s = [1e-3, 1e-3]
t=[1,10]
osc_2102 = Instrument(name="SDS 2102", typ="Osciloscopio")
gen_1032 = Instrument(name="SDG 1032X", typ="Generador de funciones")
fuente_vcc = Instrument(name="FUENTE", typ="Fuente de alimentación")

equipo_de_jose = Equipo(name="Equipo de jose", typ="Fltro BP")
jose = Client(name="Juan",equipo = equipo_de_jose, date_sol = datetime.now().strftime("%d/%m/%Y"), number = 1123344556)

condiciones_amb = {"Temperatura":"22°C", "Humedad":"56%","Presion":"1atm"} 
MAUX = Medicion(fig_id=[axes1[0].figure,axes2[0].figure], axe_id=[axes1[0],axes2[0]], RL=RL, n_points=n_points, nombre=name, v_alim=v_alim, v_s=v_s, t=t)
medido = MAUX.list_
#CrearReporte(filter_f=True, magn_arr=None, phase_arr=None, client = None, emiter=None, instruments=None, id_report=None, cond_amb= None, mediciones = None):
CrearReporte(client = jose, emiter = Emisor, instruments=[osc_2102,gen_1032,fuente_vcc],cond_amb = condiciones_amb, mediciones= medido)        
#%% Imports de Signal
# import matplotlib.pyplot as plt
# import numpy as np
#Importo signals de tratamiento de senales
# import sys
# import os
# # Ruta absoluta a la carpeta
# ruta_ME1 = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(ruta_ME1)
# from TratamientoSenales import Signal

# #%%     PARÁMETROS E INICIALIZACION
# SRC_PATH = "/home/facu/MEI/13_06_files/"
# CH1_PATH = "DS0005_CH1_100us_ESTESI.CSV"
# CH2_PATH = "DS0006_CH2_100us_ESTETMB.CSV"
# ROW_START = 20
# COL_XY = (0,1)

# R = 1e3
# C = 100e-9

# ch1 = Signal(src_path=SRC_PATH, path=CH1_PATH)
# ch1.open_csv()
# ch1.get_xy(col_y= COL_XY[1] , col_x = COL_XY[0], row_start= ROW_START)
# ch1.set_xy_name(("tiempo", "vg"))

# ch2 = Signal(src_path=SRC_PATH, path=CH2_PATH)
# ch2.open_csv()
# ch2.get_xy(col_y= COL_XY[1] , col_x = COL_XY[0], row_start= ROW_START)
# ch2.xy[type(ch2).Y] = ch2.xy[type(ch2).Y] / R
# ch2.set_xy_name(("tiempo", "ir"))

# vg_id = ch1.plot()
# ir_id = ch2.plot(ext_signal = ch1)




# #%%
# plt.savefig('grafico1.png')
