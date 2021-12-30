import pandas as pd
import psycopg2
import streamlit as st
import altair as alt
from configparser import ConfigParser
import matplotlib.pyplot as plt


@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

def fetch_data(sql: str):
    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

def Search_Movie():
    st.subheader("Search for a Movie")
    m=set()
    g=set()
    l=set()
    c=set()
    y=set()
    d=set()
    p=set()
    a=set()


    with st.form(key='searchform'):
            search_movie=st.text_input("Enter a Movie Name")
            submit_button=st.form_submit_button(label="Search")
            moviename=search_movie.strip().title()

            if submit_button:
                try:
                    st.info("Results")
                    st.markdown("__Expand to see the Results__")
                    genre=f"select M.Movie_Name, G.Type as genretype, M.Movie_Language, M.Country, M.Release_Date, D.Name as dname, P.Name as pname, A.Name as aname from Movie M, Belong_To BT , Genre G, Director D, Producers P, Produced_By PB, Actors A, Acted_By AB where M.Movie_Id = BT.Movie_Id and BT.Genre_Id = G.Genre_Id and D.Director_Id = M.Director_Id and PB.Movie_Id = M.Movie_Id and P.Producer_Id = PB.Producer_Id and AB.Movie_Id = M.Movie_Id and A.Actor_Id = AB.Actor_Id and M.Movie_Name = '{moviename}';"
                    genrequery=fetch_data(genre)
                    #st.write(genrequery)
                    for i in genrequery:
                        m.add(i[0])
                        g.add(i[1])
                        l.add(i[2])
                        c.add(i[3])
                        y.add(i[4])
                        d.add(i[5])
                        p.add(i[6])
                        a.add(i[7])
                    with st.expander('{}'.format(next(iter(m)))):
                        st.markdown("__Genre__")
                        for gn in g:
                            st.write(gn)
                        st.markdown("__Language__")
                        st.write(next(iter(l)))
                        st.markdown("__Country__")
                        st.write(next(iter(c)))
                        st.markdown("__Year of Release__")
                        st.write(next(iter(y)))
                        st.markdown("__Actors__")
                        for an in a:
                            st.write(an)
                        st.markdown("__Producers__")
                        for pn in p:
                            st.write(pn)
                        st.markdown("__Director__")
                        st.write(next(iter(d)))
                        st.success("Successful")
                        st.subheader('The query is returning the information of the movie given by user')
                except:
                    st.error("No such movie found.Try another movie")
                    

def TopRattedGenre():
    st.subheader("Top ratted movies of selected genre")
    sql_genre = "select distinct type from Genre;"
    try:
        genre_names = query_db(sql_genre)["type"].tolist()
        genre_name = st.selectbox("Choose a genre", genre_names)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

    try:
        if genre_name:
            sql_movie = f"Select M.movie_name as Movie_Name,Round(avg(R.rating),1) as Ratings from Movie M,Genre G,Belong_to B,Rated_by R where B.movie_id=M.movie_id and M.movie_id=R.movie_id and B.genre_id=G.genre_id and G.type='{genre_name}' group by M.movie_name having avg(R.Rating)>=6.5 order by Ratings desc;"
            movie_info = query_db(sql_movie)
            for i in range(len(movie_info)) :
                st.write(str(movie_info.loc[i, "movie_name"])+" with rating of " +str(movie_info.loc[i, "ratings"]))
            st.write(movie_info)
            st.success("Successful")
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")
    st.subheader("The query is returning movies of the selected genre whose rating is more than 65%")


def AgeDistribution():
    st.subheader("Get age wise distribution of people interested in particular genre")
    sql_genre = "select distinct type from Genre;"
    try:
        genre_names = query_db(sql_genre)["type"].tolist()
        genre_name = st.selectbox("Choose a genre", genre_names)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

    try:
            if genre_name:
               sql_agecount = f"Select S.AGE,count(S.age) as peoplecount from Spectators S,Genre G,Belong_to B,Viewed_by VB where VB.spectator_id=S.spectator_id and VB.movie_id=B.movie_id and G.genre_id=B.genre_id and G.type='{genre_name}' group by S.age;"
               agecount_info = query_db(sql_agecount)
               chart = (
                        alt.Chart(
                        data=agecount_info,
                        title="Age wise count of people interested in particular genre",
                          )
                        .mark_line()
                        .encode(
                        x=alt.X("age", axis=alt.Axis(title="Age")),
                        y=alt.Y("peoplecount", axis=alt.Axis(title="No. of people intrested")),
                        )
                      )

               st.altair_chart(chart)
               st.write(agecount_info)
               st.success("Successful")
    except:
            st.write("Sorry! Something went wrong with your query, please try again.")
    st.subheader("The query is returning age wise count of no. of people interested in particular genre in a form of line graph along with the table")
        
def Distribute_Scenes():
    st.subheader("Distribution of type of scenes of particular actor")
    
    sql_actor = "select distinct name from Actors;"
    try:
        actor_names = query_db(sql_actor)["name"].tolist()
        actor_name = st.selectbox("Choose an actor", actor_names)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")
    
    st.write('You selected:', actor_name)
        
    try:
        if actor_name:
            sql_scenes = f"select HS.type as scene_type, count(HS.type) as no_of_scenes from Actors A,Acted_by AB,Have_Scenes HS where HS.movie_id=AB.movie_id and A.actor_id=AB.actor_id and A.name='{actor_name}' group by HS.type order by count(HS.type) desc;"             
            scenes_info = query_db(sql_scenes)
            
            labels = scenes_info['scene_type']
            sizes = scenes_info['no_of_scenes']

            if scenes_info.empty:
                st.subheader("This actor has not acted in any film yet.")
            else:
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
                ax1.axis('equal')  

                st.pyplot(fig1)

                st.write(scenes_info)
                st.success("Successful")
            
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")
    st.subheader('The query is returning distribution type of scenes that the actor has worked in along with its percentage value in a form of pie chart')

def GenderDistribution(start_year, end_year, awards):
    try:
       if awards and start_year and end_year:
            sql_gender = f"select A.gender as gender, count(A.gender) as population from Receive_Awards RA, Actors A where RA.actor_id = A.actor_id and RA.type = '{awards}' and RA.year>='{start_year}' and RA.year<='{end_year}' group by A.gender order by count(A.gender) desc;"
            gender_info = query_db(sql_gender)

            labels = gender_info['gender']
            sizes = gender_info['population']
        
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
            ax1.axis('equal')  

            st.pyplot(fig1)

            st.write(gender_info)
            st.success("Successful")
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")
    st.subheader('The query will show percentage distribution of all genders who has received a particular type of award within given range of year')

def Most_Watched_year():
    st.subheader("Top 5 Most Watched Movies within range of year specified by the user")
    try:
        start_year1, end_year1 = st.select_slider(
         'Select a range of year in which actor must have received award',
          options=['1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015', '2021'],
          value=('1980', '2000'))
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

    try:
        if start_year1 and end_year1:
            sql_count=f"Select M.movie_name,M.release_date,count(V.spectator_id) from Movie M ,viewed_by V where V.movie_id=M.movie_id and M.release_date>={start_year1} and M.release_date<={end_year1} group by M.release_date,M.movie_name order by count desc limit 5;"
            most_watched_info=query_db(sql_count)
            for i in range(len(most_watched_info)) :
                st.write(most_watched_info.loc[i, "movie_name"], most_watched_info.loc[i, "release_date"])
            st.write(most_watched_info)
            st.success("Successful")
                
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")
    st.subheader('The query is returning top 5 most watched movies in the range of years specified by user')


    



def main():
    st.title("Movie Recommendation System")
    menu=['Search for a Movie','Know about type of scenes of particular actor','Get age wise distribuion of people intrested in particular genre',
    'Search for a Movie of particular genre','Gender Distribution based on awards and year range','Most watched Movie for particular range of year']
    choice = st.sidebar.selectbox('Menu',menu)
    if choice=='Search for a Movie':
        Search_Movie()
        
    elif choice=="Search for a Movie of particular genre":
        TopRattedGenre()
        
    elif choice=="Know about type of scenes of particular actor":
        Distribute_Scenes()

    elif choice=="Get age wise distribuion of people intrested in particular genre":
        AgeDistribution()

    elif choice=='Gender Distribution based on awards and year range':
        st.subheader('Gender wise distribution based on award type and year range')
        start_year, end_year = st.select_slider(
         'Select a range of year in which actor must have received award',
          options=['1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015', '2021'],
          value=('1980', '2000'))
        awards = st.radio(
          "Award Categories",
          ('Best Leading Role', 'Best Supporting Role'))
        GenderDistribution(start_year, end_year, awards)
    elif choice=='Most watched Movie for particular range of year':
        Most_Watched_year()





if __name__ == '__main__':
    main()




