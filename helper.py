import pandas as pd
region_df = pd.read_csv('noc_regions.csv')

def medal_tally_fn(df):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False, ).reset_index()
    medal_tally['Total Medals'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally


def fetch_year_country(df, year, country):
    flag = 0
    dropped_df = df.drop_duplicates(subset=['NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if year == 'Overall' and country == 'Overall':
        temp_df = dropped_df
    if year != 'Overall' and country == 'Overall':
        temp_df = dropped_df[dropped_df['Year'] == year]
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = dropped_df[dropped_df['region'] == country]
    if year != 'Overall' and country != 'Overall':
        temp_df = dropped_df[(dropped_df['region'] == country) & (dropped_df['Year'] == year)]
    if flag == 1:
        medal_tally_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True)
        medal_tally_df['Total Medals'] = medal_tally_df['Gold'] + medal_tally_df['Silver'] + medal_tally_df['Bronze']
    else:
        medal_tally_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
        medal_tally_df['Total Medals'] = medal_tally_df['Gold'] + medal_tally_df['Silver'] + medal_tally_df['Bronze']
    return medal_tally_df


def select_countries_year(df):
    #Countries
    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0,'Overall')
    #Year
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    return years,countries


def get_year_event_chart(df, col):
    df.drop_duplicates(subset=['Year', col], inplace=True)
    year_no_of_col_df = df['Year'].value_counts().sort_values(ascending=True).reset_index()
    year_no_of_col_df.rename(
        columns={
            'Year': 'Editions',
            'count': col
        }, inplace=True
    )
    year_no_of_col_df.sort_values('Editions', inplace=True)
    return year_no_of_col_df

def gen_heatmap(df):
    df = df[df['Season'] == 'Summer']
    df = pd.merge(df, region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset=['Year', 'Event','Sport'], inplace=True)
    pivot_df = df.pivot_table(
        values='Event',
        index='Sport',
        columns='Year',
        aggfunc='count'
    )
    pivot_df.fillna(0, inplace=True)
    pivot_df = pivot_df.astype('int')
    return pivot_df

def get_highest_medals(df):
    df = pd.merge(df, region_df, on='NOC', how='left')
    b_df = df.dropna(subset=['region'])
    countries = b_df['region'].unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')
    df = df[(df['Season'] == 'Summer') & (df['Medal'].notna())]
    final_df = df.groupby(['Name', 'region'])['Medal'].count().reset_index()
    final_df.rename(columns={'Medal': 'count'}, inplace=True)
    final_df = final_df.sort_values(by='count', ascending=False)
    final_df.reset_index(drop=True, inplace=True)
    final_df.index = final_df.index + 1
    return final_df, countries

def get_country_names(df):
    df = pd.merge(df, region_df, on='NOC', how='left')
    b_df = df.dropna(subset=['region'])
    countries = b_df['region'].unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')
    return countries

def get_sport_names(df):
    df = pd.merge(df, region_df, on='NOC', how='left')
    b_df = df.dropna(subset=['Sport'])
    sports = b_df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0, 'Overall')
    return sports

def countries_medal_chart(df, country):
    overall_df = df[df['Season']=='Summer']
    overall_df=pd.merge(overall_df,region_df, on='NOC', how='left')
    overall_df.drop_duplicates(inplace=True)
    df1=overall_df.copy()
    df1.dropna(subset=['Medal'], inplace=True)
    year_country_df=df1[df1['region']==country]
    year_country_df=year_country_df.drop_duplicates(subset=['Year','Event','Medal'])
    df2=year_country_df['Year'].value_counts()
    df2=df2.reset_index().sort_values('Year')
    df2.rename(columns={
    'Year':'Editions',
    'count':'Total Medals'
            }, inplace=True)
    df2['Country']=country
    return df2


def get_countrywise_medal_heatmap(df, country):
    df = df[df['Season'] == 'Summer']
    overall_df = pd.merge(df, region_df, on='NOC', how='left')
    overall_df = overall_df.dropna(subset=['Medal'])
    overall_df.drop_duplicates(inplace=True)
    a_df = overall_df[['Year', 'Sport', 'region', 'Event']]
    country_a_df = a_df[a_df['region'] == country]
    country_a_df = country_a_df.drop_duplicates(subset=['Year', 'Event'])
    sample_pivot_table = pd.pivot_table(country_a_df, values='Event', index='Sport', columns='Year', aggfunc='count')
    sample_pivot_table = sample_pivot_table.fillna(0)
    sample_pivot_table = sample_pivot_table.astype('int')
    return sample_pivot_table


def get_top_10_athlete_countrywise(df, country):
    if country == 'Overall':
        df = df[df['Season'] == 'Summer']
        overall_df = pd.merge(df, region_df, on='NOC', how='left')
        overall_df = overall_df.dropna(subset=['Medal'])
        overall_df.drop_duplicates(inplace=True)
        temp_df = overall_df[['Name', 'Event', 'Sport', 'Medal', 'region']]
        temp_df = pd.get_dummies(temp_df, columns=['Medal'], dtype='int')
        temp1_df = temp_df.groupby('Name').sum()[['Medal_Bronze', 'Medal_Gold', 'Medal_Silver']]
        temp1_df = temp1_df.reset_index()
        athlete_country = overall_df[['Name', 'region', 'Sport']]
        d_df = pd.merge(temp1_df, athlete_country, on='Name', how='left')
        d_df = d_df[['Name', 'region', 'Sport', 'Medal_Gold', 'Medal_Silver', 'Medal_Bronze']]
        d_df.rename(columns={
            'region': 'Country',
            'Medal_Gold': 'Gold',
            'Medal_Silver': 'Silver',
            'Medal_Bronze': 'Bronze'
        }, inplace=True)
        d_df['Total Medals'] = d_df['Gold'] + d_df['Silver'] + d_df['Bronze']
        e_df = d_df.sort_values('Total Medals', ascending=False)
        e_df.drop_duplicates(inplace=True)
        f_df = e_df.head(10)
        f_df = f_df.reset_index()
        f_df.drop(columns='index', axis=1, inplace=True)
        f_df.index = f_df.index + 1
        return f_df

    else:
        df = df[df['Season'] == 'Summer']
        overall_df = pd.merge(df, region_df, on='NOC', how='left')
        overall_df = overall_df.dropna(subset=['Medal'])
        overall_df.drop_duplicates(inplace=True)
        temp_df = overall_df[['Name', 'Event', 'Sport', 'Medal', 'region']]
        temp_df = pd.get_dummies(temp_df, columns=['Medal'], dtype='int')
        temp1_df = temp_df.groupby('Name').sum()[['Medal_Bronze', 'Medal_Gold', 'Medal_Silver']]
        temp1_df = temp1_df.reset_index()
        athlete_country = overall_df[['Name', 'region', 'Sport']]
        d_df = pd.merge(temp1_df, athlete_country, on='Name', how='left')
        d_df = d_df[['Name', 'region', 'Sport', 'Medal_Gold', 'Medal_Silver', 'Medal_Bronze']]
        d_df.rename(columns={
            'region': 'Country',
            'Medal_Gold': 'Gold',
            'Medal_Silver': 'Silver',
            'Medal_Bronze': 'Bronze'
        }, inplace=True)
        d_df['Total Medals'] = d_df['Gold'] + d_df['Silver'] + d_df['Bronze']
        e_df = d_df[d_df['Country'] == country].sort_values('Total Medals', ascending=False)
        e_df.drop_duplicates(inplace=True)
        f_df = e_df.head(10)
        f_df=f_df.reset_index()
        f_df.drop(columns='index',axis=1,inplace=True)
        f_df.index=f_df.index+1
        return f_df

def get_age_distribution(df):
    df = df[df['Season'] == 'Summer']
    df = pd.merge(df, region_df, on='NOC', how='left')
    df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df = df.copy()
    x1 = athlete_df['Age']
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']
    return x1,x2,x3,x4

def get_age_wrt_sports(df):
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug of war', 'Athletics', 'Swimming', 'Badminton', "Sailing",
                     "Gymnastics", 'Weightlifting', 'wrestling',
                     "Art Competitions", "Handball", "Weightlifting",
                     "water Polo", 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'cycling',
                     'Diving', "Canoeing",
                     "Tennis", 'Golf', 'Softball', "Archery",
                     "Volleyball", 'Synchronized Swimming', 'Table Tennis', "Baseball", 'hythmic Gymnastics',
                     "Rugby Sevens",
                     "Beach Volleyball", "Triathlon", "Rugby", "Polo", "Ice Hockey"]
    df = df[df['Season'] == 'Summer']
    df = pd.merge(df, region_df, on='NOC', how='left')
    df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df = df.copy()
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        ages = temp_df[temp_df['Medal'] == 'Gold']["Age"].dropna()
        if len(ages) > 0:  # This line filters out empty groups
            x.append(ages)
            name.append(sport)
    return x,name


def get_h_w_scatter(df,sport):
    df = df[df['Season'] == 'Summer']
    df = pd.merge(df, region_df, on='NOC', how='left')
    df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df = df.copy()
    if sport == 'Overall':
        athlete_df['Medal'].fillna('No Medal', inplace=True)
        return athlete_df
    else:
        athlete_df = athlete_df[athlete_df['Sport'] == sport]
        athlete_df['Medal'].fillna('No Medal', inplace=True)
        return athlete_df

def get_m_w_part_years(df):
    df = df[df['Season'] == 'Summer']
    df = pd.merge(df, region_df, on='NOC', how='left')
    df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df = df.copy()
    male = athlete_df[athlete_df['Sex'] == 'M']
    female = athlete_df[athlete_df['Sex'] == 'F']
    male = male.groupby('Year').count()['Sex'].reset_index()
    female = female.groupby('Year').count()['Sex'].reset_index()
    sex_df = pd.merge(male, female, on='Year', how='left')
    sex_df.rename(columns={
        'Sex_x': 'Male',
        'Sex_y': 'Female'
    }, inplace=True)
    sex_df['Female'] = sex_df['Female'].fillna(0)
    sex_df['Female'] = sex_df['Female'].astype('int')
    return sex_df




