import sys

def main(filename):
	with open(filename, "r") as fin:
		s = fin.read()
	depths = list(map(int, s.split("\n")[:-1]))
	n = 0
	s = sum(depths[:3])
	for i, depth in enumerate(depths[3:]):
		#print(s)
		if s - depths[i] + depth > s:
			n += 1
			#print(i)
		s = s - depths[i] + depth
	return n

if __name__ == "__main__":
	n = main(sys.argv[1])
	print(n)

