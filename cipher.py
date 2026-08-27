# encryption 
def encrypt_file(shift1, shift2, input_path, output_path):
    encrypted_content = ""
    with open(input_path, "r") as file:
      content = file.read()
    for char in content :
       if char.islower():
          if "a" <= char <= "n" :
             encrypted_content += chr((((ord(char)-97) + (shift1 * shift2) )% 14)+ 97) 
          else:
             encrypted_content += chr((((ord(char)-111) - (shift1 + shift2) )% 12)+ 111) 

       elif char.isupper():
          if "A" <= char <= "M" :
             encrypted_content += chr((((ord(char)-65) - shift1 )% 13)+ 65)
          else:
             encrypted_content += chr((((ord(char)-78) + (shift2 ** 2 ))% 13)+ 78) 

       elif char.isdigit():
           encrypted_content += chr((((ord(char)-48) + (shift1 - shift2 ))% 10)+ 48) 
       else: 
          encrypted_content += char

    with open(output_path,"w") as file :
          file.write(encrypted_content)
                 
# decryption

def decrypt_file(shift1, shift2, input_path, output_path):
    decrypted_content = ""
    with open(input_path, "r") as file:
      content = file.read()
    for char in content :
           if char.islower():
              if "a" <= char <= "n" :
                 decrypted_content += chr((((ord(char)-97) - (shift1 * shift2) )% 14)+ 97) 
              else:
                 decrypted_content += chr((((ord(char)-111) + (shift1 + shift2) )% 12)+ 111) 
    
           elif char.isupper():
              if "A" <= char <= "M" :
                 decrypted_content += chr((((ord(char)-65) + shift1 )% 13)+ 65)
              else:
                 decrypted_content += chr((((ord(char)-78) - (shift2 ** 2 ))% 13)+ 78) 
    
           elif char.isdigit():
               decrypted_content += chr((((ord(char)-48) - (shift1 - shift2 ))% 10)+ 48) 
           else: 
              decrypted_content += char
    with open(output_path, "w") as file:
     file.write(decrypted_content)



