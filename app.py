import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
st.sidebar.image("https://toppng.com/uploads/preview/olympic-rings-logo-png-transparent-images-11660730428ymzixzlmet.png")
st.sidebar.title('Olympics Analysis (from 1896-2016)')
updated_df = preprocessor.preprocess(df, region_df)
user_menu=st.sidebar.radio(
    "Choose your option",
    ['Medals Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis']
)



if user_menu =='Medals Tally':
    years,countries= helper.select_countries_year(updated_df)
    st.sidebar.header('Medals Tally')
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Medal Tally of each country (1896-2016)")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally of each country in year " + str(selected_year))
    if selected_year == "Overall" and selected_country != "Overall":
        st.title("Medal Tally of " + selected_country + "(1896-2016)" )
    if selected_year != "Overall" and selected_country != "Overall":
        st.title("Medal Tally of " + selected_country + " in " + str(selected_year) + "Olympics")
    medal_tally = helper.fetch_year_country(updated_df, selected_year, selected_country)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = updated_df['Year'].unique().shape[0] -1
    cities = updated_df['City'].unique().shape[0]
    sports = updated_df['Sport'].unique().shape[0]
    events = updated_df['Event'].unique().shape[0]
    athlete = updated_df['Name'].unique().shape[0]
    nations = updated_df['region'].unique().shape[0]

    st.title("Overall Analysis")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athlete)
    with col3:
        st.header("Countries")
        st.title(nations)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    #Year vs Countries
    countries_over_time = helper.get_year_event_chart(updated_df,'region')
    fig = px.line(countries_over_time, x="Editions", y='region')
    st.title("Countries participation over time")
    st.plotly_chart(fig)

    # Year vs Countries
    events_over_time = helper.get_year_event_chart(updated_df, 'Event')
    fig = px.line(events_over_time, x="Editions", y='Event')
    st.title("No. of Events across Olympics Editions")
    st.plotly_chart(fig)

    # Year vs Countries
    athletes_over_time = helper.get_year_event_chart(updated_df, 'Name')
    fig = px.line(athletes_over_time, x="Editions", y='Name')
    st.title("Athlete participation over time")
    st.plotly_chart(fig)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.title("Number of Events per Sport Across Olympic Years (Heatmap)")
    #Heatmap-No.of events per country per year
    pivot_tab_data = helper.gen_heatmap(df)
    fig,ax = plt.subplots(figsize=(25,25))
    sns.heatmap(
        pivot_tab_data,
        annot=True,
        fmt="d",
        ax=ax
    )
    st.pyplot(fig)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    athletes_with_most_medals, country = helper.get_highest_medals(df)
    st.title('Top Medal Winners – Summer Olympics')
    selected_region = st.selectbox('Select Country',country)
    if selected_region == 'Overall':
        st.dataframe(athletes_with_most_medals.head(20))
    else:
        athletes_with_most_medals=athletes_with_most_medals[athletes_with_most_medals['region'] == str(selected_region)].reset_index()
        athletes_with_most_medals.drop('index',axis=1, inplace=True)
        athletes_with_most_medals.index = athletes_with_most_medals.index + 1
        st.dataframe(athletes_with_most_medals)

if user_menu == 'Country-wise Analysis':
    st.title('Country-wise Analysis')
    st.write("")
    st.write("")
    st.header("Country-wise Performance Trend w.r.t Medals across Olympics")
    regions = helper.get_country_names(df)
    sel_reg=st.selectbox('Select Country', regions)
    if sel_reg == 'Overall':
        st.subheader('Top 5 countries with highest medal count')
        df1 = helper.countries_medal_chart(df, 'USA')
        df2 = helper.countries_medal_chart(df, 'Russia')
        df3 = helper.countries_medal_chart(df, 'Germany')
        df4 = helper.countries_medal_chart(df, 'UK')
        df5 = helper.countries_medal_chart(df, 'France')
        final_df=pd.concat([df1,df2,df3,df4,df5])
        fig = px.line(final_df,x='Editions',y='Total Medals', color='Country')
        st.plotly_chart(fig)
    else:
        st.subheader(str(sel_reg))
        final_df = helper.countries_medal_chart(df,sel_reg)
        fig = px.line(final_df, x='Editions', y='Total Medals', color='Country')
        st.plotly_chart(fig)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.header("Country-wise Medals in Sports across Olympics (Heatmap)")
    reg_names=regions.copy()
    reg_names.remove('Overall')
    reg_names.insert(0, 'None')
    sel_country=st.selectbox('Select a country',reg_names)
    if sel_country == 'None':
        st.subheader('Select a country from the above dialogue box to generate its heatmap')
    else:
        country_medal_pivot_tab = helper.get_countrywise_medal_heatmap(df, sel_country)
        if country_medal_pivot_tab.empty:
            st.write('No medals achieved up till 2016')

        else:
            fig, ax = plt.subplots(figsize=(25, 25))
            sns.heatmap(
                country_medal_pivot_tab,
                annot=True,
                fmt='d',
                ax=ax
            )
            st.pyplot(fig)
    st.write("")
    st.write("")

    st.header('Top 10 Athletes country-wise across Olympics (till 2016)')
    select_reg = st.selectbox('Countries', regions)
    if select_reg == 'Overall':
        dataframe1 = helper.get_top_10_athlete_countrywise(df,select_reg)
        st.table(dataframe1)
    else:
        dataframe1 = helper.get_top_10_athlete_countrywise(df,select_reg)
        st.table(dataframe1)

if user_menu == 'Athlete-wise Analysis':
    st.title('Athlete-wise Analysis')
    st.write("")
    st.write("")
    st.header('Athlete Age Distribution across Olympics')
    x1,x2,x3,x4=helper.get_age_distribution(df)
    fig = ff.create_distplot([x1.dropna(), x2['Age'].dropna(), x3['Age'].dropna(), x4['Age'].dropna()],
                             ['Overall', 'Gold', 'Silver', 'Bronze'], show_hist=False)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        xaxis_title='Age',
        yaxis_title='Density'
    )
    st.plotly_chart(fig)
    st.write("")
    st.write("")
    st.header('Athlete Age Distribution for each Sport across Olympics')
    x,name=helper.get_age_wrt_sports(df)
    fig = ff.create_distplot(x, name, show_hist=False)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        xaxis_title='Age',
        yaxis_title='Density'
    )
    st.plotly_chart(fig)
    st.write("")
    st.write("")
    st.header("Athlete's Height-Weight Scatterplot for each Sport")
    sports=helper.get_sport_names(df)
    selected_sport=st.selectbox('Select Sport',sports)
    h_w_df = helper.get_h_w_scatter(df,selected_sport)
    fig,bx=plt.subplots()
    bx=sns.scatterplot(x=h_w_df['Weight'], y=h_w_df['Height'], hue=h_w_df['Medal'],
                           style=h_w_df['Sex'],s=60)
    st.pyplot(fig)
    st.write("")
    st.write("")
    st.header("Men and Women Athlete Participation across Olympics Editions")
    sex_df=helper.get_m_w_part_years(df)
    fig = px.line(sex_df, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)



















