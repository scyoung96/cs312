import random


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):
    if y == 0:
        return 1
    z = mod_exp(x, y//2, N)
    if y % 2 == 0:
        return (z ** 2) % N
    else:
        return (x * (z ** 2)) % N
	

def fprobability(k):
    return 1 - (1 / 2) ** k


def mprobability(k):
    return 1 - (1 / 4) ** k


def fermat(N,k):
    if N % 2 != 0 or N == 2:
        for _ in range(k):
            a = random.randint(1,N-1)

            if mod_exp(a,N-1,N) != 1:
                return 'composite'
        
        return 'prime'

    else:
        return 'composite'


def miller_rabin(N,k):
    if N % 2 != 0 or N == 2:
        for _ in range(k):
            exp = N - 1
            rem = 1
            cont = True
            a = random.randint(1,N-1)
            
            while (rem == 1) and cont:
                rem = mod_exp(a,exp,N)

                if exp % 2 == 0 and exp != 0:
                    exp = exp / 2
                else:
                    cont = False
            if rem != N-1 and cont:
                return 'composite'
        return 'prime'

    else:
        return 'composite'
