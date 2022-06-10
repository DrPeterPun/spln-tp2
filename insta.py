import instaloader
import re

f = open('comments.txt', 'w+')

# needs to be filled up with credentials
USER = ""
PASSWORD = ""

l = instaloader.Instaloader()
profile = instaloader.Profile.from_username(l.context,
                                            'adidas')
l.login(USER, PASSWORD)
 
posts = profile.get_posts()

for comment in next(posts).get_comments():
    text = re.sub(r'\n', ' ', comment.text)        
    f.write(text + "\n")
    for c in comment.answers:
        text = re.sub(r'\n', ' ', c.text)   
        f.write("   " + text + "\n")