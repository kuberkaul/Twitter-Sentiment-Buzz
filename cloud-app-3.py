from pygeocoder import Geocoder
from google.appengine.ext import db
from google.appengine.api import users
import urllib, json, pprint, cgi, webapp2, datetime, shlex,  re
import json as simplejson
from google.appengine.api import urlfetch
from collections import Counter


MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action = '/' method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Welcome!"></div>
    </form>
    <hr>
    
  </body>
</html>
"""

class Tweet(db.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    Address = db.StringProperty(multiline=True)
    Category = db.StringProperty(multiline=True)
    tweetID = db.StringProperty(multiline=True)
    handle = db.StringProperty(multiline=True)
    username = db.StringProperty(multiline=True)
    timeline = db.StringProperty(multiline=True)
    display_tweet = db.StringProperty(multiline=True)
    profile_image_url = db.StringProperty(multiline=True)
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body style="font-family:calibri;color:Red;i;background-color:Black;"><h1>Cloud Assignment 3!</h1>')
        self.response.write('<html><body style="font-family:calibri"><h1>By: Digvijay Singh(ds3161) & Kuber Kaul(kk2872) </h1>') 
        self.response.write("""Enter the Category and Address for tweet search in that order!:
        <form method = "post">
        <input type = "textarea" name = "Category"></input>
        <input type = "textarea" name = "Address"></input>
        <input type = "submit" ></input>
        </form>""")

	
        # Ancestor Queries, as shown here, are strongly consistent with the High
        # Replication Datastore. Queries that span entity groups are eventually
        # consistent. If we omitted the ancestor from this query there would be
        # a slight chance that Greeting that had just been written would not
        # show up in a query.
		
        """
        self.tweets = Tweet.all()  

        for self.tweet in self.tweets:
            self.response.write('<p>%s</p>' % cgi.escape(self.tweet.id))
            self.response.write('<p>%s</p>' % cgi.escape(self.tweet.handle))
            self.response.write('<p>%s</p>' % cgi.escape(self.tweet.username))
            self.response.write('<p>%s</p>' % cgi.escape(self.tweet.timeline))
            self.response.write('<p>%s</p>' % cgi.escape(self.tweet.display_tweet))
         
        '''self.response.write('<br />')'''

        # Write the submission form and the footer of the page
        """
        self.response.write('</body></html>')

    def post(self):
        self.response.write('<html><body style="font-family:calibri"><h1><b>Cloud Computing Assignment 3 </b></h1>')
        usr_input = self.request.get('Category')
        user_inputs = shlex.split(usr_input)
        user_input = '%20'.join(user_inputs)
        
        rows = self.request.get('Address')
        line = shlex.split(rows)
        final = ','.join(line)
        
        fresults = Geocoder.geocode(final)[0].coordinates
        if not fresults[0]:
            self.response.write('<html><h1>No Address Found</h1>')
        lat = "%g" % round(fresults[0], 2)
        lng = "%g" % round(fresults[1], 2)
        
        tweets = db.GqlQuery("SELECT * "
                                "FROM Tweet "
                                "WHERE Category = :1 AND Address = :2",
                                usr_input,rows)
                                
        display1="No tweets found!!! Search for something better!!"
        display2 = "There are no existing tweets for the search in the cache"
        display3 = "Copying tweets into the cache ...."
        display4 = "Retreiving tweets from the cache...."
        #display5 = ".................................................................................................."
        buzz_words = []
        Dict = ()
        if tweets.count(1) == 0:
            self.response.write('<p>%s</p>' %display2)
            self.response.write('<p>%s</p>' %display3)
            search = urllib.urlopen("http://search.twitter.com/search.json?q="+user_input+"&rpp=5"+"&include_entities=true"+"&result_type=mixed"+"&geocode:"+lat+','+lng+','+"2mi")
            dict = simplejson.loads(search.read())
            if not dict["results"]:
                self.response.write('<p>%s</p>' % display1)
                
            for result in dict["results"]: # result is a list of dictionaries
                display_tweet =result["text"]
                handle = result["from_user"]
                username = result["from_user_name"]
                tweetID= result["from_user_id_str"]
                timeline =str(result["created_at"])
                profile_image_url=result["profile_image_url"]
                self.tweet = Tweet()
                self.tweet.profile_image_url= profile_image_url
                self.tweet.Category = usr_input
                self.tweet.Address= rows
                self.tweet.tweetID = tweetID
                self.tweet.handle= handle
                self.tweet.username = username
                self.tweet.timeline = timeline
                self.tweet.display_tweet = display_tweet
                self.tweet.put()
                list1 = display_tweet.lower()
                list2 = re.findall(r'\w+', list1,flags = re.UNICODE | re.LOCALE)
                stopwords = ['a','able','about','across','after','all','almost','ve','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your', '', ' ', 'http', 'rt', 't', 's', 'co', 'm', ]
                for list3 in list2:
                    if list3 not in stopwords:
                         if len(list3) >= 3:
                            buzz_words.append(list3)
                         else:
                            continue
        f = open("AFINN-111.txt")
        lines = f.readlines()
        line = [i.split()for i in lines]
        count = Counter(buzz_words)
        #self.response.write('<p>%s: Tweet</p>' %  count)
        for wordss, counterss in count.most_common(10):
            sentiment = 0
            self.response.write('<html><h1>******************************************************************</h1>')
            self.response.write('<p>%s<b>  :BUZZ</b></p>' %  wordss)
            #self.tweet.wordss = wordss
            self.response.write('<html><h1>******************************************************************</h1>')
            for result in dict["results"]:# result is a list of dictionaries
                display_tweet = result["text"]
                display_tweet1 = display_tweet.lower()
                display_tweet2 = re.findall(r'\w+', display_tweet1,flags = re.UNICODE | re.LOCALE)
                for display_tweet3 in display_tweet2:
                   for linetup in line:
		      #display_tweet3.encode('utf-8')
		      #linetup[0].encode('utf-8')
                      if ((display_tweet3) == (linetup[0]) and len(linetup) == 2):
                         sentiment += int(linetup[1])                          
                      else:
                         continue
                    
                if wordss in display_tweet2:
                    self.response.write('<p>%s<b>  :Tweet</p></b>' %  display_tweet)
                    self.response.write('<img src =%s></img>' % profile_image_url)
                    self.response.write('<p>%s<b>  :Handle<b/></p>' % handle)
                    self.response.write('<p>%s<b>  :UserName<b/></p>' %  username)
                    self.response.write('<html><h1>-------------------------------------------------------------------------------</h1>')
                  
                else:
                    continue
         
            if (sentiment <= -2):
                sentiments = "Very Negative"
            elif (sentiment >= -2 and sentiment <= 0):
                sentiments = "Negative"
            elif (sentiment >= 0 and sentiment <= 2):
                sentiments = "Neutral"
            elif (sentiment >= 2 and sentiment <= 5):
                sentiments = "Positive"
            elif (sentiment > 5):
                sentiments = "Very Positive"
            self.response.write('<p>%s  :Sentiment</p>' %  sentiments)
            self.response.write('<html><h1>-------------------------------------------------------------------------------</h1>')
            
        else:
            self.response.write('<p>%s</p>' %display4)
            for tweet in tweets:
                list1 = tweet.display_tweet.lower()
                list2 = re.findall(r'\w+', list1,flags = re.UNICODE | re.LOCALE)
                stopwords = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your', '', ' ', 'http', 'rt', 't', 's', 'co', 'm']
                for list3 in list2:
                    if list3 not in stopwords:
                        buzz_words.append(list3)
            f = open("AFINN-111.txt")
            lines = f.readlines()
            line = [i.split()for i in lines]
            count = Counter(buzz_words)
            for wordss, counterss in count.most_common(10):
                sentiment = 0
                self.response.write('<html><h1>******************************************************************</h1>')
                self.response.write('<p>%s<b>  :BUZZ</b></p>' %  wordss)
                self.response.write('<html><h1>******************************************************************</h1>')
                for tweet in tweets:
                    display_tweet = tweet.display_tweet
                    profile_image_url = tweet.profile_image_url
                    handle = tweet.handle
                    username = tweet.username
                    display_tweet1 = display_tweet.lower()
                    display_tweet2 = re.findall(r'\w+', display_tweet1,flags = re.UNICODE | re.LOCALE)
                    for display_tweet3 in display_tweet2:
                       for linetup in line:
                          if (display_tweet3 == linetup[0] and
                                    len(linetup) == 2):
                             sentiment += int(linetup[1])                          
                          else:
                             continue
                        
                    if wordss in display_tweet2:
                        self.response.write('<p>%s<b>  :Tweet</p></b>' %  display_tweet)
                        self.response.write('<img src =%s></img>' % profile_image_url)
                        self.response.write('<p>%s<b>  :Handle<b/></p>' % handle)
                        self.response.write('<p>%s<b>  :UserName<b/></p>' %  username)
                        self.response.write('<html><h1>-------------------------------------------------------------------------------</h1>')
                      
                    else:
                        continue
             
                if (sentiment <= -2):
                    sentiments = "Very Negative"
                elif (sentiment >= -2 and sentiment <= 0):
                    sentiments = "Negative"
                elif (sentiment >= 0 and sentiment <= 2):
                    sentiments = "Neutral"
                elif (sentiment >= 2 and sentiment <= 5):
                    sentiments = "Positive"
                elif (sentiment > 5):
                    sentiments = "Very Positive"
                self.response.write('<p>%s  :Sentiment</p>' %  sentiments)
                self.response.write('<html><h1>-------------------------------------------------------------------------------</h1>')
            """
            for tweet in tweets:
                #self.response.write('<p>%s<b>  :Sentiments</b></p>' % cgi.escape(tweet.sentiments))
                #self.response.write('<p>%s<b>  :Buzz</b></p>' % cgi.escape(tweet.wordss))	 
                self.response.write('<p>%s<b>  :TweetId</b></p>' % cgi.escape(tweet.tweetID))
                self.response.write('<p>%s<b>  :Handle</b></p>' % cgi.escape(tweet.handle))
                self.response.write('<p>%s<b>  :UserName</b></p>' % cgi.escape(tweet.username))
                self.response.write('<p>%s<b>  :Timeline</b></p>' % cgi.escape(tweet.timeline))
                self.response.write('<p>%s<b>  :Tweet</b></p>' % cgi.escape(tweet.display_tweet))	
                self.response.write('<p>%s</p>' % cgi.escape(tweet.profile_image_url))	
            """
       
        
        # We set the same parent key on the 'Greeting' to ensure each greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
		        
        self.response.write('</body></html>')
        
        '''self.redirect('/')'''
        

        

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
