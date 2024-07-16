sentence = input("Enter a sentence: ")

words = sentence.split()
print("Even length words in the sentence:")
for even in words:
    if len(even) % 2 == 0:
        print(even, "Sentence is a Even")
    else:
        print(not even, "Not a Even" )