## A WhatsApp Bot for Citizen Journalism in Rural India
I pursued this project at CGNet Swara, in collaboration with **Mircosoft Research** and Voicedeck Technologies, for fulfillment of my thesis (BITS F422) at BITS Pilani, India during spring 2021. I designed, developed and deployed a chat bot to enable low-literate, rural communities of Chattisgrah, India to report and receive journalism reports. Following review by moderators, reports are published on a website and social media sites, and can also be browsed interactively using the WhatsApp bot. The deployed system has shown high acceptance, and is presently in use by the NGO and rural communities. 

- [Paper](https://drive.google.com/file/d/1v0cU2ZyEy1IYrxyX9lQ2sypHaChQp8wQ/view)
- [Thesis Grade](https://drive.google.com/file/d/1yu0-LjbKRSuIYBpHsGMM6F2QRLYOb-C9/view?usp=sharing)
- [Presentation at ACM COMPASS'21](https://youtu.be/t_QsbcMS7Vg?t=717)

### Background
The NGO CGNet Swara provides an interactive voice response (IVR) platform for citizen journalism in remote areas of Chattisgrah, India, unreachable by the mainstream media forces. To use IVR, people give a missed call to a number, whereupon they are called back and can press ‘1’ to report a story and ‘2’ to hear the stories reported by others. These reported stories are taken to a backend content management system where moderators approve or reject these submissions. 

Due to the increased penetration of internet-enabled smartphones, the NGO decided to augment its long existing IVR number with WhatsApp. Therefore, the WhatsApp chat bot has been developed which enables submission of both audio (with or without image) and video reports and stories. This multi-way, intermediated model of communication expands the scope and functionality of typical WhatsApp groups while offering significant cost savings relative to IVR systems.

### Bot Features
The bot is designed with minimal number of steps and without requiring any textual input from users. Users are guided at each step of their interaction journey through an instruction or acknowledgment based reply.

- When a user first starts interaction, bot sends main menu and a link to the most recent story.
- To submit a story, user can direclty send an audio, image or video to the bot.
-	User can share a contact card attachment to receive story submitted by that user. 
-	User can receive local stories by sharing their current location.
-	By typing 1, user gets the message to input a contact number to receive a recent story submitted from that number.
-	By typing 2, user can receive status of their most recent submissions.
-	By typing 3, user can receive a recent random story.

![main_menu_image](https://user-images.githubusercontent.com/39693183/125064245-12e7d480-e0ce-11eb-8e3a-c57dcd2b1d3c.jpg)

![send_stories_status](https://user-images.githubusercontent.com/39693183/125064238-10857a80-e0ce-11eb-9449-5ee9566794de.jpg)

------
#### Online Resources
- [PhP basics](https://www.smashingmagazine.com/2010/04/php-what-you-need-to-know-to-play-with-the-web/)
- [PhP variables scope](http://cs.ucf.edu/~mikel/Telescopes/scope.htm)
- [HTTP POST request](https://reqbin.com/Article/HttpPost)
- [Apache Web server](https://www.hostinger.in/tutorials/what-is-apache)
