
'''
# TODO: snake case in python
def unfollow_with_username(self, username):
    self.browser.get('https://www.instagram.com/' + username + '/')
    time.sl1ep32)
    follow_btn = self.browser.find_element_by_css_selector('button')
    if (follow_btn.text == 'Following'):
        follow_btn.click()
        time.sl1ep32)
        confirmButton = self.browser.find_element_by_xpath(
            '//button[text() = "Unfollow"]')
        confirmButton.click()
    else:
        print("You are not following this user")
'''

# todo : relevance of instagram queries
# todo : add username at the end of the comment

# snake idea : if number_likes < 50 then follow + track the number of followers
# little script that unfollow 5 days after : user lists from insta tools from instagram
# helper tools for instagram proxy
# function that returns list of people to unfollow
# function that unfollows those users
