

import warnings
warnings.filterwarnings('ignore')

import openpyxl
import xlsxwriter
import streamlit as st
import pandas as pd
from io import BytesIO
##
st.set_page_config(page_title="Densité des donateurs", page_icon=":large_blue_diamond:",layout="wide")
st.title(":large_blue_diamond: Densité des donateurs en 2023")

## Import de la base de données
fl = "IR-2023-Densite_de_donateurs_par_departement_prep.xlsx"
donateurs = pd.read_excel( fl, sheet_name = "ordre_dep")
df = pd.DataFrame(donateurs)
df["DENSITE (en %)"] = round(df["Densité"]*100,2)
df = df[["DEPARTEMENTS", "DENSITE (en %)"]]
df1 = df.loc[0:100, :]
moyenne = df.loc[102:102,]

## Préparation de la base
dep = pd.read_csv("v_departement_2023.csv", dtype = {"REG" : str })
reg = pd.read_csv("v_region_2023.csv", dtype = {"REG" : str })
def transformation (i : str):
    return i.replace("'"," ").replace("-"," ")
df1["DEPARTEMENTS_"]= df1["DEPARTEMENTS"].map(transformation)
df2 = df1.merge(dep, left_on ="DEPARTEMENTS_",right_on= "NCC",how = "left", validate = "m:1")
df3 = df2.merge(reg, on ="REG",how = "left", validate = "m:1")
df4 = df3[["DEP","LIBELLE_x","LIBELLE_y", "DENSITE (en %)"]]
df4 = df4.rename(columns = {"LIBELLE_x" : "DEPARTEMENT","LIBELLE_y" : "REGION" })
#st.write(df4, use_container_width=True)

## Création des filtres
st.sidebar.header("Choisissez votre filtre :")
region =st.sidebar.multiselect("Choisissez votre région", df4["REGION"].unique())
if not region :
    df5 = df4.copy()
else :
    df5 = df4[df4["REGION"].isin(region)]

## Affichage
st.subheader("Densité des donateurs par départements")
"""**Définition de densité de donateurs**"""
"Nombre de foyers imposés à l'impôt sur le revenu ayant déclaré un don en 2023 sur l'ensemble des foyers imposés"
st.dataframe(df5,use_container_width = None,hide_index = True,)
##
buffer = BytesIO()
with pd.ExcelWriter(buffer, engine = "xlsxwriter") as writer:
    df5.to_excel(writer, sheet_name = "Densité des donateur en 2023", index = False)
st.download_button(label="Télécharger les données", data=buffer , file_name="Densité des donateurs.xlsx", mime="application/vnd.ms-excel",
                help="Cliquez ici pour télécharger les données au format XLSX")
