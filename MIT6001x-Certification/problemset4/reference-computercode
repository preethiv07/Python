def playGame(wordList): 
192     """ 
193     Allow the user to play an arbitrary number of hands. 
194   
195     1) Asks the user to input 'n' or 'r' or 'e'. 
196         * If the user inputs 'e', immediately exit the game. 
197         * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again. 
198  
199     2) Asks the user to input a 'u' or a 'c'. 
200         * If the user inputs anything that's not 'c' or 'u', keep asking them again. 
201  
202     3) Switch functionality based on the above choices: 
203         * If the user inputted 'n', play a new (random) hand. 
204         * Else, if the user inputted 'r', play the last hand again. 
205        
206         * If the user inputted 'u', let the user play the game 
207           with the selected hand, using playHand. 
208         * If the user inputted 'c', let the computer play the  
209           game with the selected hand, using compPlayHand. 
210  
211     4) After the computer or user has played the hand, repeat from step 1 
212  
213     wordList: list (string) 
214     """ 
215     # initialize empty hand 
216     hand = {} 
217        
218     while True: 
219          
220         # initialize variable for game_choice 
221         game_choice = str(raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')) 
222          
223         # if player chooses to exit, break the loop 
224         if game_choice == 'e': 
225             break 
226           
227         # if player chooses to replay but hand is empty, print error message 
228         elif game_choice == 'r': 
229             if hand == {}: 
230                 print 'You have not played a hand yet. Please play a new hand first!' 
231             else: 
232                 # if hand is not empty, prompt for player choice of user or computer 
233                 player_choice = str(raw_input('Enter u to have yourself play, c to have the computer play: ')) 
234                 # if player chooses to play, initiate playHand 
235                 if player_choice == 'u': 
236                     playHand(hand, wordList, HAND_SIZE) 
237              
238                 # if player chooses computer to play, initiate compPlayHand 
239                 elif player_choice == 'c': 
240                     compPlayHand(hand, wordList, HAND_SIZE) 
241                  
242                 # if player chooses another other input, print error message 
243                 else: 
244                     print 'Invalid command.'   
245                        
246         # if player chooses to play new game or replay old hand, ask for player 
247         # choice of either user or computer 
248         elif game_choice == 'n': 
249             player_choice = str(raw_input('Enter u to have yourself play, c to have the computer play: '))             
250             hand = dealHand(HAND_SIZE) 
251              
252             # if player chooses to play, initiate playHand 
253             if player_choice == 'u': 
254                 playHand(hand, wordList, HAND_SIZE) 
255              
256             # if players chooses computer to play, initiate compPlayHand 
257             elif player_choice == 'c': 
258                 compPlayHand(hand, wordList, HAND_SIZE) 
259              
260             # if player chooses another other input, print error message 
261             #else: 
262                 print 'Invalid command.' 
263                  
264         # if any other input, print error message 
265         else: 
266             print 'Invalid command.'  
