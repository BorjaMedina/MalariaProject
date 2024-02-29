import sys

try:
    genomefile = sys.argv[1]
    scaffolds = sys.argv[2]
    output = sys.argv[3]

except:
    print("Run program like: cleaningScaffolds.py species.genome scaffolds.txt output.fasta")
    sys.exit()


with open(scaffolds, "r") as T1, open(genomefile) as genome:
    sequences=genome.readlines()
    birds=T1.readlines()
l=[]
ll=[]
for line in birds:
#    print(line)
    for z in range(0,len(sequences)):
        x=sequences[z].find(line.strip())
        if x>0:
            l.append(z)
for x in l:
      ll.append(x)
      ll.append(x+1) 

for n in sorted(ll, reverse=True):
    del sequences[n]

with open (output, "w") as newOut:
    newOut.writelines(sequences)
