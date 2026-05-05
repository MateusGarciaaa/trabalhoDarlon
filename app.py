import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Multi-Bases", layout="wide")

st.title("Aplicação de Análise de Dados")

# =============================
# Função para normalizar colunas
# =============================
def normalize_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

# =============================
# Carregar dados
# =============================
@st.cache_data
def load_data():
    spacex = pd.read_csv("data/spacex_sample.csv")
    games = pd.read_csv("data/videogames_sample.csv")
    cars = pd.read_csv("data/carros.csv")

    # Normalizar colunas
    spacex = normalize_columns(spacex)
    games = normalize_columns(games)
    cars = normalize_columns(cars)

    return spacex, games, cars

spacex, games, cars = load_data()

# =============================
# Menu lateral
# =============================
option = st.sidebar.selectbox(
    "Escolha a base:",
    ["SpaceX Launches", "Video Games Sales", "Carros"]
)

# =============================
# SPACE X
# =============================
if option == "SpaceX Launches":
    st.header("SpaceX Launch Data")

    df = spacex.copy()


    # Detectar possíveis colunas
    rocket_col = next((col for col in df.columns if "rocket" in col or "booster" in col), None)
    success_col = next((col for col in df.columns if "success" in col or "outcome" in col), None)

    # Filtro sucesso
    if success_col:
        success_filter = st.selectbox(
            "Sucesso da missão:",
            ["Todos"] + list(df[success_col].dropna().unique())
        )

        if success_filter != "Todos":
            df = df[df[success_col] == success_filter]

    # Filtro foguete
    if rocket_col:
        rocket_filter = st.multiselect(
            "Foguete:",
            df[rocket_col].dropna().unique()
        )

        if rocket_filter:
            df = df[df[rocket_col].isin(rocket_filter)]

    st.dataframe(df)
    st.write("Total de registros:", len(df))


# =============================
# VIDEO GAMES
# =============================
elif option == "Video Games Sales":
    st.header("Video Game Sales")

    df = games.copy()


    # Detectar colunas automaticamente
    name_col = next((c for c in df.columns if "name" in c), None)
    genre_col = next((c for c in df.columns if "genre" in c), None)
    platform_col = next((c for c in df.columns if "platform" in c), None)

    # Gênero
    if genre_col:
        genre_filter = st.multiselect(
            "Gênero:",
            df[genre_col].dropna().unique()
        )
        if genre_filter:
            df = df[df[genre_col].isin(genre_filter)]

    # Plataforma
    if platform_col:
        platform_filter = st.multiselect(
            "Plataforma:",
            df[platform_col].dropna().unique()
        )
        if platform_filter:
            df = df[df[platform_col].isin(platform_filter)]

    # Busca por nome
    if name_col:
        search_name = st.text_input("Buscar jogo:")
        if search_name:
            df = df[df[name_col].str.contains(search_name, case=False, na=False)]

    st.dataframe(df)
    st.write("Total de registros:", len(df))


# =============================
# CARROS
# =============================
elif option == "Carros":
    st.header("Carros - Preço")

    df = cars.copy()


    # Detectar colunas automaticamente
    brand_col = next((c for c in df.columns if "brand" in c or "make" in c), None)
    model_col = next((c for c in df.columns if "model" in c), None)
    year_col = next((c for c in df.columns if "year" in c), None)
    fuel_col = next((c for c in df.columns if "fuel" in c), None)
    trans_col = next((c for c in df.columns if "trans" in c), None)
    price_col = next((c for c in df.columns if "price" in c), None)
    mileage_col = next((c for c in df.columns if "mile" in c or "km" in c), None)

    # Marca
    if brand_col:
        brand_filter = st.multiselect("Marca:", df[brand_col].dropna().unique())
        if brand_filter:
            df = df[df[brand_col].isin(brand_filter)]

    # Modelo (busca)
    if model_col:
        search_model = st.text_input("Buscar modelo:")
        if search_model:
            df = df[df[model_col].str.contains(search_model, case=False, na=False)]

    # Ano
    if year_col:
        year_range = st.slider(
            "Ano:",
            int(df[year_col].min()),
            int(df[year_col].max()),
            (int(df[year_col].min()), int(df[year_col].max()))
        )
        df = df[(df[year_col] >= year_range[0]) & (df[year_col] <= year_range[1])]

    # Combustível
    if fuel_col:
        fuel_filter = st.multiselect("Combustível:", df[fuel_col].dropna().unique())
        if fuel_filter:
            df = df[df[fuel_col].isin(fuel_filter)]

    # Transmissão
    if trans_col:
        trans_filter = st.multiselect("Transmissão:", df[trans_col].dropna().unique())
        if trans_filter:
            df = df[df[trans_col].isin(trans_filter)]

    # Quilometragem
    if mileage_col:
        km_range = st.slider(
            "Quilometragem:",
            int(df[mileage_col].min()),
            int(df[mileage_col].max()),
            (int(df[mileage_col].min()), int(df[mileage_col].max()))
        )
        df = df[(df[mileage_col] >= km_range[0]) & (df[mileage_col] <= km_range[1])]

    # Preço
    if price_col:
        price_range = st.slider(
            "Preço:",
            int(df[price_col].min()),
            int(df[price_col].max()),
            (int(df[price_col].min()), int(df[price_col].max()))
        )
        df = df[(df[price_col] >= price_range[0]) & (df[price_col] <= price_range[1])]

        st.metric("Preço médio", f"${int(df[price_col].mean())}")

    # Gráfico
    if brand_col:
        st.subheader("Distribuição por marca")
        st.bar_chart(df[brand_col].value_counts())

    st.dataframe(df)
    st.write("Total de registros:", len(df))
