import lexico

def isExist(text):
    try: 
        globals()[text]
        return True
    except:
        return False

if __name__ == '__main__':
    
    while True:
        text = input('shell > ')  
        tokens, error = lexico.run('<stdin>', text)

        # Comando para salir de la consola
        if text == '\c':
            break
        
        # Si el texto ingresado es una variable previamente guarda se manda a llamar
        elif isExist(text):
            print("\t", globals()[text])
        
        else:
            # Imprime el error en caso de que haya encontrado uno
            if error:
                print(error.ToString())
            else:
                expression = lexico.make_identifier(text)
                if expression != None:
                    # De haber hecho la declaracion de una variable se añade al entorno junto con su valor
                    globals()[(tokens[0].Value())] = expression
                # Imprime los tokens encontrados con sus respectivos valores
                print("\tTOKENS->", tokens)