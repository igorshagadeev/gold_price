"""
This file generate entries with jewelry parameters
emulating real parsing system for jewelry selling sites

it also contains special developed formula to 
evaluate jewelry price + some error


"""
import random as r

filename = 'data.csv'

# 1m values
MAX_ENTRIES = 10000

def generate(max_entries=MAX_ENTRIES):
    with open(filename, 'w+') as f:
        
        probes = [500, 585, 600, 700]
        
        head_str = 'probe,weight,jew_type,jew_weight,complexity,price\n'
        f.write(head_str)
        for i in range(max_entries):
            #probe
            p = r.choices(probes)[0]
            # weight
            w = r.randint(1,10)
            # jew_type
            jt = r.randint(1,10)
            # jew_weight
            jw = r.randint(1,10)
            # complexity
            c = r.randint(1,5)
            
            #price = (probe*10 + jew_type*jew_weight)*complexity
            #price = (probe*jew_weight*3 + jew_type*jew_weight*5 )*complexity
            #price = round(
                #(probe*weight*0.7 + 1.8**jew_type*1.7**jew_weight )*(complexity - 0.3)**(1.1*complexity) + r.randint(100,500), 2)
            
            price = round(
                (int((p**2/15))*(w) + (jt+2)**2/10*((jw+2)**2/20)*10000)*(1.3)**(c-0.4) + r.randint(1000,3000), 2)
            
            
            gen_str = f'{p},{w},{jt},{jw},{c},{price}\n'
            
            f.write(gen_str)


if __name__ == "__main__":
    generate()
