

if __name__ == '__main__':
    #iterator
    mylist = [x for x in range(10)]
    for i in mylist:
        print(i)


    #generator (data are created on fly (not stored))
    mylist = (x for x in range(10))
    for i in mylist:
        print(i)


    def genMultby2():
        mylist = range(4)
        for i in mylist:
            yield i*2

    print("")
    mygen = genMultby2()
    for i in mygen:
        print("-----")
        print(i)
