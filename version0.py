#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 12:33:38 2025

@author: facu
"""

"""
IDEA DE TABLA

https://docs.google.com/document/d/1VMYdzl9J-h5e4MDn2IjW-6AdnLMQeB59aEyGwQ72WYY/edit?usp=sharing
"""

class Instrument:
    id_ = 0
    list_ = []
    types_ = ("Osciloscopio", "Generador de funciones", "Fuente de alimentación")
    
    def __init__(self, name, typ):
        
        if(type(name)!=str):
            return
        if(type(typ)!=str):
            return        
        self.name=name
        self.typ=typ
        type(self).list_.append(self)
        
        
class Equipo:
    id_ = 0
    list_ = []
    types_ = ("Filtro BP", "Filtro LP", "Filtro HP")
    
    def __init__(self, name, typ):
        
        if(type(name)!=str):
            return
        if(type(typ)!=str):
            return        
        self.name=name
        self.typ=typ
        type(self).list_.append(self)
        
        
class Client:
    id_ = 0
    list_ = []
    
    def __init__(self, name, equipo, date_sol, number):
    #Chequeo de tipos de dato
        if(type(name)!=str):
            return
        if(equipo!=None):
            if(type(equipo)!=Equipo):
                raise TypeError("Error de tipo")
        self.name = name
        self.date_sol = date_sol
        self.number = number
        self.equ = equipo
        
        self.id_ = type(self).id_
        type(self).id_ = type(self).id_ + 1
        
        # self.inst_list = []
        # self.inst_list.append(inst)

class Medicion:
   
    list_ = []
    def __init__(self, fig_id, axe_id, RL, n_points, nombre, v_alim, v_s,t,ou_flag = False):
    #Chequeo de tipos de dato
        cls = type(self)
        # if(type(fig_id)==list and type(axe_id) == list and len(fig_id)==len(axe_id) == len(RL) == len(nombre) == len(n_points)):
            
        #     for n in range (len(fig_id)):                
        #         Medicion(fig_id= fig_id[n], axe_id = axe_id[n], RL = RL[n], n_points = n_points[n],nombre = nombre[n], ou_flag = True)            
        #     if(len(cls.list_)>=len(fig_id)):
        #         nuevos_elementos = len(fig_id)
        #     else:
        #         raise ValueError("Falló la creación de objetos")
        #     print("Hay "+str(nuevos_elementos)+ " nuevos elementos")
        if(type(fig_id)==list and type(axe_id)==list and type(RL)==list and type(nombre)==list and type(n_points)==list and type(v_alim)==list and type(v_s)==list and type(t)==list and len(fig_id)==len(axe_id) == len(RL) == len(nombre) == len(n_points) == len(v_alim)==len(v_s)==len(t)):
            self.list_ = []
            for n in range (len(fig_id)):                
                self.list_.append(Medicion(fig_id= fig_id[n], axe_id = axe_id[n], RL = RL[n], n_points = n_points[n],nombre = nombre[n], v_alim = v_alim[n],v_s = v_s[n],t = t[n],ou_flag = True))
            cls.list_.append(self)
            self.id_=len(cls.list_)
            print("Se agregaron "+str(len(self.list_))+" mediciones")
            
        if(type(fig_id)!=list and type(axe_id)!=list and type(RL)!=list and type(nombre)!=list and type(n_points)!=list and type(v_alim)!=list and type(v_s)!=list and type(t)!=list):
            self.fig_id = fig_id
            self.axe_id = axe_id
            self.RL = RL
            self.nombre = nombre
            self.n_points = n_points
            self.v_alim = v_alim
            self.t = t
            self.v_s = v_s

            if(ou_flag == False):
                cls.list_.append(self)
                self.id_ = len(cls.list_)
                print("Se agregó 1 medición")
    
        
        # self.inst_list = []
        # self.inst_list.append(inst)
#%%
from datetime import datetime

osc_2102 = Instrument(name="SDS 2102", typ="Osciloscopio")
gen_1032 = Instrument(name="SDG 1032X", typ="Generador de funciones")
fuente_vcc = Instrument(name="FUENTE", typ="Fuente de alimentación")

equipo_de_jose = Equipo(name="Equipo de jose", typ="Fltro BP")
jose = Client(name="Juan",equipo = equipo_de_jose, date_sol = datetime.now().strftime("%d/%m/%Y"), number = 1123344556)

condiciones_amb = {"Temperatura":"22°C", "Humedad":"56%","Presion":"1atm"}

fig_id=[2,2]
axe_id = [1,1]
name =["fase","magn"]
RL = [1, 2]
n_points = [100, 100]
v_alim = [5,5]
v_s = [1e-3, 1e-3]
t=[1,10]
pruebas = Medicion(fig_id= fig_id, axe_id = axe_id, RL=RL, n_points=n_points,nombre=name, v_alim=v_alim, v_s=v_s, t=t)
prueba = Medicion(fig_id= 1, axe_id = 2, RL=1e3, n_points=100,nombre="medicion primera",v_alim=5,v_s=1e-3,t=10)
#%%
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from config_reporte import *




def CrearReporte(filter_f=True, magn_arr=None, phase_arr=None, client = None, emiter=None, instruments=None, id_report=None, cond_amb= None, mediciones = None):
    #Revisión tipo de datos
    # -------
    #Creo objeto PDF
    pdf_name = "Reporte"+emiter['id_report'] + ".pdf"
    pdf = SimpleDocTemplate(pdf_name, pagesize=A4)
    col_w = pdf.pagesize[0] - pdf.leftMargin-pdf.rightMargin #En cada tabla, dividir por cantidad de columnas
    elementos = [] #Encapsula los elementos platypus del pdf
    #CREO LAS DISTINTAS PARTES
    
    #Titulo  = TÍTULO
    Titulo = Paragraph("<u>REPORTE FRA</u>", Titulo_style)
    elementos.append(Titulo)
    
    #Tabla1 = DATOS EMISOR
    datos_t1 = [
            [Paragraph("Datos emisor:",Subtitulo_style) ],
            [Paragraph("Organismo emisor: "+emiter['nombre'], Texto_style), Paragraph("Id_certificado: "+str(id_report), Texto_style)]
            ]
    #Tabla1 = Table(datos_emisor,colWidths=COL_W, rowHeights=ROW_H, hAlign='LEFT')
    Tabla1 = Table(datos_t1, colWidths=col_w/len(datos_t1[1]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE,splitByRow=0)
    Tabla1.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
        # ,('FONTSIZE',(0,0),(-1,-1), TEXT_SIZE)
        # ,('FONTNAME',(0,0),(-1,-1),TEXT_FONT)
        # ,('FONTNAME', (0,0),(0,0), SUBT_FONT)
        # ,('FONTSIZE',(0,0),(0,0),SUBT_SIZE)
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ]))
    elementos.append(KeepTogether([Tabla1]))
    
    #Tabla2 = DATOS SOLICITANTE
    datos_t2 = [
            [Paragraph("Datos solicitante:", Subtitulo_style)]
            ,[Paragraph("Nombre: "+client.name, Texto_style), Paragraph("Fecha solicitud: "+client.date_sol, Texto_style), Paragraph("Contacto: "+str(client.number), Texto_style)]
            ]
    Tabla2 = Table(datos_t2, colWidths=col_w/len(datos_t2[1]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE, splitByRow=0)
    Tabla2.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
        # ,('FONTSIZE',(0,0),(-1,-1), TEXT_SIZE)
        # ,('FONTNAME',(0,0),(-1,-1),TEXT_FONT)
        # ,('FONTNAME', (0,0),(0,0), SUBT_FONT)
        # ,('FONTSIZE',(0,0),(0,0),SUBT_SIZE)
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ]))
    elementos.append(KeepTogether([Tabla2]))
    
    #Tabla3 = DATOS EQUIPO
    datos_t3 = [
            [Paragraph("Datos equipo a medir:", Subtitulo_style)]
            ,[Paragraph("Nombre: "+client.equ.name, Texto_style), Paragraph("Tipo: "+client.equ.typ, Texto_style)]
            ]
    Tabla3 = Table(datos_t3, colWidths=col_w/len(datos_t3[1]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE, splitByRow=0)
    Tabla3.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
        # ,('FONTSIZE',(0,0),(-1,-1), TEXT_SIZE)
        # ,('FONTNAME',(0,0),(-1,-1),TEXT_FONT)
        # ,('FONTNAME', (0,0),(0,0), SUBT_FONT)
        # ,('FONTSIZE',(0,0),(0,0),SUBT_SIZE)
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ]))
    elementos.append(KeepTogether([Tabla3]))
    #Tabla4 = DATOS MEDICION
    datos_t4 = [
            [Paragraph("Datos medición:", Subtitulo_style)]
            ,[Paragraph("Modelo "+instruments[0].typ+":<br/>"+instruments[0].name, Texto_style), Paragraph("Modelo "+instruments[1].typ+":<br/>"+instruments[1].name,Texto_style), Paragraph("Modelo "+instruments[2].typ+":<br/>"+instruments[2].name, Texto_style)]
            ,[Paragraph("Temperatura ambiente:"+str(cond_amb['Temperatura']), Texto_style), Paragraph("Humedad relativa:"+cond_amb["Humedad"],Texto_style), Paragraph("Presion atmosférica"+ cond_amb["Presion"], Texto_style)]
            ,[Paragraph("Fecha de realización: "+datetime.now().strftime("%d/%m/%Y"),Texto_style), Paragraph("Fecha de emisión: "+ datetime.now().strftime("%d/%m/%Y"),Texto_style)]
            ]
    
    Tabla4 = Table(datos_t4, colWidths=col_w/len(datos_t4[1]), rowHeights=[25, None, None, None],  hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE, splitByRow=0)
    Tabla4.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)                
        # ,('FONTSIZE',(0,0),(-1,-1), TEXT_SIZE)
        # ,('FONTNAME',(0,0),(-1,-1),TEXT_FONT)
        # ,('FONTNAME', (0,0),(0,0), SUBT_FONT)
        # ,('FONTSIZE',(0,0),(0,0),SUBT_SIZE)
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ,('TOPPADDING', (0,2), (-1,-1),4)
        ]))
    elementos.append(KeepTogether([Tabla4]))
    elementos.append(PageBreak())
    #TablaN = MEDICIONES
    #Si es una lista de mediciones, imprimo todas...
    if(type(mediciones)==Medicion):
        mediciones = [mediciones] 
    if(type(mediciones)==list):
        i = 0
        for medicion in mediciones:

            string = "foto"+str(i)+".png"
            i+=1
            medicion.axe_id.figure.savefig(string)
            img = Image(string, width=IMG_W, height=IMG_H)

            datos_tN = [
                [Paragraph(str(medicion.nombre),Subtitulo2_style)]
                ,[Paragraph("Valimentación: "+str(medicion.v_alim)+"V"+SPACE+"Vseñal: "+str(medicion.v_s)+"V"+SPACE+"Tiempo de toma: "+str(medicion.t)+"s"+SPACE+"Numero de puntos: "+str(medicion.n_points)+"pts"+SPACE+"Resistencia de carga: "+str(medicion.RL)+"ohm", Texto_style)]
                ,[Paragraph("Fci:"+"FrecCorteInf"+"Hz",Texto_style),Paragraph("Fcs: "+"FrecCorteSup"+"Hz", Texto_style)]
                ,[img]
                ]
            TablaN = Table(datos_tN, colWidths=col_w/len(datos_tN[2]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE)
            TablaN.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
                ('BACKGROUND',(0,0),(-1,0),colors.lightblue)
                ,('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
                ,('SPAN', (0,1), (-1,1)) #Uno segunda fila (especificaciones)
                ,('SPAN', (0,-1), (-1,-1)) 
                #,('Background',(0,1),(-1,1),colors.H
                ,('VALIGN',(0,0),(-1,-1),'TOP')
                ,('ALIGN',(0,0),(-1,-1),'CENTER')
                ,('TOPPADDING', (0,0), (-1,-1),0)
                ,('BOTTOMPADDING', (0,0), (-1,-1),0)
                ,('TOPPADDING', (0,2), (-1,-1),4)
               # , ("GRID", (0,0), (-1,-1), 0.5, colors.black)  # todas las líneas internas
               # ,("INNERGRID", (0,0), (-1,-1), 0, colors.red)
                 ,("BOX", (0,0), (-1,-1), 2, colors.black)  
               ]))
            elementos.append(KeepTogether([TablaN]))
            # recortar al bbox del Axes
            # fig.savefig("solo_axes.png", bbox_inches=axs[0,0].get_tightbbox(fig.canvas.get_renderer()))
    
    
    pdf.build(elementos)
    
#CrearReporte(client=jose, emiter=Emisor, instruments=[osc_2102,gen_1032,fuente_vcc],cond_amb=condiciones_amb)