import argparse
import RDT
import time


#Return Pig Latin version of a given word
def makePigLatin(word):
    m  = len(word)
    vowels = "a", "e", "i", "o", "u", "y" 
    if m<3 or word=="the":
        return word
    else:
        for i in vowels:
            if word.find(i) < m and word.find(i) != -1:
                m = word.find(i)
        if m==0:
            return word+"way" 
        else:
            return word[m:]+word[:m]+"ay" 


#Return Pig Latin version of a sentence string
def piglatinize(message):
    essagemay = ""
    message = message.strip(".")
    for word in message.split(' '):
        essagemay += " "+makePigLatin(word)
    return essagemay.strip()+"."


#Server begins here
if __name__ == '__main__':
    parser =  argparse.ArgumentParser(description='Pig Latin conversion server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()
    
    timeout = 15 #close connection if no new data within 15 seconds
    time_of_last_data = time.time()
    
    #Listen for requests, pig-latinize, and respond
    rdt = RDT.RDT('server', None, args.port)
    while(True):
        #try to receive message before timeout
        msg_S = rdt.rdt_1_0_receive()
        if msg_S is None:
            if time_of_last_data + timeout < time.time():
                break
            else:
                continue
        time_of_last_data = time.time()
        
        #convert and reply
        rep_msg_S = piglatinize(msg_S)
        print('Converted %s \nto \n%s\n' % (msg_S, rep_msg_S))
        rdt.rdt_1_0_send(rep_msg_S)
        
    print 'Server timed out.  Attempts to reach me now will result in Errno 32 Broken Pipe!'
    rdt.disconnect()
