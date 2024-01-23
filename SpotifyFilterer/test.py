def keep_asking():
    lock = True
    while(lock):
        try:
            a = int(input('enter num'))
            b = int(input('enter num'))
            print(a/b) #true risk
            lock = False
        except:
            print('do it again')
            lock = True