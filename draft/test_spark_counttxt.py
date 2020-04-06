#! /bin/python3
import sys
from pyspark import SparkContext



sc = SparkContext()

lines =sc.textFile(sys.argv[1]) #Transfo
words= lines.flatMap(lambda line: line.split(' ')) #Transfo
words_with_1 = words.map(lambda word: (word,1))#Transfo
word_counts = words_with_1.reduceByKey(lambda count1, count2: count1+count2)#Transfo

result = word_counts.collect()#Action !


for (word,count) in result:
    print(word,count)
