# chinese_learning
Command line tool to help save time learning Chinese vocabulary

# About
Frustrated with how long it took me to build flashcard decks on Quizlet/Anki for studying Chinese, I made a python command line script where the user enters the characters to memorize, and then they are automatically translated into English/Chinese Pinyin to save time. Also included spaced repetition to maximize retention.

# Increased Efficiency 
For an input of "和谐，气氛，投资，股票，下载，逃犯，色鬼，警告，品牌，挑战，贸易战，经济，发展" into the new_character_archive.txt, the following dictionary is produced thanks to an MIT translator. 

![](https://github.com/evan-schott/chinese_learning/blob/master/auto_translate.png)

This reduces friction, as it is often so frustrating having to click so many buttons to make decks of flashcards in anki or quizlet. With this all you have to do is type the chinese characters to memorize for the day in a list, as opposed to having to also type in the english definition and pinyin. 

# Screenshots
![](https://github.com/evan-schott/chinese_learning/blob/master/interface.png)

The interface is nothing fancy, but promotes extreme speed of creation, and self testing. I found that testing myself was most effective when the words were layed out in a random order. No button clicking, just reading down the line. For those who prefer seeing one at a time, that option is also included.

![](https://github.com/evan-schott/chinese_learning/blob/master/character_cluster.png)
![](https://github.com/evan-schott/chinese_learning/blob/master/pinyin_cluster.png)
![](https://github.com/evan-schott/chinese_learning/blob/master/english_cluster.png)




# notes
- Require "new_character_archive.txt" file with comma space list of characters to learn. 
- Mistakes can be corrected by opening "character_learning.txt" file
- This was before I knew about pickle, but still works fine

