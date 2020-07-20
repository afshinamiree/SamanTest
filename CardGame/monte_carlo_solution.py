import numpy as np


def calc_stats(suit_count: int, iter_count: int):
	cards = np.repeat(np.arange(suit_count), 13)

	res = np.zeros(iter_count)
	for i in range(iter_count):
		np.random.shuffle(cards)
		point = sum(cards[1:] == cards[:-1])
		res[i] = point

	print('the mean score: ', res.mean())
	print('the standard deviation: ', res.std())
	print('the conditional probability: ', sum(res > 12) / sum(res > 6))


def print_stats():
	iter_num = int(input("please set an integer for number of sample in monte-carlo simulation.\n"))
	print('--------------------------------')
	print('the stats for the case N=26 and M=2 are :')
	calc_stats(2, iter_num)
	print('--------------------------------')

	print('the stats for the case N=52 and M = 4 are :')
	calc_stats(4, iter_num)
	print('--------------------------------')


if __name__ == "__main__":
	print_stats()
