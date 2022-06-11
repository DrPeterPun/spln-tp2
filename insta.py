import instaloader
import re
import os
import shutil

def get_info(username, password, account, n):

    if not os.path.isdir("out"):
        os.mkdir("out")
    else:
        shutil.rmtree("out")
        os.mkdir("out")

    f = open('out/comments.txt', 'w+')

    l = instaloader.Instaloader(dirname_pattern='out/'+account)
    profile = instaloader.Profile.from_username(l.context,
                                                account)
    l.login(username, password)
 
    posts = profile.get_posts()

    while n>0:
        next(posts)
        n-= 1

    post = next(posts)

    '''
    if os.path.isdir(username):
        shutil.rmtree(username)'''

    l.download_post(post, username)
    likes = post.likes

    comments=0

    for comment in post.get_comments():
        text = re.sub(r'\n', ' ', comment.text)        
        f.write(text + "\n")
        for c in comment.answers:
            text = re.sub(r'\n', ' ', c.text)   
            f.write("   " + text + "\n")
            comments+= 1
        comments+=1
    
    f.close()

    return likes, comments