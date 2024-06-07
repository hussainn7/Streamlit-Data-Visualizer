import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title='Hussain Data Visualizer', layout='wide')

st.title('Hussain Data Visualizer')

uploaded_file = st.file_uploader("Upload a CSV, Excel, TXT, JSON, or Parquet file",
                                 type=['csv', 'xlsx', 'txt', 'json', 'parquet'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file, delimiter='\t')
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith('.parquet'):
            df = pd.read_parquet(uploaded_file)
        else:
            st.error("Unsupported file type!")

        st.write("## DataFrame")
        st.dataframe(df)

        st.write("## Descriptive Statistics")
        st.write(df.describe())

        st.sidebar.header('Plot Settings')
        plot_type = st.sidebar.selectbox('Select plot type',
                                         ['line', 'bar', 'scatter', 'heatmap', 'pairplot', 'distplot', 'histogram'])
        x_column = st.sidebar.selectbox('Select X-axis column', df.columns)
        y_column = st.sidebar.selectbox('Select Y-axis column', df.columns)

        st.write(f"## {plot_type.capitalize()} Plot")
        if plot_type == 'line':
            fig, ax = plt.subplots()
            sns.lineplot(data=df, x=x_column, y=y_column, ax=ax)
            st.pyplot(fig)
        elif plot_type == 'bar':
            fig, ax = plt.subplots()
            sns.barplot(data=df, x=x_column, y=y_column, ax=ax)
            st.pyplot(fig)
        elif plot_type == 'scatter':
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x_column, y=y_column, ax=ax)
            st.pyplot(fig)
        elif plot_type == 'heatmap':
            if df.select_dtypes(include=['number']).shape[1] > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
                st.pyplot(fig)
            else:
                st.error("Heatmap requires at least two numerical columns")
        elif plot_type == 'pairplot':
            fig = sns.pairplot(df)
            st.pyplot(fig)
        elif plot_type == 'distplot':
            fig, ax = plt.subplots()
            sns.histplot(df[x_column], kde=True, ax=ax)
            st.pyplot(fig)
        elif plot_type == 'histogram':
            fig, ax = plt.subplots()
            ax.hist(df[x_column].dropna(), bins=30)
            ax.set_xlabel(x_column)
            ax.set_ylabel('Frequency')
            st.image(fig, use_column_width=True)

        st.sidebar.header('Additional Plotting Options')
        if plot_type in ['line', 'bar', 'scatter']:
            hue_column = st.sidebar.selectbox('Select hue column (optional)', [None] + list(df.columns))
            if hue_column:
                fig, ax = plt.subplots()
                if plot_type == 'line':
                    sns.lineplot(data=df, x=x_column, y=y_column, hue=hue_column, ax=ax)
                elif plot_type == 'bar':
                    sns.barplot(data=df, x=x_column, y=y_column, hue=hue_column, ax=ax)
                elif plot_type == 'scatter':
                    sns.scatterplot(data=df, x=x_column, y=y_column, hue=hue_column, ax=ax)
                st.pyplot(fig)

        if st.button('Show DataFrame Info'):
            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)

        if st.button('Show DataFrame Description'):
            st.write(df.describe())

        st.write("## DataFrame Manipulations")

        # Change column names
        st.write("### Change Column Names")
        col1, col2 = st.columns(2)
        with col1:
            old_column = st.selectbox('Select column to rename', df.columns)
        with col2:
            new_column = st.text_input('New column name')

        if st.button('Rename Column'):
            if new_column:
                df.rename(columns={old_column: new_column}, inplace=True)
                st.success(f'Column renamed from {old_column} to {new_column}')
                st.write("Updated DataFrame:")
                st.dataframe(df)
            else:
                st.error('Please enter a new column name')

        if st.button('Check for Null Values'):
            st.write(df.isnull().sum())

        if st.button('Remove Duplicate Rows'):
            df.drop_duplicates(inplace=True)
            st.success('Duplicate rows removed')
            st.write("Updated DataFrame:")
            st.dataframe(df)

        st.write("### Replace Null Values")
        replace_value = st.text_input('Value to replace null values with')
        if st.button('Replace Null Values'):
            df.fillna(replace_value, inplace=True)
            st.success('Null values replaced')
            st.write("Updated DataFrame:")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error loading file: {e}")

else:
    st.info('No file uploaded yet, please upload one.')

