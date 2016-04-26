from election import Election2016

def main():
    election = Election2016()
    election.init()
    election.runRegression()
    print "Finished"

if __name__ == "__main__": main()