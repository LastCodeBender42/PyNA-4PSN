#!/usr/bin/python
import sys, os
import pymol
import pandas as pd
cmd = pymol.cmd

# cmd.fetch('1yok')

cmd.hide('lines')
cmd.show('sticks')

with open("node_weights.txt", "r") as ec:
    lines = ec.readlines()
    n = 0
    ecVals = []
    resVals = []
    for i in lines:   
        ecVals.append(float(i.strip()))
    for i in range(len(ecVals)):
        resVals.append("resi " + str(300+i))
        
    mapVals = [list(a) for a in zip(resVals, ecVals)]
    
    for i in mapVals:
        j,k = i
        colname = "col" + str(n)
        cmd.set_color(colname ,[1.00 , 1.00-k , 1.00-k])
        cmd.color(colname, j)
        n += 1

    df = pd.read_csv("edge_weights.txt", sep=",")
    for i in range(len(df)):
        c,a,b = str(df.iloc[i,0]),str(df.iloc[i,2]),str(df.iloc[i,3])
        c=float(c)
        cmd.bond(("resi " + a + " and name CA"), ("resi " + b + " and name CA"))
        cmd.set_bond("stick_radius", 10.0*c, ("resi " + a + " and name CA"), ("resi " + b + " and name CA"))
        cmd.set_bond("line_color", "red", ("bond resi " + a + " and name CA"), ("bond resi " +  b +  " and name CA"))
        cmd.show("sticks", ("resi " + a + " and name CA , resi " + b + " and name CA"))


cmd.bg_color("white")
cmd.remove("resn HOH")

cmd.hide('sticks', '(polymer and not (name ca))')
cmd.png('1yokSetColor5.png', 600, 600)
