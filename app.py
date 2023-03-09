# Librerias
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly_express as px


# ---------------CONFIGURACION DE LA PAGINA--------------------
st.set_page_config(page_title= "TITANIC" , layout= "centered", page_icon="🚢")

# ------------------Leemos el DataFrame---- -------------------

df = pd.read_csv(r"TITANIC/TITANIC_limpio.csv")
df2 = pd.read_csv(r"TITANIC/titanic.csv")
# ------------------EMPIEZA NUESTRA APP----------------------------

st.image("https://www.lavanguardia.com/files/image_948_465/uploads/2018/06/29/5fa43d002c905.jpeg")
st.markdown("Fuente -- Online:[www.lavanguardia.com/files/image_948_465/uploads/2018/06/29/5fa43d002c905.jpeg]")
st.title("TITANIC DATA")
st.text("Aquí vamos a mostrar como limpiar los datos, luego haremos un pequeño análisis")
st.text("y las conclusiones del mismo")
# ---------------------SIDEBAR------------------------------
st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.image("http://c.files.bbci.co.uk/16D1/production/_100814850_gettyimages-877330410.jpg", width=150)
st.sidebar.title("Menu")
st.sidebar.write("----")

if st.sidebar.button("DataFrame INICIAL"):
    st.dataframe(df2)

if st.sidebar.button("Limpieza de datos"):
    st.header("Limpieza")
    st.text("Comenzamos viendo como están distribuidos los valores nulos")
    code="df.isnull().sum()"
    st.code(code,language="python")
    st.write(df2.isnull().sum())
    st.text("Vemos que porcentaje de nulos tiene cada columna")
    code= "df.isnull().sum() * 100 / len(df)"
    st.code(code,language="python")
    df2.isnull().sum() * 100 / len(df)
    st.text("Se decide eliminar la columna Cabin por tener un alto porcentaje de valores nulos")
    st.code("df.drop(['Cabin'],axis=1,inplace=True)")
    st.text("Empezamos a reparar la columna Age, para ello vemos el tipo de columna que es")
    st.code("df['Age'].info()")
    st.text("Se chequea la información con la función .describe teniendo en cuenta que es un float")
    st.code("df[df['Age'].notnull()]['Age'].describe()")
    st.write(df2[df2["Age"].notnull()]["Age"].describe())
    st.text("Como la media es un valor con decimales, elijo la mediana como valor para reemplazar los nulos")
    st.code("df['Age'].fillna(df['Age'].median(),inplace=True)")
    st.text("Luego pasamos a la columna Embarked y vemos sus valores")
    st.code("df['Embarked'].value_counts()")
    st.write(df2["Embarked"].value_counts())
    st.text("Vemos que el valor más común es la S, por ende, rellenamos los nulos con este valor")
    st.code("df['Embarked'].fillna(value='S', inplace=True)")
    st.text("Comprobamos lo hecho")
    st.code("df.isnull().sum()")
    st.write(df.isnull().sum())
    st.subheader("Hago nuevos rangos en base a las edades para un mejor análisis")
    st.text("(niños (0-10) - adolescentes (11-18)- jóvenes (19-28) - adultos (29-59) - ancianos (+60))")
    st.code("""
    edad_cond = [df["Age"]<= 10,
            (df["Age"]> 10) & (df["Age"]<= 18),
            (df["Age"]> 18) & (df["Age"]<= 28),
            (df["Age"]> 28) & (df["Age"]<= 59),
            df["Age"]> 59]

    nuevos_nombres = ["Kids", "Teenagers", "Young People", "Adults", "Seniors"]""")
    st.text("Añado la nueva columna")
    st.code("""df["Age_description"] = np.select(edad_cond,nuevos_nombres)""")
    st.text("Así queda la nueva columna")
    st.write(df.head(5))
    st.text("Aquí termina la limpieza de los datos y pasamos al análisis de los mismos")

if st.sidebar.button("DataFrame Final"):
    st.dataframe(df)
# --------------------------------------------------------GENERAL----------------------------------------------------------
if st.sidebar.button("General"):
    st.header("Análisis General")
    # age_max = df['Age'].max()
    # Age_min = df['Age'].min()
    # st.write("La edad maxima es " + str(age_max))
    # st.write("La edad minima es " + str(Age_min))
    st.markdown("- El número de pasajeros embarcados fue 891")
    st.markdown("- La distribución en base al rango de edades fue:")
    st.write(df["Age_description"].value_counts())
    st.markdown("- Mediana de precios por clase:")
    st.markdown("Clase 1-     60.29")
    st.markdown("Clase 2-     14.25")
    st.markdown("Clase 3-      8.05")
    st.markdown(" - El promedio de precio pagado por las mujeres fue de 23 y de 10.5 para los hombres")
    st.markdown("- El 64.76 % eran hombres, y el 35.24 % eran mujeres y en el siguiente grafico lo podemos ver:")

    sns.set_style('ticks')
    sns.countplot(x='Age_description', hue= "Sex",data=df, palette='bright').set(title= "Cantidad de personas según su rango etario y sexo")    
    sns.despine()
    st.pyplot()
    st.text("En este grafico podemos ver que, salvo en los niños y adolescentes,")
    st.text("confirmamos que hubo más hombres que mujeres en el Titanic")
    st.markdown("---")

# --------------------------------------------------------Supervivientes-------------------------------------------------
if st.sidebar.button("Supervivientes"):

    st.subheader("Gráficos relacionados a la cantidad de supervivientes")
    super = df.groupby("Pclass")["Survived"].value_counts().unstack()
    super = super.rename(columns={0:"Muertos", 1:"Vivos"})
    graf = px.bar(super, title="Cantidad de supervivientes por clase", template = 'plotly_dark', color_discrete_sequence = ['#FF6347', '#A9A9A9'],
            height=500, labels={'index':'Clase', 'value':'cantidad', 'survived':"Supervivientes"} )
    st.plotly_chart(graf)
    st.text("En este grafico se puede ver como la mayoría de los supervivientes fueron de primera")
    st.text("clase, aunque era una de las clases con menos tripulante")
    st.markdown("---")
    # fig1 = px.bar(df, x= "Pclass", y="Survived" , color="Sex", barmode="group", title="Cantidad de supervivientes en base al sexo y la clase",
    #             labels={"Pclass": "Clase de pasajero", "Survived": "Cantidad de supervivientes"})
    # st.plotly_chart(fig1)
    fig1 = px.histogram(df, x= "Pclass", y="Survived" , color="Sex", barmode="group", title="Supervivencia en base al sexo y la clase",text_auto=True,
                labels={"Pclass": "Clase de pasajero", "Survived": "Cantidad de supervivientes"})
    st.plotly_chart(fig1)
    st.text("La mayoría de supervivientes fueron mujeres, sin importar la clase")
    st.markdown("---")
    fig3= px.histogram(df, x= "Age_description", y="Survived", color="Sex" , barmode="group", text_auto=True, 
                    title= "Cantidad de personas por edad y sexo que sobrevivieron",
                    labels={"Age_description": "Rango de edad del pasajero", "Survived": "Cantidad de Supervivientes"})
    fig3.update_traces(textposition="outside",cliponaxis=False)
    st.plotly_chart(fig3)  
    st.text("Aquí podemos ver como solo los niños y ancianos sobrevivieron en la misma medida,")
    st.text("en cambio en el resto de los casos las mujeres sobrevivieron más")
    
    st.markdown("---")

# ---------------------------------------------------------TARIFA---------------------------------------------------------  
if st.sidebar.button("Tarifa"):

    st.subheader("Gráficos relacionados a la tarifa")

    # st.code(df.groupby("Pclass")["Fare"].median())
    sns.boxplot(x="Pclass",y="Age", hue= "Sex",data= df,palette='Set1').set(title= "Distribución de las edades en base a la clase")
    st.pyplot()
    st.text("Las tarifas más caras eran adquiridas por personas de mayor edad")
    st.markdown("---")
    fare_max = round(df["Fare"].max(),2)
    fare_min = df["Fare"].min()

    fig = px.treemap(df, path=[px.Constant("All"), 'Age_description', 'Sex'], values="Fare", title="Total pagado en base al rango de edad y sexo")
    st.plotly_chart(fig)
    st.text("Aquí podemos ver que los que más pagaron fueron los adultos y los jóvenes")
    st.text("Si bien las mujeres eran menos, pagaron el mismo monto que los hombres")
    st.markdown("---")
    sns.catplot(x = "Pclass", y = "Fare",hue="Sex", data = df, jitter= 0.2).set(title= "Distribución de los precios pagados en base a la clase y el sexo")
    st.pyplot()
    st.text("Aquí vemos que la clase 1 fue la que pago los precios más elevados")
    st.text("También podemos ver como hubo personas de clase 1 que no pagaron nada por ingresar")
    st.text("""al Titanic, algo muy curioso, los "influencers" de la época""")
    st.markdown("---")
# -------------------------------------------------------EMBARQUE--------------------------------------------------------
if st.sidebar.button("Embarque"):

    st.subheader("Gráficos relacionados al embarque")

    fig6 = px.histogram(df, y="Embarked", color="Pclass" , barmode="group", text_auto=True, 
                    title= "Suma de personas en base al lugar que embarcaron y su clase",
                    labels={"count": "Cantidad de personas", "Embarked": "Lugar donde embarco"})
    fig6.update_traces(textposition="outside",cliponaxis=False)
    st.plotly_chart(fig6)
    st.text("S= Southampton / C= Cherbourg / Q= Queenstown")
    st.text("Aquí se puede ver que la gran mayoría se ha embarcado en Southampton")
    st.markdown("---")
    j= df.groupby("Embarked")["Survived"].value_counts().unstack()
    j = j.rename(columns={0:"Muertos", 1:"Vivos"})
    fig7 = px.bar(j , pattern_shape="Survived",title="Cantidad de supervivientes en base al lugar de embarque", template = 'plotly_dark', color_discrete_sequence = ['#FF6347', '#A9A9A9'],
             pattern_shape_sequence=["x", "+"] ,labels={'value':'cantidad', 'survived':"Supervivientes"})
    st.plotly_chart(fig7)
    st.text("La mayoría de los muertos han sido de Southampton")

# --------------------------------------------------------Conclusiones---------------------------------------------------
if st.sidebar.button("Conclusiones Generales"):
    st.header("Conclusiones")
    st.text("Según los datos proporcionados podemos decir que: ")
    st.subheader("Datos de embarque")
    st.markdown("- El 81 % de las personas embarcadas eran jóvenes (19-28) y adultos (29-59)")
    st.markdown("- El 55 % eran de la tercera clase")
    st.markdown("- El 72 % ha embarcado en Southampton")
    st.markdown("- El 93 % de los embarcados en Queenstown eran de la tercera clase")

    st.subheader("Datos de supervivencia")
    st.markdown("- Murieron el 62 % de las personas que embarcaron")
    st.markdown("- Del total de sobrevivientes el 40 % eran de la primera clase")
    st.markdown("- Del total de muertos, el 68 % eran de la tercera clase")
    st.markdown("- El 63 % de las personas de primera clase sobrevivieron")
    st.markdown("- El 76 % de las personas de tercera clase murieron")
    st.markdown("- El 72 % de las mujeres sobrevivieron")
    st.markdown("- Del total de sobrevivientes el 78 % eran jóvenes (19-28) y adultos (29-59)")
    st.markdown("- Solo el 32 % de los sobrevivientes fueron hombres")
    st.markdown("- El 92 % y el 97 % de las mujeres de segunda y tercera clase respectivamente sobrevivieron")

    st.subheader("Datos Económicos")
    st.markdown("- Si bien las mujeres eran el 35 % de los tripulantes, en proporción pagaron casi el 49 % del total de los billetes")
    st.markdown("- El 63 % del monto total abonado fue pagado por la primera clase")
