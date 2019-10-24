import king_tester as kt



if __name__ == '__main__':
    bestEV = 0
    #home/away is most sensitive to size of data (how far into the season you are)
    bestWeights = [50, 40, 10]
    ev = kt.the_main(bestWeights)
    
    
    

    
    print(ev)