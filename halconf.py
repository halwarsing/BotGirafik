import sys
text = open(sys.argv[1],"r").split(";")
info = {}
for i in text:
    args = i.split("=")
    info[args[0]] = args[1]

def save():
    global info
    out = ""
    
    for k,v in info.items():
        out += k+"="+v+";"

    out = out[:-1]
    return out

print(save())
