import pandas as pd
import datetime as datetime

def get_age_years(x):
    age = datetime.datetime.today() - x
    age_years = age.days / 365
    return age_years


def get_valor_geo_ref(df, VALOR_N):
	GEO_REF_DF = df.groupby("GEO_REFERENCIA")[["VALOR_01","VALOR_02","VALOR_03","VALOR_04"]].mean()
	VALOR_N_DF=GEO_REF_DF.sort_values(by=VALOR_N, ascending=False)[VALOR_N].reset_index(drop=False).reset_index(drop=False)
	VALOR_N_DF.rename(index=str, columns={"index": "{v}_GEO_REF".format(v=VALOR_N), VALOR_N: VALOR_N}, inplace=True)
	VALOR_N_DF = VALOR_N_DF[["{v}_GEO_REF".format(v=VALOR_N),"GEO_REFERENCIA"]]
	return VALOR_N_DF


def get_quantile(df, x, VAR_N):
    q25 = df[VAR_N].quantile(q=0.25)
    q50 = df[VAR_N].quantile(q=0.50)
    q75 = df[VAR_N].quantile(q=0.75)
    
    if ( x < q25 ):
        return 4
    elif ( x >= q25 ) & ( x < q50 ):
        return 3
    elif ( x >= q50 ) & ( x < q75 ):
        return 2
    elif ( x >= q75 ):
        return 1


def clean_data(df):
    """ Clean dataframe """
    df["IDADE"] = df["DATA_NASCIMENTO"].apply(lambda x : get_age_years(x))
    df["PROFISSAO_GERAL"] = df["PROFISSAO"].apply(lambda x : x.split(" ")[0])
    df["ESTADO_CIVIL_GERAL"] = df["ESTADO_CIVIL"].apply(lambda x : x.split(" ")[0])
    
    df = df.merge(get_valor_geo_ref(df, VALOR_N="VALOR_01"),left_on="GEO_REFERENCIA",right_on="GEO_REFERENCIA",how="left")
    df = df.merge(get_valor_geo_ref(df, VALOR_N="VALOR_02"),left_on="GEO_REFERENCIA",right_on="GEO_REFERENCIA",how="left")
    df = df.merge(get_valor_geo_ref(df, VALOR_N="VALOR_03"),left_on="GEO_REFERENCIA",right_on="GEO_REFERENCIA",how="left")
    df = df.merge(get_valor_geo_ref(df, VALOR_N="VALOR_04"),left_on="GEO_REFERENCIA",right_on="GEO_REFERENCIA",how="left")
    
    df["VALOR_01_GEO_REF"] = df["VALOR_01_GEO_REF"].apply(lambda x : get_quantile(df, x, "VALOR_01_GEO_REF"))
    df["VALOR_02_GEO_REF"] = df["VALOR_02_GEO_REF"].apply(lambda x : get_quantile(df, x, "VALOR_02_GEO_REF"))
    df["VALOR_03_GEO_REF"] = df["VALOR_03_GEO_REF"].apply(lambda x : get_quantile(df, x, "VALOR_03_GEO_REF"))
    df["VALOR_04_GEO_REF"] = df["VALOR_04_GEO_REF"].apply(lambda x : get_quantile(df, x, "VALOR_04_GEO_REF"))


    # Remove cases where age and profession info do not match 
    df = df.drop(df[(df.IDADE<10) & (df.PROFISSAO!="ESTUDANTE")].index)
    
    return df

