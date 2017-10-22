anagram = sorted(input('What are your letters?'))


def word_checker():
	for letters in range(9,4,-1):
		words = words_with_that_amount_of(letters)
        for word in words:
            if sorted(word) == anagram:
            return word
            for letter in anagram:
                new = anagram.remove(letter)
                
