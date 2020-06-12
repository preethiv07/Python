import random 
2 import string 
3 
 
4 VOWELS = 'aeiou' 
5 CONSONANTS = 'bcdfghjklmnpqrstvwxyz' 
6 HAND_SIZE = 7 
7 
 
8 SCRABBLE_LETTER_VALUES = { 
9     'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10 
10 } 
11 
 
12 
 
13 WORDLIST_FILENAME = "words.txt" 
14 
 
15 def loadWords(): 
16     """ 
17     Returns a list of valid words. Words are strings of lowercase letters. 
18      
19     Depending on the size of the word list, this function may 
20     take a while to finish. 
21     """ 
22     print ("Loading word list from file...") 
23     # inFile: file 
24     inFile = open(WORDLIST_FILENAME, 'r', 1) 
25     # wordList: list of strings 
26     wordList = [] 
27     for line in inFile: 
28         wordList.append(line.strip().lower()) 
29     print ("  ", len(wordList), "words loaded.") 
30     return wordList 
31 
 
32 def getFrequencyDict(sequence): 
33     """ 
34     Returns a dictionary where the keys are elements of the sequence 
35     and the values are integer counts, for the number of times that 
36     an element is repeated in the sequence. 
37  
38     sequence: string or list 
39     return: dictionary 
40     """ 
41     # freqs: dictionary (element_type -> int) 
42     freq = {} 
43     for x in sequence: 
44         freq[x] = freq.get(x,0) + 1 
45     return freq 
46 
 
47 
 
48 def getWordScore(word, n): 
49     """ 
50     Returns the score for a word. Assumes the word is a valid word. 
51  
52     The score for a word is the sum of the points for letters in the 
53     word, multiplied by the length of the word, PLUS 50 points if all n 
54     letters are used on the first turn. 
55  
56     Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is 
57     worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES) 
58  
59     word: string (lowercase letters) 
60     n: integer (HAND_SIZE; i.e., hand size required for additional points) 
61     returns: int >= 0 
62     """ 
63     length=len(word) 
64     word=word.lower() 
65     score=0 
66     for ch in word: 
67         score+=SCRABBLE_LETTER_VALUES[ch] 
68     score*=length 
69     if(length==n): 
70         score+=50 
71     return score 
72 
 
73 def displayHand(hand): 
74     """ 
75     Displays the letters currently in the hand. 
76  
77     For example: 
78     >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1}) 
79     Should print out something like: 
80        a x x l l l e 
81     The order of the letters is unimportant. 
82  
83     hand: dictionary (string -> int) 
84     """ 
85     for letter in hand.keys(): 
86         for j in range(hand[letter]): 
87              print (letter),              # print all on the same line 
88     print                               # print an empty line 
89 
 
90 
 
91 def dealHand(n): 
92     """ 
93     Returns a random hand containing n lowercase letters. 
94     At least n/3 the letters in the hand should be VOWELS. 
95  
96     Hands are represented as dictionaries. The keys are 
97     letters and the values are the number of times the 
98     particular letter is repeated in that hand. 
99  
100     n: int >= 0 
101     returns: dictionary (string -> int) 
102     """ 
103     hand={} 
104     numVowels = int(n / 3) 
105      
106     for i in range(numVowels): 
107         x = VOWELS[random.randrange(0,len(VOWELS))] 
108         hand[x] = hand.get(x, 0) + 1 
109          
110     for i in range(numVowels, n):     
111         x = CONSONANTS[random.randrange(0,len(CONSONANTS))] 
112         hand[x] = hand.get(x, 0) + 1 
113          
114     return hand 
115 
 
116 
 
117 def updateHand(hand, word): 
118     """ 
119     Assumes that 'hand' has all the letters in word. 
120     In other words, this assumes that however many times 
121     a letter appears in 'word', 'hand' has at least as 
122     many of that letter in it.  
123  
124     Updates the hand: uses up the letters in the given word 
125     and returns the new hand, without those letters in it. 
126  
127     Has no side effects: does not modify hand. 
128  
129     word: string 
130     hand: dictionary (string -> int)     
131     returns: dictionary (string -> int) 
132     """ 
133     hand_copy=dict(hand) 
134     for ch in word: 
135         hand_copy[ch]=hand_copy.get(ch,0)-1 
136         if(hand_copy.get(ch,0)==0): 
137             del hand_copy[ch] 
138     return hand_copy 
139 
 
140 def isValidWord(word, hand, wordList): 
141     """ 
142     Returns True if word is in the wordList and is entirely 
143     composed of letters in the hand. Otherwise, returns False. 
144  
145     Does not mutate hand or wordList. 
146     
147     word: string 
148     hand: dictionary (string -> int) 
149     wordList: list of lowercase strings 
150     """ 
151     wordlist_copy=wordList[:] 
152     hand_copy=hand.copy() 
153     flag=1 
154     if word in wordlist_copy: 
155         for ch in word: 
156             if ch in hand_copy: 
157                 flag=0 
158                 hand_copy[ch]=hand_copy.get(ch,0)-1 
159                 if(hand_copy.get(ch,0)==0): 
160                     del hand_copy[ch] 
161             else: 
162                 flag=1 
163                 break 
164     if (flag==0): 
165         return True 
166     else: 
167         return False 
168 
 
169 
 
170 # 
171 # Problem #4: Playing a hand 
172 # 
173 
 
174 def calculateHandlen(hand): 
175     """  
176     Returns the length (number of letters) in the current hand. 
177      
178     hand: dictionary (string-> int) 
179     returns: integer 
180     """ 
181     count=0 
182     for ch in hand: 
183         if(hand.get(ch,0)>0): 
184             count+=1 
185     return count 
186      
187 
 
188 
 
189 
 
190 def playHand(hand, wordList, n): 
191     """ 
192     Allows the user to play the given hand, as follows: 
193  
194     * The hand is displayed. 
195     * The user may input a word or a single period (the string ".")  
196       to indicate they're done playing 
197     * Invalid words are rejected, and a message is displayed asking 
198       the user to choose another word until they enter a valid word or "." 
199     * When a valid word is entered, it uses up letters from the hand. 
200     * After every valid word: the score for that word is displayed, 
201       the remaining letters in the hand are displayed, and the user 
202       is asked to input another word. 
203     * The sum of the word scores is displayed when the hand finishes. 
204     * The hand finishes when there are no more unused letters or the user 
205       inputs a "." 
206  
207       hand: dictionary (string -> int) 
208       wordList: list of lowercase strings 
209       n: integer (HAND_SIZE; i.e., hand size required for additional points) 
210        
211     """ 
212     # Keep track of the total score 
213     score=0 
214      
215     # As long as there are still letters left in the hand: 
216     while(calculateHandlen(hand)>0): 
217      
218         # Display the hand 
219         print("Current Hand: ",end="") 
220         displayHand(hand) 
221         # Ask user for input 
222         word=input('Enter word, or a "." to indicate that you are finished: ') 
223          
224         # If the input is a single period: 
225         if(word=="."): 
226             # End the game (break out of the loop) 
227             print("Goodbye! Total score: ",score, " points") 
228             break 
229 
 
230              
231         # Otherwise (the input is not a single period): 
232         else: 
233             # If the word is not valid: 
234             if not isValidWord(word,hand,wordList): 
235              
236                 # Reject invalid word (print a message followed by a blank line) 
237                 print("Invalid word, please try again.") 
238                 continue 
239 
 
240             # Otherwise (the word is valid): 
241             else: 
242 
 
243                 # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line 
244                 score1=getWordScore(word,n) # score of each word 
245                 score+=score1 # total score till now 
246                 print('"' +str(word) + '"' + " earned " + str(score1) + " points. Total: " + str(score) + " points.") 
247              
248                 # Update the hand 
249                 hand=updateHand(hand,word) 
250                  
251 
 
252     # Game is over (user entered a '.' or ran out of letters), so tell user the total score 
253     if(calculateHandlen(hand)==0): 
254         print("Run out of letters. Total score: " + str(score) + " points.") 
255 
 
256 
 
257 def playGame(wordList): 
258     """ 
259     Allow the user to play an arbitrary number of hands. 
260  
261     1) Asks the user to input 'n' or 'r' or 'e'. 
262       * If the user inputs 'n', let the user play a new (random) hand. 
263       * If the user inputs 'r', let the user play the last hand again. 
264       * If the user inputs 'e', exit the game. 
265       * If the user inputs anything else, tell them their input was invalid. 
266   
267     2) When done playing the hand, repeat from step 1     
268     """ 
269     hand={} 
270     HAND_SIZE=9 
271     while True: 
272         choice=input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ") 
273         if(choice=='n'): 
274             hand=dealHand(HAND_SIZE) 
275             playHand(hand,wordList,HAND_SIZE) 
276         elif(choice=='r'): 
277             if(hand=={}): 
278                 print("You have not played a hand yet. Please play a new hand first!") 
279             else: 
280                 hand=hand.copy() 
281                 playHand(hand,wordList,HAND_SIZE) 
282         elif(choice=='e'): 
283             break 
284         else: 
285             print("Invalid command.") 
286             continue 
287          
288          
289              
290          
291 
 
292 # 
293 # Build data structures used for entire session and play game 
294 # 
295 if __name__ == '__main__': 
296     wordList = loadWords() 
297     playGame(wordList) 
