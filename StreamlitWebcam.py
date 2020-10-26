import streamlit as st
#EDA Pkgs
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import cv2
from PIL import Image, ImageEnhance
import os
import face_recognition

# Functions
from db_fxn import *
#Templates
from templates import *

# Security
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def main():
    """A Webcam Application"""
    st.title("Simple Webcam Application")
    st.text('Built with Streamlit and OpenCV')

    menu = ["Home","Webcam","Login","SignUp","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")
        result = view_all_notes()
        # st.write(result)


    elif choice == "Login":
        st.subheader("Log in Here")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox('Login'):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged in as: {}".format(username))
            else:
                st.warning('Incorrect username and password')


    elif choice == "SignUp":
        st.subheader("Create a new account here")
        new_user = st.text_input('User name')
        new_password = st.text_input('Password',type='password')
        if st.button('SignUp'):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success('You have successfully created an account')

    elif choice =="Webcam":
        st.subheader("Webcamera Application")
        #capture the video from default camera
        webcam_video_stream = cv2.VideoCapture(0)

        #initialize the array variable to hold all the face locations in the frame
        all_face_locations = []

        while True:
            #get current frame
            ret, current_frame = webcam_video_stream.read()
            #resuze the current frame to 1/4 the size to process faster
            current_frame_small = cv2.resize(current_frame,(0,0),fx=0.25,fy=0.25)

            #detect all face locations in the image
            #arguments are image, no_of_times_to_upsample, model
            all_face_locations = face_recognition.face_locations(current_frame_small,number_of_times_to_upsample=2,model='hog')

            for index,current_face_location in enumerate(all_face_locations):
                #splitting the tuple to get the four position values of current face
                top_pos,right_pos,bottom_pos,left_pos= current_face_location
                top_pos = top_pos * 4
                right_pos = right_pos * 4
                bottom_pos = bottom_pos * 4
                left_pos = left_pos * 4
                #print the location of the current face detected
                print('Found face {} at top: {}, right:{}, bottom:{}, left:{}'.format(index+1,top_pos,right_pos,bottom_pos,left_pos))
                #current_face_image = image_to_detect[top_pos:bottom_pos,left_pos:right_pos]
                #draw a rectangle around the face detected
                cv2.rectangle(current_frame,(left_pos,top_pos),(right_pos,bottom_pos),(0,0,255),2)
            cv2.imshow('Webcam Video',current_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        webcam_video_stream.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
