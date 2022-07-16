from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox

root = Tk()
root.title('Card Deck')

root.geometry("1200x800")
root.configure(background="green")

# Stand
def stand():
	global player_total, dealer_total, player_score
	player_total = 0
	dealer_total = 0

	for score in dealer_score:
		dealer_total += score

	for score in player_score:
		player_total += score

	card_button.config(state="disabled")
	stand_button.config(state="disabled")

	if dealer_total >= 17:
		if dealer_total > 21:
			messagebox.showinfo("Player Wins!!", f"Player Wins!  Dealer: {dealer_total}  Player: {player_total}")
		elif dealer_total == player_total:
			messagebox.showinfo("Tie!!", f"It's a Tie!!  Dealer: {dealer_total}  Player: {player_total}")
		elif dealer_total > player_total:
			messagebox.showinfo("Dealer Wins!!", f"Dealer Wins!  Dealer: {dealer_total}  Player: {player_total}")
		else:
			messagebox.showinfo("Player Wins!!", f"Player Wins!  Dealer: {dealer_total}  Player: {player_total}")
	else:
		dealer_hit()
		stand()


def blackjack_shuffle(player):
	global player_total, dealer_total, player_score
	player_total = 0
	dealer_total = 0
	if player == "dealer":
		if len(dealer_score) == 2:
			if dealer_score[0] + dealer_score[1] == 21:
				blackjack_status["dealer"] = "yes"
				

	if player == "player":
		if len(player_score) == 2:
			if player_score[0] + player_score[1] == 21:
				blackjack_status["player"] = "yes"
		else:
			for score in player_score:
				player_total += score
			if player_total == 21:
				blackjack_status["player"] = "yes"
			elif player_total > 21:
				for card_num, card in enumerate(player_score):
					if card == 11:
						player_score[card_num] = 1
						player_total = 0
						for score in player_score:
							player_total += score
						if player_total > 21:
							blackjack_status["player"] = "bust"

				else:
					if player_total == 21:
						blackjack_status["player"] = "yes"
					if player_total > 21:
						blackjack_status["player"] = "bust"



	if len(dealer_score) == 2 and len(player_score) == 2:
		if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
			messagebox.showinfo("Push!", "It's a Tie!")
			card_button.config(state="disabled")
			stand_button.config(state="disabled")
		
		elif blackjack_status["dealer"] == "yes":
			messagebox.showinfo("Dealer Wins!", "Blackjack! Dealer Wins!")
			card_button.config(state="disabled")
			stand_button.config(state="disabled")

		elif blackjack_status["player"] == "yes":
			messagebox.showinfo("Player Wins!", "Blackjack! Player Wins!")
			card_button.config(state="disabled")
			stand_button.config(state="disabled")
	
	else:
		if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
			messagebox.showinfo("Push!", "It's a Tie!")
			card_button.config(state="disabled")
			stand_button.config(state="disabled")
		
		elif blackjack_status["dealer"] == "yes":
			messagebox.showinfo("Dealer Wins!", "21! Dealer Wins!")
			card_button.config(state="disabled")
			stand_button.config(state="disabled")

		elif blackjack_status["player"] == "yes":
			messagebox.showinfo("Player Wins!", "21! Player Wins!")
			card_button.config(state="disabled")
			stand_button.config(state="disabled")

	if blackjack_status["player"] == "bust":
		messagebox.showinfo("Player Busts!", f"Player Loses! {player_total}")
		card_button.config(state="disabled")
		stand_button.config(state="disabled")

# Resize Cards
def resize_cards(card):
	our_card_img = Image.open(card)
	our_card_resize_image = our_card_img.resize((150, 218))
	
	global our_card_image
	our_card_image = ImageTk.PhotoImage(our_card_resize_image)
	return our_card_image

# Shuffle The Cards
def shuffle():
	global blackjack_status, player_total, dealer_total
	player_total = 0
	dealer_total = 0

	blackjack_status = {"dealer":"no", "player":"no"}

	# Enable buttons
	card_button.config(state="normal")
	stand_button.config(state="normal")
	# Clear all the old cards from previous games
	dealer_label_1.config(image='')
	dealer_label_2.config(image='')
	dealer_label_3.config(image='')
	dealer_label_4.config(image='')
	dealer_label_5.config(image='')

	player_label_1.config(image='')
	player_label_2.config(image='')
	player_label_3.config(image='')
	player_label_4.config(image='')
	player_label_5.config(image='')


	# Define Our Deck
	suits = ["diamonds", "clubs", "hearts", "spades"]
	values = [2,3,4,5,6,7,8,9,10, "J","Q","K","A"]
	# 11 = Jack, 12=Queen, 13=King, 14 = Ace

	global deck
	deck =[]

	for suit in suits:
		for value in values:
            
			deck.append(f'{value} of {suit}')


	# Create our players
	global dealer, player, dealer_spot, player_spot, dealer_score, player_score
	dealer = []
	player = []
	dealer_score = []
	player_score = []
	dealer_spot = 0
	player_spot = 0



	# Shuffle Two Cards for player and dealer
	dealer_hit()
	dealer_hit()

	player_hit()
	player_hit()

	# Put number of remaining cards in title bar
	root.title(f'{len(deck)} Cards Left')

def dealer_hit():
	global dealer_spot
	global player_total, dealer_total, player_score

	if dealer_spot <= 5:
		try:
			# Get the player Card
			dealer_card = random.choice(deck)
			# Remove Card From Deck
			deck.remove(dealer_card)
			# Append Card To Dealer List
			dealer.append(dealer_card)
			# Append to dealer score list and convert facecards to 10 or 11
			dcard = int(dealer_card.split("_", 1)[0])
			if dcard == "A":
				dealer_score.append(11)
			elif dcard == "J" or dcard == "Q" or dcard == "K":
				dealer_score.append(10)
			else:
				dealer_score.append(dcard)

			# Output Card To Screen
			global dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5
			
			
			if dealer_spot == 0:
				dealer_image1 = resize_cards(f'images/{dealer_card}.png')
				dealer_label_1.config(image=dealer_image1)
				dealer_spot += 1
			elif dealer_spot == 1:
				dealer_image2 = resize_cards(f'images/{dealer_card}.png')
				dealer_label_2.config(image=dealer_image2)
				dealer_spot += 1
			elif dealer_spot == 2:
				dealer_image3 = resize_cards(f'images/{dealer_card}.png')
				dealer_label_3.config(image=dealer_image3)
				dealer_spot += 1
			elif dealer_spot == 3:
				dealer_image4 = resize_cards(f'images/{dealer_card}.png')
				dealer_label_4.config(image=dealer_image4)
				dealer_spot += 1
			elif dealer_spot == 4:
				dealer_image5 = resize_cards(f'images/{dealer_card}.png')
				dealer_label_5.config(image=dealer_image5)
				dealer_spot += 1
				player_total = 0
				dealer_total = 0

				for score in player_score:
					player_total += score
				for score in dealer_score:
					dealer_total += score
				if dealer_total <= 21:
					card_button.config(state="disabled")
					stand_button.config(state="disabled")
					messagebox.showinfo("Dealer Wins!!", f"Dealer Wins! Dealer:{dealer_total}   Player: {player_total}")

			root.title(f'{len(deck)} Cards Left')

		except:
			root.title(f'No Cards In Deck')

		# Check for blackjack
		blackjack_shuffle("dealer")

def player_hit():
	global player_spot
	global player_total, dealer_total, player_score
	if player_spot <= 5:
		try:
			player_card = random.choice(deck)
			deck.remove(player_card)
			player.append(player_card)
			pcard = (player_card.value.isnumeric())
			if pcard == "A":
				player_score.append(11)
			elif pcard == "J" or pcard == "Q" or pcard == "K":
				player_score.append(10)
			else:
				player_score.append(pcard)
			global player_image1, player_image2, player_image3, player_image4, player_image5
			
			
			if player_spot == 0:
				player_image1 = resize_cards(f'images/{player_card}.png')
				player_label_1.config(image=player_image1)
				player_spot += 1
			elif player_spot == 1:
				player_image2 = resize_cards(f'images/{player_card}.png')
				player_label_2.config(image=player_image2)
				player_spot += 1
			elif player_spot == 2:
				player_image3 = resize_cards(f'images/{player_card}.png')
				player_label_3.config(image=player_image3)
				player_spot += 1
			elif player_spot == 3:
				player_image4 = resize_cards(f'images/{player_card}.png')
				player_label_4.config(image=player_image4)
				player_spot += 1
			elif player_spot == 4:
				player_image5 = resize_cards(f'images/{player_card}.png')
				player_label_5.config(image=player_image5)
				player_spot += 1

				# See if 5 card bust
				# grab our totals
				player_total = 0
				dealer_total = 0
				for score in player_score:
					player_total += score

				for score in dealer_score:
					dealer_total += score

				# Check to see if <= 21
				if player_total <= 21:
					card_button.config(state="disabled")
					stand_button.config(state="disabled")
					messagebox.showinfo("Player Wins!!", f"Player Wins! Dealer:{dealer_total}   Player: {player_total}")
			root.title(f'{len(deck)} Cards Left')

		except:
			root.title(f'No Cards In Deck')


		blackjack_shuffle("player")

def deal_cards():
	try:
		card = random.choice(deck)
		deck.remove(card)
		dealer.append(card)
		global dealer_image
		dealer_image = resize_cards(f'images/{card}.png')
		#dealer_label.config(image=dealer_image)
		#dealer_label.config(text=card)
		card = random.choice(deck)
		deck.remove(card)
		player.append(card)
		global player_image
		player_image = resize_cards(f'images/{card}.png')
		#player_label.config(image=player_image)
		#player_label.config(text=card)


		# Put number of remaining cards in title bar
		root.title(f'{len(deck)} Cards Left')

	except:
		root.title(f'No Cards In Deck')




my_frame = Frame(root, bg="green")
my_frame.pack(pady=5)

# Create Frames For Cards
dealer_frame = LabelFrame(my_frame, text="Dealer", bd=0)
dealer_frame.pack(padx=10, ipadx=20)

player_frame = LabelFrame(my_frame, text="Player", bd=0)
player_frame.pack(ipadx=20, pady=10)

# Put Dealer cards in frames
dealer_label_1 = Label(dealer_frame, text='')
dealer_label_1.grid(row=0, column=0, pady=20, padx=20)

dealer_label_2 = Label(dealer_frame, text='')
dealer_label_2.grid(row=0, column=1, pady=20, padx=20)

dealer_label_3 = Label(dealer_frame, text='')
dealer_label_3.grid(row=0, column=2, pady=20, padx=20)

dealer_label_4 = Label(dealer_frame, text='')
dealer_label_4.grid(row=0, column=3, pady=20, padx=20)

dealer_label_5 = Label(dealer_frame, text='')
dealer_label_5.grid(row=0, column=4, pady=20, padx=20)

# Put Player cards in frames
player_label_1 = Label(player_frame, text='')
player_label_1.grid(row=1, column=0, pady=20, padx=20)

player_label_2 = Label(player_frame, text='')
player_label_2.grid(row=1, column=1, pady=20, padx=20)

player_label_3 = Label(player_frame, text='')
player_label_3.grid(row=1, column=2, pady=20, padx=20)

player_label_4 = Label(player_frame, text='')
player_label_4.grid(row=1, column=3, pady=20, padx=20)

player_label_5 = Label(player_frame, text='')
player_label_5.grid(row=1, column=4, pady=20, padx=20)

# Create Button Frame
button_frame = Frame(root, bg="green")
button_frame.pack(pady=20)

# Create a couple buttons
shuffle_button = Button(button_frame, text="Shuffle Deck", font=("Helvetica", 14), command=shuffle)
shuffle_button.grid(row=0, column=0)

card_button = Button(button_frame, text="Hit Me!", font=("Helvetica", 14), command=player_hit)
card_button.grid(row=0, column=1, padx=10)

stand_button = Button(button_frame, text="Stand!", font=("Helvetica", 14), command=stand)
stand_button.grid(row=0, column=2)



# Shuffle Deck On Start
shuffle()
print(deck)



root.mainloop()