
while True:
    key= input("introduzca la contraseña: ")
    if len(key) >= 8:
        print("contraseña segura")
        break 
    else:
        print("contraseña insegura")
        
    
input("presione enter para salir")