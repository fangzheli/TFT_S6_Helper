# TFT_S6_Helper
League of Legends TFT Helper for Season 6<br />
Teamfight Tactics (TFT) is an auto battler game based on the universe of League of Legends (LOL). You are supposed to choose champions from a store to fight against other 7 players. Synergy system is the most essential system in an auto battler game. Each champion in TFT has at least one, at most three traits with them. With the synergy, different drafts can have extra abilities. However, there are 28 types of traits there, so it is very hard for rookie like me to remember. An idea to help with this situation is that people put in the champions they have for now and a helper program gives some suggestions on the potential draft I can build based on both the win rate and my current draft. To simplify the question, we will not take the action of other players into consideration because in most case, the action of other players will only affect the level of your champions instead of the draft of your team. Also, hextech augments are not considered because most of them only affect the intensity of your team instead of the draft of your team. Here are some sample screenshots for the data source.

How to use it<br />
Link to the repo: https://github.com/fangzheli/TFT_S6_Helper/<br />
The default homepage for TFT helper is http://127.0.0.1:5000/helper<br />
Two functions get_champions() and get_traits_rank() are used to get the dynamic websites by selenium. Two functions clean_champions_synergy() and clean_traits_rank() are used to process the two htmls mentioned above to json. These four functions only need to be runned when there is a need to update or rescrap the page. When running the flask, there is no need for running these functions so I have commented out these functions in the main functions.
Required packages are requests, flask, bs4 and selenium.

Data Source<br />
All the data I need is the whole list of champions and their traits, the whole list of traits and their effects and the win rate for different drafts. The whole list of champions and their traits can be got by scraping https://tftactics.gg/db/champions. The win rate for different drafts can be scraped from https://tftactics.gg/meta-report. I check the robots.txt file of this website and I am allowed to scrap anything.
Selenium are used to load the dynamic pages and downloads two html files. Then I clean it up by using clean_champions_synergy() and clean_traits_rank() to make it into JSON files. Also, some images are downloaded by using cache to put in static/imgs.
There are 58 records for champions and 95 records for the win rates of traits. For champions, each champion has the name, icon image, class, origin and cost. For traits, each trait has trait name, average place, win rate, top 4 rate and popularity.
    
Data Access and Storage<br />
I use selenium to get the page I want because this website use JavaScript to load the pages, so I use Selenium and pause for a few second and get the html file. Then I use beautifulsoup to parse it and it works well.
 
Data Processing<br />
A binary search tree for different traits with their win rates. After the user inputs the champions that they have currently, the helper will check the traits and search it in the binary search tree to get its win rate.

Data Presentation<br />
A Flask app is created to demonstrate the content.

The known problem<br />
1. When people don't click any champions but clicking "get recommendation", they may get a very simple page to tell them there is not enough champions clicked.<br />
2. When too many champions are chosen, it will take a very long time to go through every combination of comps.

Future Work<br />
1. improve the recommendation algorithm<br />
2. add and beautify flask page<br />

![image](https://user-images.githubusercontent.com/48412604/146498622-3240377d-293f-49ec-b385-12d2344fc45d.png)
![image](https://user-images.githubusercontent.com/48412604/146498693-a32437a5-339b-4479-900b-a0cfd3c7e6cf.png)
