from crypt import methods
from distutils.log import debug
from os import mkdir
from venv import create
from flask import Flask, render_template, request, redirect, url_for,send_file
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import mysql.connector as mysql
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from urllib import parse
import csv
import io
import pymongo
import dns
import youtube_dl
import logging
import os


app = Flask(__name__)

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html',is_index=True)


@app.route('/videos',methods=['GET','POST'])
@cross_origin()
def videos():
    if request.method == 'POST':
        youtuber = request.form['search']

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)


        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


        # if want to insert into database uncomment below line
        # try:
        #     client = pymongo.MongoClient("mongodb+srv://sandeep:sandeep001@cluster0.l25wu2o.mongodb.net/?retryWrites=true&w=majority")
        #     db = client['test']
        # except Exception as e:
        #     logging.INFO("MongoDB connection failed")
        

        # Scroll to bottom of page
        def scroll_page():
            for x in range(1):
                html = driver.find_element(by=By.TAG_NAME,value="html")
                html.send_keys(Keys.END)
                time.sleep(2)

        def channel_urls(url):
            scroll_page()

            # Get all channel urls
            

            try:
                channel_name = driver.find_element(by=By.XPATH,value='//*[@id="channel-name"]').text
            except:
                logging.INFO("Channel name not found")
            try:
                channel_image = driver.find_element(by=By.XPATH,value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/yt-img-shadow/img').get_attribute('src')
            except:
                logging.INFO("Channel image not found")
            try:
                subscribers_count = driver.find_element(by=By.XPATH,value='//*[@id="subscriber-count"]').text
            except:
                logging.INFO("Subscribers count not found")
            
            channel_info = {
                'channel_name':channel_name,
                'channel_image':channel_image,
                'subscribers_count':subscribers_count,
                
            }
            

            channel_details.append(channel_info)

            
            # insert into mongodb
            # try:
            #     col = db['about_channel']
            #     col.insert_many(channel_details)
            #     print('inserted into mongodb')
            # except Exception as e:
            #     print('not inserted into mongodb')

            


            # scraping all the videos 
            videos = driver.find_elements(by=By.CLASS_NAME,value="style-scope ytd-grid-video-renderer")

            # scraping top 50 urls 
            for video in videos[:50]:
                try:
                    video_url = video.find_element(by=By.TAG_NAME,value="a").get_attribute("href")
                except Exception as e:
                    logging.INFO("Video url not found")

            
                channel_video_info = {
                    'video_url':video_url,
                }

                channel_urls_list.append(channel_video_info)


                # Video_title
                def video_title():
                    video_title = "//div[@class='watch-main-col']/meta[@itemprop='name']"
                    elems = driver.find_elements(by=By.XPATH,value=video_title)
                    for elem in elems:
                        return elem.get_attribute("content")


                # partial video description
                def video_description():
                    vid_desc = "//div[@class='watch-main-col']/meta[@itemprop='description']"
                    elems = driver.find_elements(by=By.XPATH,value=vid_desc)
                    for elem in elems:
                        return elem.get_attribute("content")

                # get thumbnail of video
                def video_thumbnail(url):
                    url_parsed = parse.urlparse(url)
                    qsl = parse.parse_qs(url_parsed.query)
                    id = qsl['v'][0]
                    thumbnail = f'https://i.ytimg.com/vi/{id}/maxresdefault.jpg'
                    return thumbnail

                def video_id(url):
                    url_parsed = parse.urlparse(url)
                    qsl = parse.parse_qs(url_parsed.query)
                    id = qsl['v'][0]
                    return id

                # publish_date
                def video_publish():
                    pub_date = "//div[@class='watch-main-col']/meta[@itemprop='datePublished']"
                    elems = driver.find_elements(by=By.XPATH,value=pub_date)
                    for elem in elems:
                        return elem.get_attribute("content")


                # upload_date
                def video_upload():
                    upload_date = "//div[@class='watch-main-col']/meta[@itemprop='uploadDate']"
                    elems = driver.find_elements(by=By.XPATH,value=upload_date)
                    for elem in elems:
                        return elem.get_attribute("content")


                # genre
                def video_genre():
                    genre = "//div[@class='watch-main-col']/meta[@itemprop='genre']"
                    elems = driver.find_elements(by=By.XPATH,value=genre)
                    for elem in elems:
                        return elem.get_attribute("content")


                # video_width
                def video_width():
                    v_width = "//div[@class='watch-main-col']/meta[@itemprop='width']"
                    elems = driver.find_elements(by=By.XPATH,value=v_width)
                    for elem in elems:
                        return elem.get_attribute("content")


                # video_height
                def video_height():
                    v_height = "//div[@class='watch-main-col']/meta[@itemprop='height']"
                    elems = driver.find_elements(by=By.XPATH,value=v_height)
                    for elem in elems:
                        return elem.get_attribute("content")


                # Interaction Count
                def video_interactions():
                    interactions = "//div[@class='watch-main-col']/meta[@itemprop='interactionCount']"
                    elems = driver.find_elements(by=By.XPATH,value=interactions)
                    for elem in elems:
                        return elem.get_attribute("content")


                # Video_title
                def video_title():
                    video_title = "//div[@class='watch-main-col']/meta[@itemprop='name']"
                    elems = driver.find_elements(by=By.XPATH,value=video_title)
                    for elem in elems:
                        return elem.get_attribute("content")


                # Channel_name
                def channel_name():
                    channel_name = ("//div[@class='watch-main-col']/span[@itemprop='author']/link[@itemprop='name']")
                    elems = driver.find_elements(by=By.XPATH,value=channel_name)
                    for elem in elems:
                        return elem.get_attribute("content")


                # Number Likes
                def video_likes():
                    likes_xpath = "(//div[@id='top-level-buttons-computed']//*[contains(@aria-label,' likes')])[last()]"
                    return driver.find_element(by=By.XPATH,value=likes_xpath).text




            

            

            count = 0
            for url in channel_urls_list:
                driver.get(url['video_url'])
                count += 1
                time.sleep(3)
                subscribe_button = '//*[@id="subscribe-button"]'
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, subscribe_button)))

                try:
                    title = video_title()
                    description = video_description()
                    thumbnail = video_thumbnail(url['video_url'])
                    videoid = video_id(url['video_url'])
                    publish_date = video_publish()
                    upload_date = video_upload()
                    genre = video_genre()
                    width = video_width()
                    height = video_height()
                    interactions = video_interactions()
                    channelname = channel_name()
                    likes = video_likes()
                except:
                    exception_urls.append(url['video_url'])


                video_info = {
                    'video_title':title,
                    'video_description':description,
                    'video_thumbnail':thumbnail,
                    'video_id':videoid,
                    'video_publish_date':publish_date,
                    'video_upload_date':upload_date,
                    'video_genre':genre,
                    'video_width':width,
                    'video_height':height,
                    'video_interactions':interactions,
                    'video_channel_name':channelname,
                    'video_likes':likes,
                    'video_url':url['video_url']
                
                    
                }

               

                video_info_list.append(video_info)


            #insert into database
            # try:
            #     col = db['video_details']
            #     col.insert_many(video_info_list)
            # except Exception as e:
            #     print("Error inserting into database video details")
                

               

        def about_channel(about_url):

                chan_name_xp = '//*[@id="channel-name"]'
                chan_join = './/*[@id="right-column"]/yt-formatted-string[2]/span[2]'
                chan_views = './/*[@id="right-column"]/yt-formatted-string[3]'
                chan_desc = '//*[@id="description-container"]/yt-formatted-string[2]'
                

                #Scrap Channel Name
                try:
                    channel_name = driver.find_element(by=By.XPATH,value=chan_name_xp).text
                except (Exception,):
                    logging.INFO("Channel name not found")

                # Scrap Channel Join Date (about)
                try:
                    channel_join = driver.find_element(by=By.XPATH,value=chan_join).text
                except (Exception,):
                    logging.INFO("Channel join date not found")

                # Scrap Channel Views (about)
                try:
                    channel_views = driver.find_element(by=By.XPATH,value=chan_views).text
                except (Exception,):
                    logging.INFO("Channel views not found")
                # Scrap Channel Description (about)
                try:
                    channel_description = driver.find_element(by=By.XPATH,value=chan_desc).text
                except (Exception,):
                    logging.INFO("Channel description not found")

                about_items = {
                    'name':channel_name,
                    'join':channel_join,
                    'views':channel_views,
                    'description':channel_description,
                }

                about_details.append(about_items)

                # insert into mongodb
                # try:
                #     col = db['about_page']
                #     col.insert_many(about_details)
                # except Exception as e:
                #     print('Error inserting into database')


        #list for video info
        video_info_list = []


        #list for exception urls
        exception_urls = []

        
        channel_urls_list = []

        #channel info
        channel_details  = []
        
        #about channel
        about_details = []

        print("scraping data for ",youtuber)
        url = f"https://www.youtube.com/{youtuber}/videos"
        driver.get(url)
        scroll_page()
        channel_urls(url)
        about_url = f"https://www.youtube.com/{youtuber}/about"
        driver.get(about_url)
        driver.implicitly_wait(10)
        about_channel(about_url)
        driver.quit()
    

        context = {
            'video_info_list':video_info_list,
            'exception_urls':exception_urls,
            'channel_info':channel_details,
            'about_channel':about_details,
        }


    return render_template('videos.html',is_videos=True,**context)
      

@app.route('/videos/<string:id>',methods=['GET','POST'])
@cross_origin()
def comments(id):

    #chrome_path = "/home/sandeep/Desktop/youtubeTask/chromedriver"
    url = f"https://www.youtube.com/watch?v={id}"
    thumbnail = f'https://i.ytimg.com/vi/{id}/maxresdefault.jpg'

    try:
        client = pymongo.MongoClient("mongodb+srv://sandeep:sandeep001@cluster0.l25wu2o.mongodb.net/?retryWrites=true&w=majority")
        db = client['test']
    except:
        print("Error connecting to database")
    
    


    # change youtube URL to scrape different video's comments
    page_url = url  # Chopin!
    # --------------------------------------------------------------------

    # --------------- PAGE ACCESS ---------------
    # accessing the page holding comments (here: youtube)
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'))
    driver.get(page_url)
    time.sleep(2)  # give the page some time to load

    video_title_Xpath= "//div[@class='watch-main-col']/meta[@itemprop='name']"
    video_title= [elem.get_attribute("content") for elem in driver.find_elements(by=By.XPATH,value=video_title_Xpath)]
    channel_name = ("//div[@class='watch-main-col']/span[@itemprop='author']/link[@itemprop='name']")
    channel_name =[elem.get_attribute("content") for elem in driver.find_elements(by=By.XPATH,value=channel_name)]
    posted_date = ("//div[@class='watch-main-col']/meta[@itemprop='datePublished']")
    posted_date = [elem.get_attribute("content") for elem in driver.find_elements(by=By.XPATH,value=posted_date)]
    SCROLL_PAUSE_TIME = 2
    CYCLES = 30

    # we know there's always exactly one HTML element, so let's access it
    html = driver.find_element(by=By.TAG_NAME,value='html')
    # first time needs to not jump to the very end in order to start
    html.send_keys(Keys.PAGE_DOWN)  # doing it twice for good measure
    html.send_keys(Keys.PAGE_DOWN)  # one time sometimes wasn't enough
    # adding extra time for initial comments to load
    # if they fail (because too little time allowed), the whole script breaks
    time.sleep(SCROLL_PAUSE_TIME * 3)
    # and now for loading the hidden comments by scrolling down and up
    for i in range(CYCLES):
        html.send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)

    
   
    

    # --------------- GETTING THE COMMENT TEXTS ---------------
    comment_elems = driver.find_elements(by=By.XPATH,value='//*[@id="content-text"]')
    comment_count = driver.find_element(by=By.XPATH,value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer[1]/div[1]/h2/yt-formatted-string/span[1]').text
    username_elems=driver.find_elements(by=By.XPATH,value='//*[@id="author-text"]')
    print(comment_count)


    comment_list = []
    for username,comment in zip(username_elems,comment_elems):
        username = username.text
        comment = comment.text

        comments_info = {
            "username":username,
            "comment":comment,
            "video_title":video_title,
            "channel_name":channel_name,
        }
        comment_list.append(comments_info)

    
    #  # insert into mongodb
    # try:
    #     col = db['comments']
    #     col.insert_many(comment_list)
        
    # except Exception as e:
    #     print('Error inserting into database')

    driver.quit()
    
    context = {
        "comments":comment_list,
        "thumbnail":thumbnail,
        "video_title":video_title,
        "channel_name":channel_name,
        "posted_date":posted_date,
        "comment_count":comment_count,
    }

    return render_template('comments.html', **context)    


@app.route('/download_video',methods=['GET','POST'])
@cross_origin()
def downlaod_video():
    try:
        youtube_id = request.form["video_id"]
        video_url = f"https://www.youtube.com/watch?v={youtube_id}"
        video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download = False)
        SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'
        file = f"{video_info['title']}.mp3"
        options={
            'format':'bestvideo+bestaudio',
            'writethumbnail':'writethumbnail',
            'writesubtitles':'writesubtitles',
            'writedescription':'writedescription',
            'outtmpl':SAVE_PATH + '/%(title)s.%(ext)s',
            }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
    except:
        logging.error("Error downloading video")


@app.route('/about')
@cross_origin()
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)