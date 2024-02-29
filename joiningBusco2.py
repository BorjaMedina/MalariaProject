#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:59:40 2024

@author: inf-47-2023
"""

import sys

try:
    BUSCO = sys.argv[1]
    
except:
    print("Run program like: cleaningScaffolds.py species.genome scaffolds.txt output.fasta")
    sys.exit()


with open(BUSCO, "r") as genes:
    genes=genes.readlines()


for x in genes:

    
    try:
        with open(("Ht/"+x).strip(), "r") as Ht:
            Ht=Ht.readlines()
            Ht.pop(0)
            Ht=[">Ht\n","".join(Ht).replace("\n",""),"\n"]
            
        with open(("Pb/"+x).strip(), "r") as Pb:
            Pb=Pb.readlines()
            Pb.pop(0)
            Pb=[">Pb\n","".join(Pb).replace("\n",""),"\n"]
  
        with open(("Pc/"+x).strip(), "r") as Pc:
            Pc=Pc.readlines()
            Pc.pop(0)
            Pc=[">Pc\n", "".join(Pc).replace("\n",""),"\n"]
    
        with open(("Pk/"+x).strip(), "r") as Pk:
            Pk=Pk.readlines()
            Pk.pop(0)
            Pk=[">Pk\n","".join(Pk).replace("\n",""),"\n"]

        with open(("Pv/"+x).strip(), "r") as Pv:
            Pv=Pv.readlines()
            Pv.pop(0)
            Pv=[">Pv\n","".join(Pv).replace("\n",""),"\n"]

        with open(("Py/"+x).strip(), "r") as Py:
            Py=Py.readlines()
            Py.pop(0)
            Py=[">Py\n","".join(Py).replace("\n",""),"\n"]

        with open(("Pf/"+x).strip(), "r") as Pf:
            Pf=Pf.readlines()
            Pf.pop(0)
            Pf=[">Pf\n","".join(Pf).replace("\n",""),"\n"]

        with open(("Tg/"+x).strip(), "r") as Tg:
            Tg=Tg.readlines()
            Tg.pop(0)
            Tg=[">Tg\n","".join(Tg).replace("\n",""),"\n"]
    
        total=Ht+Pc+Pb+Pf+Pk+Pv+Py+Tg
        
        with open(x.strip(), "w") as output:
            output.writelines(total)
            
    except FileNotFoundError:
        pass

   


