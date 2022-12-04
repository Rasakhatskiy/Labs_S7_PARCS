import random

n=160000
with open('input-160k.txt', 'w') as fp:
  for i in range(n):
    fp.write("%s " % random.randint(0,100000))
        
  print('Done')