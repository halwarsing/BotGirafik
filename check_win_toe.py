def list_gets(arr,index):
    out = []
    for i in arr:
        out.append(i[index])
    return out

def list_diagonale_gets(arr,left):
    out = []
    if left:
        c = 0
        for i in arr:
            out.append(i[c])
            c += 1

    else:
        c = len(arr[0]) - 1
        for i in arr:
            out.append(i[c])
            c -= 1
    return out

def check_win_toe(arr):
    out = False
    player = None
    if "".join(arr[0][:3]) == "xxx" or "".join(arr[1][:3]) == "xxx" or "".join(arr[2][:3]) == "xxx" or "".join(list_gets(arr,0)) == "xxx" or "".join(list_gets(arr,1)) == "xxx" or "".join(list_gets(arr,2)) == "xxx" or "".join(list_diagonale_gets(arr,False)) == "xxx" or "".join(list_diagonale_gets(arr,True)) == "xxx":
        out = True
        player = "p1"
    elif "".join(arr[0][:3]) == "yyy" or "".join(arr[1][:3]) == "yyy" or "".join(arr[2][:3]) == "yyy" or "".join(list_gets(arr,0)) == "yyy" or "".join(list_gets(arr,1)) == "yyy" or "".join(list_gets(arr,2)) == "yyy" or "".join(list_diagonale_gets(arr,False)) == "yyy" or "".join(list_diagonale_gets(arr,True)) == "yyy":
        out = True
        player = "p2"
    return (out,player)

arr = [
    ["y","x","x"],
    [" ","x"," "],
    [" "," ","y"]
]

print(check_win_toe(arr))
