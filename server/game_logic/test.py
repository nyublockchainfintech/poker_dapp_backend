import dealer, client_shuffle

dealer = dealer.Dealer()

alice = client_shuffle.Client('Alice')
bob = client_shuffle.Client('Bob')
charlie = client_shuffle.Client('Charlie')
jane = client_shuffle.Client('Jane')

dealer.add_user(alice)
dealer.add_user(bob)
dealer.add_user(charlie)
dealer.add_user(jane)

print("deck before shuffle:")
dealer.print_deck()
dealer.start_shuffle()
print("\ndeck after shuffle:")
dealer.print_deck()
