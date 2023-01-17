welcome_msg = "\n\t-*_*-  Welcome to HackerNews Crawler v0.1.0\n"
help_msg = "=> most likely you see this message because you didn't provide any argument to the program. I will guide you to interactive mode where you can set your preferences for the data you need most. enter 'h' to get help on the programs arguments or 'q' to quit the program. enjoy!"
startup_msg = "\nAre you ready?! cause we are going for a ride baby   😁 🏎\nseriously though, now I will ask for some of your preference, then based on your inputs I will start crawling the good old HackerNews website and get the most relevant data.\n\t#NOTE: the only mandatory one is the headline (topic), others are optional and can be left blank.\n\t#NOTE: it's recommended not to use more than 2 limiters in your searches. if search came empty try to loosen the search rang, and check your word-casing..."
topic_msg = (
    "\n1. enter a topic you seek most: (try to be concise and not too specific.)\n>> "
)
poster_msg = "\n2. enter the name of your favorite poster or tech company on hacker news:\n(only use this factor if you exactly know whose posts you wanna target)\n>> "
time_msg = "\n3. enter a specific date delimited by `-` (e.g. YYYY-MM-dd):\n(leave blank for the goodies sorted descending from fresh ones)\n>> "
votes_msg = "\n4. enter the minimum number of votes for a post to be displayed:\n>> "
comments_msg = (
    "\n5. enter the minimum number of comments for a post to be displayed:\n>> "
)
prompt_msg = "\nChoose an option that you want to filter your search with: (just enter number)\n1. post topic   -*-   2. poster   -*-   3. post date   -*-   4. number of votes [RECOMMENDED]   -*-   5. number of comments\n>> "
prompt_msgs = (topic_msg, poster_msg, time_msg, votes_msg, comments_msg)

post_number_msg = "\nI almost forgot, how many messages do you need me to retrieve from HackerNews (with all filtering above applied):\n>> "
