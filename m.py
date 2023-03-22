import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import streamlit as st  # 🎈 data web app development
import pandas as pd # read csv, df manipulation
import numpy as np # np mean, np random
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express  as px  # interactive charts
import time  # to simulate a real time data, time loop

st.set_page_config(page_title="European hotel Customers Review",page_icon=':bar_chart:')

def login():
    names = ['Shruti Ushire','Yash Jadhav']
    usernames = ['shruti','yash']
    passwords = ['admin','coadmin']
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login('Login', 'main')
        
    if st.session_state["authentication_status"]:
        test=authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{st.session_state["name"]}*')
        # Importing data set
        df = pd.read_csv('data.csv')
        st.dataframe(df)
        df.info()

        tab1 = st.tabs(["DASHBOARD"])

        
            # ---- MAINPAGE ----
        st.title(":bar_chart: European customers")
        st.markdown("##")



            #To make draw bar chart (satisfaction levels of people)
        col1, col2 = st.columns(2)
        with col1:
                
            t=df['satisfaction'].value_counts()
        st.write(t)
        with col2:
                st.header('satisfaction')
        st.bar_chart(t)


            #
        st.header(':clipboard: Overview of Hotel Users')     
        fig, ax = plt.subplots(2,2, figsize=(14, 12))
        sns.countplot(data=df, x='Gender', hue='satisfaction', ax=ax[0][0])
        sns.countplot(data=df, x='purpose_of_travel', hue='satisfaction', ax=ax[0][1])
        sns.countplot(data=df, x='Type_of_Travel', hue='satisfaction', ax=ax[1][0])
        sns.countplot(data=df, x='Type_Of_Booking', hue='satisfaction', ax=ax[1][1])
        st.pyplot(fig)

            #
        def df_countplot(df, target):
            f, axes = plt.subplots(1, 2, figsize=(15,5))
            ax1 = sns.countplot( x = target, data = df,  ax=axes[0])

            counts = df.groupby([target, 'satisfaction']).size().to_frame('Total')
            counts = counts.reset_index()
            ax2 = sns.barplot(data=counts, y='Total', x=target, hue='satisfaction', ax=axes[1])
            st.pyplot(f)
            #     return ax1

        def pivot_satisfaction(df,target):
            df_rate = pd.pivot_table(
                df[['id',target,'satisfaction']],
                index       =[target],
                columns     =['satisfaction'],
                aggfunc     ="count",
                fill_value  =0,
            ).reset_index()

            df_rate.columns=[target,'neutral or dissatisfied','satisfied']

            df_rate['total'] = df_rate['neutral or dissatisfied'] + df_rate['satisfied']
            df_rate["satisfaction Rate"] = round((df_rate['satisfied']/df_rate['total'])*100,2)
            df_rate["dissatisfied Rate"] = round((df_rate['neutral or dissatisfied']/df_rate['total'])*100,2)
            return df_rate

            #
        col1, col2 = st.columns(2)
        with col1:
                
            t1=df['Gender'].value_counts()
        st.write(t1)
        with col2:
                st.header('Gender')
        st.bar_chart(t1)

            #
        st.title(":hotel: Pupose of travel")
        df_countplot(df,"purpose_of_travel")
        t3=df['purpose_of_travel'].value_counts()
        st.write(t3)

            #
        st.title(":briefcase: Type of Travel")
        df_countplot(df,"Type_of_Travel")
        t4=df['Type_of_Travel'].value_counts()
        st.write(t4)

            #
        st.title(":briefcase: Type Of Booking")
        df_countplot(df,"Type_Of_Booking")
        t4=df['Type_Of_Booking'].value_counts()
        st.write(t4)

        col1, col2 = st.columns(2)
        with col1:
                
            t1=df['Gender'].value_counts()
        st.write(t1)
        with col2:
                st.header('Gender')
        st.bar_chart(t1)

        
            #Numeric data visualization
        st.title(" :hotel: Reviews for Services of Hotel")
        fig, ax = plt.subplots(5,2, figsize=(14, 20))
        sns.countplot(data=df, x='Hotel_wifi_service', hue='satisfaction', ax=ax[0][0])
        sns.countplot(data=df, x='Departure_Arrival_convenience', hue='satisfaction', ax=ax[0][1])
        sns.countplot(data=df, x='Ease_of_online_booking', hue='satisfaction', ax=ax[1][0])
        sns.countplot(data=df, x='Hotel_location', hue='satisfaction', ax=ax[1][1])
        sns.countplot(data=df, x='Food_and_drink', hue='satisfaction', ax=ax[2][0])
        sns.countplot(data=df, x='Other_service', hue='satisfaction', ax=ax[2][1])
        sns.countplot(data=df, x='Stay_comfort', hue='satisfaction', ax=ax[3][0])
        sns.countplot(data=df, x='Common_Room_entertainment', hue='satisfaction', ax=ax[3][1])
        sns.countplot(data=df, x='Checkin_Checkout_service', hue='satisfaction', ax=ax[4][0])
        sns.countplot(data=df, x='Cleanliness', hue='satisfaction', ax=ax[4][1])
        st.write(fig)

        facet = sns.FacetGrid(df, hue = 'satisfaction', aspect = 4)
        facet.map(sns.kdeplot, "Age", shade= True)
        facet.add_legend()
        st.pyplot(facet)

        plt.rcParams["figure.figsize"] = [8,8]
        plt.rcParams["figure.autolayout"] = True
        sns.histplot(data = df, x = "Age", kde = True, hue = "satisfaction")

        #Age and hotel wifi service
        st.title("Age and hotel wifi service")
        df_countplot(df,"Hotel_wifi_service")
        t5=df['Hotel_wifi_service'].value_counts()
        st.write(t5)

        #Age and common room entertaiment
        st.title("Age and common room entertaiment")
        df_countplot(df,"Common_Room_entertainment")
        t6=df['Common_Room_entertainment'].value_counts()
        st.write(t6)

        #Age and stay comfort
        st.title("Age and stay comfort")
        df_countplot(df,"Stay_comfort")
        t7=df['Stay_comfort'].value_counts()
        st.write(t7)


           
        tab1 = st.tabs(["Feedback Form"])
        st.header(":mailbox: Feedback Form for Customers!")

        contact_form = """
        <form action="https://formsubmit.co/shruti.dulu@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name"placeholder="Your name" required><br>
            <input type="email" name="email" placeholder="Your email" required><br>
            <textarea name="message" placeholder="Add your Feedback"></textarea><br>
            <button type="submit" style= "background-color:green" >Send</button><br>
        </form>
        """

        st.markdown(contact_form, unsafe_allow_html=True)
    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')
        
def main():
    login()

if __name__ == "__main__":
    main()