def transformations(data):
    #fill nulls with Other
    data['phone'] = data['phone'].fillna('Other')
    
    #make dummies for iphone, android, and other
    #make dummies for each city
    df = pd.concat([data, pd.get_dummies(data['phone'])], axis=1)
    df = df.drop('Other',axis =1)
    df = pd.concat([df, pd.get_dummies(df['city'])], axis=1)
    df = df.drop('phone',axis =1)
    df = df.drop('city',axis =1)
    df = df.drop('Winterfell',axis =1)
    
    #full nulls with average
    df['no_rating'] = df['avg_rating_of_driver'].isna().astype(int)
    df['avg_rating_of_driver'] = df['avg_rating_of_driver'].fillna(df['avg_rating_of_driver'].mean())
    df['avg_rating_by_driver'] = df['avg_rating_by_driver'].fillna(df['avg_rating_by_driver'].mean())
    
    #convert the dates
    df["last_trip_date"]=pd.to_datetime(df['last_trip_date'])
    df["signup_date"]=pd.to_datetime(df['signup_date'])

    #create target
    df["target"] = (df["last_trip_date"]<datetime.date(2014,6,1))*1
    
    #get the dates in correct format
    df['signup_date'] = df['signup_date'].astype(np.int64) // 10**9
    
    df = df.drop('last_trip_date',axis =1)
    
    #scale surge percent
    df['surge_pct'].apply(lambda x: np.log(x+1) if x < 80 else x)

    df["trips_in_first_30_days"] = df["trips_in_first_30_days"].apply(lambda x: df["trips_in_first_30_days"].mean() if x >70 else x)
    
    df = df[df.avg_surge < 5]
    return df