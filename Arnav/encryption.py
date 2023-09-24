# https://medium.com/@domspaulo/python-implementation-of-sha-256-from-scratch-924f660c5d57

H = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a', '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']

K = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4','0xab1c5ed5', '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe','0x9bdc06a7', '0xc19bf174', '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f','0x4a7484aa', '0x5cb0a9dc', '0x76f988da', '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7','0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967', '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc','0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', '0xa2bfe8a1', '0xa81a664b','0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', '0x19a4c116','0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3','0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7','0xc67178f2']



def turn_to_bits(message: str):

    '''
    
    Returns `list` of all bits in `message`
    
    '''

    chars = [i for i in message]
    charnums = [ord(i) for i in chars]
    charbits = [bin(i)[2:].zfill(8) for i in charnums]
    
    bitlist = []
    for i in charbits:
        bitlist += list(map(int, list(i)))

    return bitlist


def turn_to_hex(value: list[int]):
  
  '''
  
  Returns given `value` in hex form
  
  '''

  val = ''.join([str(x) for x in value])
  binaries = []

  for d in range(0, len(val), 4):
    binaries.append('0b' + val[d:d+4])

  hexes = ''
  for b in binaries:
    hexes += hex(int(b ,2))[2:]

  return hexes


def divider(bits: list, l: int = 8):

    '''
    
    divides `bits` into `l` equal parts

    Returns `list`
    
    '''

    L = [bits[i*l:(i+1)*l] for i in range(len(bits)//l)]

    return L


def fillZeros(bits: list[int], length: int = 8, endian: str = 'LE'):

    '''
    
    Fills zeroes in `bits` as per Big and Little `endian`

    Returns `list`
    
    '''

    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else: 
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits

# initialize values from H and K
def val_init(vals: list[str]):

    '''
    
    Initialises predetermined hex values in `vals`

    Returns `list`
    
    '''

    binaries = [bin(int(str(i), 16))[2:] for i in vals]

    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fillZeros(word, 32, 'BE'))
    return words

# pad the message to nearest next multiple of 512 and return list of 512 length chunks
def padder(message: str):

    '''
    
    Returns padded message in hex form
    as per sha256 algorithm
    
    '''

    msgbits = turn_to_bits(message) + [1]
    msglen = len(msgbits)-1

    n = (len(msgbits)//512)+1

    # padding + message = (512*N) - 64
    padding = 512*n - len(msgbits) - 64

    msgbits.extend([0]*padding)
    msgbits.extend(list(map(int,list(bin(msglen)[2:].zfill(64)))))

    return(msgbits)


#truth condition is integer 1
def isTrue(x: int): return x == 1


#simple if 
def if_(i: int, y: int, z: int): return y if isTrue(i) else z


#and - both arguments need to be true
def and_(i: int, j: int): return if_(i, j, 0)
def AND(i: list[int], j: list[int]): return [and_(ia, ja) for ia, ja in zip(i,j)] 


#simply negates argument
def not_(i: int): return if_(i, 0, 1)
def NOT(i: list[int]): return [not_(x) for x in i]


#return true if either i or j is true but not both at the same time
def xor(i: int, j: int): return if_(i, not_(j), j)
def XOR(i: list[int], j: list[int]): return [xor(ia, ja) for ia, ja in zip(i, j)]


#if number of truth values is odd then return true
def xorxor(i: int, j: int, l: int): return xor(i, xor(j, l))
def XORXOR(i: list[int], j: list[int], l: list[int]): return [xorxor(ia, ja, la) for ia, ja, la, in zip(i, j, l)]


#get the majority of results, i.e., if 2 or more of three values are the same 
def maj(i: int, j: int, k: int): return max([i,j], key=[i,j,k].count)


# rotate right
def rotr(x: list[int], n: int): return x[-n:] + x[:-n]
# shift right
def shr(x: list[int], n: int): return n * [0] + x[:-n]


def bin_adder(i: list[int], j: list[int]):
  
  '''
  
  Full binary adder without the final carry-over
  returns `list`
  
  '''

  length = len(i)
  sums = list(range(length))
  c = 0

  for x in range(length-1,-1,-1):

    sums[x] = xorxor(i[x], j[x], c)
    c = maj(i[x], j[x], c)

  return sums


def sha256(message: str):

    '''
    
    Encrypts `message` using SHA256 algorithm
    
    returns hex
    
    '''

    k = val_init(K)
    h0, h1, h2, h3, h4, h5, h6, h7 = val_init(H)

    chunks = divider(padder(message), 512)

    for chunk in chunks:

        w = divider(chunk, 32)
        for _ in range(48):
            w.append(32 * [0])

        for i in range(16, 64):
            s0 = XORXOR(rotr(w[i-15], 7), rotr(w[i-15], 18), shr(w[i-15], 3) ) 
            s1 = XORXOR(rotr(w[i-2], 17), rotr(w[i-2], 19), shr(w[i-2], 10))
            w[i] = bin_adder(bin_adder(bin_adder(w[i-16], s0), w[i-7]), s1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        for j in range(64):
            
            S1 = XORXOR(rotr(e, 6), rotr(e, 11), rotr(e, 25) )
            ch = XOR(AND(e, f), AND(NOT(e), g))
            temp1 = bin_adder(bin_adder(bin_adder(bin_adder(h, S1), ch), k[j]), w[j])

            S0 = XORXOR(rotr(a, 2), rotr(a, 13), rotr(a, 22))
            m = XORXOR(AND(a, b), AND(a, c), AND(b, c))
            temp2 = bin_adder(S0, m)

            h = g
            g = f
            f = e
            e = bin_adder(d, temp1)
            
            d = c
            c = b
            b = a
            a = bin_adder(temp1, temp2)

        h0 = bin_adder(h0, a)
        h1 = bin_adder(h1, b)
        h2 = bin_adder(h2, c)
        h3 = bin_adder(h3, d)
        h4 = bin_adder(h4, e)
        h5 = bin_adder(h5, f)
        h6 = bin_adder(h6, g)
        h7 = bin_adder(h7, h)
    digest = ''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += turn_to_hex(val)

    return digest
