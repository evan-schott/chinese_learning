#!/usr/bin/env python3

import pinyin 
import pinyin.cedict
import random
import os




'''
Notes: (7/14/2020)
- Require "new_character_archive.txt" file with comma space list of characters to learn. 
- Mistakes can be corrected by opening "character_learning.txt" file
- This was before I knew about pickle, but still works fine
'''



# Accepts triplets of the form: [(chinese character), (days until review again), (got right or nah)]
def display_cluster(triplet_list, characters, show_unmastered):
    print_screen()
    random.shuffle(triplet_list)
    length = len(triplet_list)
    for i in range(0,length):
        if triplet_list[i][1] != '0':
            continue
        elif show_unmastered == True:
            if triplet_list[i][2] == 'yes':
                continue
            else:
                if characters == True:
                    print("toggle option: {}, inside cluster".format(show_unmastered))
                    print(triplet_list[i][0],end="  ")
                else:
                    print(pinyin.get(triplet_list[i][0]),end="  ")  
        else:
            if characters == True:
                print(triplet_list[i][0],end="  ")
            else:
                print(pinyin.get(triplet_list[i][0]),end="  ")
    print("\n\n\n\n\n")
            
# Save lines of code
def wait_til_get_answer(message, **kwargs):
    while True:
        answer = input(message + "\n")
        if answer in list(kwargs.values()):
            return answer

def make_list(element):
    a = []
    a.append(element)
    return a

# take in triplet and insert in list of triplets based on ascii value of second triplet component
def insert_in_list(triplet_list,new_element):
    if len(triplet_list) == 0:
        return make_list(new_element)
    else:
        if triplet_list[0][1] >= new_element[1]:
            triplet_list.reverse()
            triplet_list.append(new_element)
            triplet_list.reverse()
            return triplet_list
        else:
            return make_list(triplet_list[0]) + insert_in_list(triplet_list[1:],new_element)

# expect triplets : word = [(chinese), (pinyin), (english)]
def dictionary_print(word):
    print("\n{} : {} : ".format(word[0],word[1]), end = "")
    if word[2] is not None:
        length = len(word[2])
        for i in range(0, length):
            if (i != 0):
                print(",",end =" ")
            print(word[2][i], end = "")
                
# spacing effect shift value to maximize memory retention
def calculate_new_character(word):
    if word[1] == '0':
        days = '1'
    elif word[1] == '1':
        days = '3'
    elif word[1] == '3':
        days = '7'
    elif word[1] == '7':
        days = '14'
    elif word[1] == '14':
        days = '28'
    elif word [1] == '28':
        days = '100'
    else:
        days = '0'
    final = word[0] + days
    print(final)
    return final

def calculate_new_time(word):
    print(word)
    if word[1] == '0':
        days = '1'
    elif word[1] == '1':
        days = '3'
    elif word[1] == '3':
        days = '7'
    elif word[1] == '7':
        days = '14'
    elif word[1] == '14':
        days = '28'
    elif word [1] == '28':
        days = '100'
    else:
        days = '0'
        
    return int(days)


def remove_junk_from_list(list_with_junk):
    junk_free_list = []
    for element in list_with_junk:
        if element != '':
            junk_free_list.append(element)
    return junk_free_list

def print_screen():
    for _ in range(0,30):
        print("\n")
        
def extract_new_characters(char_num):
    
    if char_num == 0:
        return []
    
    # Extract characters from file
    with open('new_character_archive.txt',mode='r') as myfile:
        contents = myfile.read()
        char_list = contents.split("，")
        length = len(char_list)
        if length < char_num:
            print("Sorry, not enough characters in archive, your typed quanity will be adjusted")
            char_num = length
        extracted_chars = char_list[0:char_num]
        new_char_archive = char_list[char_num:]
        if len(new_char_archive) == 0:
            print("Nothing left in character archive")
        
        # print(extracted_chars)
        myfile.close()

    # Remove the characters extracted from the file   
    os.remove("new_character_archive.txt")
    with open('new_character_archive.txt',mode='w') as myfile:
        length = len(new_char_archive)
        counter = 1
        for character in new_char_archive:
            myfile.write(character)
            if counter != length:
                myfile.write('，')
            counter += 1
        myfile.close()
        
    return extracted_chars
    

# How many characters to study today
is_num = False
while is_num == False:
    str_char_num = input("How many characters you wanna learn today?\n")
    is_num = str_char_num.isnumeric()
    
char_num = int(str_char_num)
extracted_chars = extract_new_characters(char_num) # Will return empty list if input is 0


        

with open('character_learning.txt',mode='r') as myfile:
    contents = myfile.read()
    day_list = contents.split("\n")
    #rint(day_list)
    day_triplet_list = []
    
    # Convert the characters to be tested today into a list of triplets 
    if len(day_list) != 0:
        if day_list[0] != '':
            
            # Split using regular expressions
            import re
            nums = remove_junk_from_list(re.split("[^\d]", day_list[0]))
            chars = remove_junk_from_list(re.split("[\d]", day_list[0]))
            
            if (len(nums) != len(chars)):
                print("error: number of characters and number of time intervals are not equal")
            
            length = len(nums)
            for i in range(0,length):
                day_triplet_list.append([chars[i]])
                day_triplet_list[i].append(nums[i])
                day_triplet_list[i].append("no")
            
            
            
    # Append the extracted characters to this list (to prevent accidental log off)
    for character in extracted_chars:
        day_triplet_list.append([character,'0','no'])
        
        
    # Create practice list 
    practice_list = []
    for triplet in day_triplet_list:
        if triplet[1] == '0':

            practice_list = insert_in_list(practice_list,[triplet[0],pinyin.get(triplet[0]), pinyin.cedict.translate_word(triplet[0])])

            
    
    # Ask user what they want to do (1 = practice new characters, 2 = test old characters, 3 = move on to next day)
    while True:
        compatible_answer = False
        while compatible_answer == False:
            what_do_next = input("\n\nType [1] to practice new characters for today. Type [2] to test yourself for the other characters of today. Type [3] to move on to the next day.\n")
            if what_do_next == '1' or what_do_next == '2' or what_do_next == '3':
                compatible_answer = True
        
        # Rewrite the file, and move on to next day
        if what_do_next == '3':
            print_screen()
            for word in day_triplet_list:
                length = len(day_list)
                if (word[2] == 'no'):
                    word[1] = '0'
                    
                placement = calculate_new_time(word)
                if placement > length - 1:
                    for _ in range(0,placement - length):
                        day_list.append('')
                    # print("{} long length".format(word))
                    day_list.append(calculate_new_character(word))
                else:
                    old_string = day_list[placement]
                    new_string = old_string + word[0] + str(placement)#calculate_new_character(word)
                    day_list[placement] = new_string
                    # print(day_list)
            myfile.close()
            os.remove('character_learning.txt')
            with open('character_learning.txt',mode='w') as myfile:
                length = len(day_list)
                for i in range(1, length):
                    myfile.write(day_list[i])
                    myfile.write("\n")
                myfile.close()
                exit(0)
                
        
            # Save [1:]
            # Delete file, make new file put [1:] in new file 
                
        # Test self before moving on to the next day      
        if what_do_next == '2':
            print_screen()
            while True: 
                compatible_answer = False
                while compatible_answer == False:
                    what_do_next = input("\n\nType [1] to test characters. Type [2] to test pinyin. Type [3] to test english. Type [4] to go back.\n")
                    if what_do_next == '1' or what_do_next == '2' or what_do_next == '3' or what_do_next == '4':
                        compatible_answer = True
                
                # To go back
                if what_do_next == '4':
                    print_screen()
                    break
                
                else:
                    print_screen()
                    random.shuffle(day_triplet_list)
                    
                    length = len(day_triplet_list)
                    for i in range(0,length):
                        print_screen()
                        if day_triplet_list[i][1] == '0':
                            continue
                        elif what_do_next == '1':
                            print(day_triplet_list[i][0])
                            print("\n\n\n\n\n")
                        elif what_do_next == '2':
                            print(pinyin.get(day_triplet_list[i][0]))
                            print("\n\n\n\n\n")

                        else:
                            placeholder = pinyin.cedict.translate_word(day_triplet_list[i][0])          
                            if placeholder is not None:
                                length = len(placeholder)
                                for i in range(0,length):
                                    print(placeholder[i],end="")
                                    if i != length - 1:
                                       print(", ", end = "")
                        
                        while True:
                            compatible_answer = False
                            while compatible_answer == False:
                                next_one = input("\n\n[1] I know [2] I don't know [3] Look at dictionary definition [4] Look at radical composition [5] Example sentence\n")
                                if next_one == '1' or next_one == '2' or next_one == '3':
                                    compatible_answer = True
                            if next_one == '1':
                                day_triplet_list[i][2] = 'yes'
                                break
                            elif next_one == '2':
                                day_triplet_list[i][2] = 'no'
                                break
                            else:
                                print("\n{} : {} : ".format(day_triplet_list[i][0], pinyin.get(day_triplet_list[i][0])), end = "")
                                placeholder = pinyin.cedict.translate_word(day_triplet_list[i][0])          
                                if placeholder is not None:
                                    length = len(placeholder)
                                    for i in range(0,length):
                                        print(placeholder[i],end="")
                                        if i != length - 1:
                                           print(", ", end = "") 

                   
            
        
        # Practice mode for new characters
        if what_do_next == '1':
            print_screen()
            while True:
                compatible_answer = False
                while compatible_answer == False:
                    what_do_next = input("\n\nType [1] to go back. Type [2] to show dictionary. Type [3] to do cluster studying. Type [3] to practice showing characters. Type [4] to practice showing pinyin. Type [5] to practice showing english.\n")
                    if what_do_next == '1' or what_do_next == '2' or what_do_next == '3' or what_do_next == '4' or what_do_next == '5':
                        compatible_answer = True
            
                # Go back
                if what_do_next == '1':
                    print_screen()
                    break
                
                # Show dictionary
                elif what_do_next == '2':
                    print_screen()
                    for word in practice_list:
                        dictionary_print(word)
                    print("\n\n\n\n\n")
                    
                
                elif what_do_next == '3':
                    print_screen()
                    only_show_unmastered = False
                    while True:
                        choice = ""
                        if only_show_unmastered:
                            choice = wait_til_get_answer("[1] To go back [2] To display character cluster [3] To display pinyin cluster [4] To display english cluster [5] To display only the words you don't know when practicing",a="1",b="2",c="3",d="4",e="5")
                        else:
                            choice = wait_til_get_answer("[1] To go back [2] To display character cluster [3] To display pinyin cluster [4] To display english cluster [5] To display all words when practicing",a="1",b="2",c="3",d="4",e="5")
                            
                        if choice == '1':
                            print_screen()
                            break
                        elif choice == '2':
                            print(day_triplet_list)
                            print("inside caller function")
                            display_cluster(day_triplet_list, True, only_show_unmastered)
                        elif choice == '3':
                            display_cluster(day_triplet_list, False, only_show_unmastered)
                        elif choice == '4':
                            print_screen()
                            random.shuffle(practice_list)
                            length = len(practice_list)
                            for i in range(0,length):
                                if practice_list[i][2] is not None:
                                    print(practice_list[i][2][0], end="")
                                    if (i != length - 1):
                                        print(" | ", end = "")
                                    else:
                                        print("\n\n\n\n")
                        elif choice == '5':
                            if only_show_unmastered == True:
                                only_show_unmastered == False
                            else:
                                only_show_unmastered == True
                            print_screen()
                        
                            
        
                # Practice Characters
                if what_do_next == '3':
                    print_screen()
                    random.shuffle(practice_list)
                    length = len(practice_list)
                    for i in range(0,length):
                        print(practice_list[i][0], end="")
                        if (i != length - 1):
                            print(", ", end = "")
                        else:
                            print("\n\n\n\n")
                            
                # Practice Pinyin
                if what_do_next == '4':
                    print_screen()
                    random.shuffle(practice_list)
                    length = len(practice_list)
                    for i in range(0,length):
                        print(practice_list[i][1], end="")
                        if (i != length - 1):
                            print(", ", end = "")
                        else:
                            print("\n\n\n\n")
                            
                            
                # Practice english
                if what_do_next == '5':
                    print_screen()
                    random.shuffle(practice_list)
                    length = len(practice_list)
                    for i in range(0,length):
                        if practice_list[i][2] is not None:
                            print(practice_list[i][2][0], end="")
                            if (i != length - 1):
                                print(", ", end = "")
                            else:
                                print("\n\n\n\n")
                    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
