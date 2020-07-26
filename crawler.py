#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import packages for crawler
import tweepy
from tweepy import OAuthHandler
import requests
import shutil
import os
import time
import numpy as np
#import packages for CNN
from keras.models import model_from_json
import tensorflow as tf
from tensorflow import keras
import json
from keras import optimizers


# In[ ]:


#tweepy method
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


# In[ ]:


#get images from users friends, save them.
def get_img(api,username):
    # Iterate through the last 30 tweets from each of the users friends.
    # get the id's for each tweet.
    friend_id = api.friends_ids(username)

    print(f"GET_IMAGE: got {len(friend_id)} friend id's")
    media_urls = []
    tweet_ids = []
    path = f"C:\\Users\\Monty\\Desktop\\my_website\\static\\twitter_images\\{username}"
    os.mkdir(path)

    for id in friend_id:
        try:
            tweets = tweepy.Cursor(api.user_timeline, user_id = id).items(30)
            try:
                for status in tweets:
                    media = status.entities.get('media', [])
                    if(len(media) > 0):
                        media_urls.append(media[0]['media_url'])
                        tweet_ids.append(status.id)
            except RecursionError:
                print("RecursionError")
                pass
        except tweepy.TweepError:
            pass
    print("GET_IMAGE: got tweet ids and media file urls")
    print(f"GET_IMAGE: got {len(media_urls)} media urls")
    print(f"GET_IMAGE: got {len(tweet_ids)} tweet ids")
    #create dir to hold the twitter images
    #populate that dir with images from tweets

    print("GET_IMAGE: starting twitter_image download")
    image_paths = []
    for i,url in enumerate(media_urls):
        res = requests.get(url)
        name = f"image_{i}.jpg"
        path = path = f"C:\\Users\\Monty\\Desktop\\my_website\\static\\twitter_images\\{username}"
        path = path + "\\" + name
        image_paths.append(path)
        imagefile = open(path, 'wb')
        for chunk in res.iter_content(100000):
            imagefile.write(chunk)
        imagefile.close()
    print("GET_IMAGE: finished downloading to twitter_images")
    print(f"GET_IMAGE: {len(image_paths)} urls for downloaded images")
    print(f" GET_IMAGE: files output looks like: {image_paths[0]}")
    return tweet_ids, image_paths


# In[ ]:
#preprocess the images and keep a list of the unprocessed images.
def process_images(image_paths):
    print("PROCESS_IMAGES: starting processing")
    processed_images = []
    for path in image_paths:
        img_array = keras.preprocessing.image.load_img(path, target_size=(32,32,3))
        img_array = keras.preprocessing.image.img_to_array(img_array)
        img_array /= 255
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        processed_images.append(img_array)
    print(f"PROCESS_IMAGES: processed {len(processed_images)} images")
    return processed_images



# In[ ]:


#use the CNN to predict if any of the images are likely to be cats and populate list if they are
def predict_cats(processed_images,model):
    print(f"PREDICT_CATS: begining prediction on {len(processed_images)} images")
    is_cat = np.zeros(len(processed_images))
    for i,img in enumerate(processed_images):
        if model.predict(img)[0] > .5:
            is_cat[i] = 1
    num_cats = np.sum(is_cat)
    print(f"PREDICT_CATS: found {num_cats} cats.")

    if num_cats > 0:
        is_empty = False
    else:
        is_empty = True
    return is_cat, is_empty



# In[ ]:

def get_cat_paths(is_empty,is_cat,image_paths,username):
    catpaths = []
    if is_empty:
        catpaths.append("static\\no_cats\\no_cats.jpg")
    else:
        for i, cat in enumerate(is_cat):
            if cat == 1:
                path = os.path.split(image_paths[i])[1]
                path = "twitter_images\\"+f"{username}\\" + path
                catpaths.append(path)

    return catpaths


def garbage_collect(username):
    user_images = []
    userdir = "C:\\Users\\Monty\\Desktop\\my_website\\static\\twitter_images\\"+f"{username}"
    files = os.listdir(userdir)
    for file in files:
        image_loc = userdir + "\\" + file
        user_images.append(image_loc)
    time.sleep(600)
    for path in image_loc:
        os.remove(path)
    os.rmdir(userdir)
    return "bye"








# In[ ]:


def driver(username,consumer_key,consumer_secret,access_token,access_secret):
    #beg daddy twitter for a scrap of data.
    print(f"USERNAME: {username}")
    print("INITIALIZING API")
    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse
    # User() is the data model for a user profil
    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse
    # You need to do it for all the models you need

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth,wait_on_rate_limit=True)
    print("INITIALIZED API")

    # load json and create model
    print("LOADING MODEL")
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("model.h5")
    model.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer=optimizers.Adam(lr=1e-5));
    print("LOADED MODEL")

    #get tweets
    print("RUNNING GET_IMG")
    tweet_ids, image_paths = get_img(api,username)
    print("GET_IMG FINISHED")

    #process images, do linear algebra, make cat dir.
    print("RUNNING PROCESS_IMAGES")
    processed_images = process_images(image_paths)
    print("PROCESS_IMAGES FINISHED")

    print("RUNNING PREDICT_CATS")
    is_cat, is_empty  = predict_cats(processed_images,model)
    print("PREDICT_CATS FINISHED")

    return get_cat_paths(is_empty,is_cat,image_paths,username)

# In[ ]:


if __name__ == "__main__":
    driver()
    garbage_collect()
