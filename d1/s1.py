import sys

def main(filename):
	with open(filename, "r") as fin:
		s = fin.read()
	depths = list(map(int, s.split("\n")[:-1]))
#	for line in s.split("\n")[:-1]:
#		print(line)
#		int(line)
	n = 0
	for i, depth in enumerate(depths[1:]):
		if depth > depths[i]:
			n += 1
	return n

if __name__ == "__main__":
	n = main(sys.argv[1])
	print(n)

