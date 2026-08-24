# encryption 
def encrypt_file(shift1, shift2, input_path, output_path):
    encrypted_content = ""
    with open(input_path, "r") as file:
      content = file.read()
    for char in content :
       if char.islower():
          if "a" <= char <= "n" :
             encrypted_content += chr((((ord(char)-97) + (shift1 * shift2) )% 26)+ 97) 
          else:
             encrypted_content += chr((((ord(char)-97) - (shift1 + shift2) )% 26)+ 97) 

       elif char.isupper():
          if "A" <= char <= "M" :
             encrypted_content += chr((((ord(char)-65) - shift1 )% 26)+ 65)
          else:
             encrypted_content += chr((((ord(char)-65) + (shift2 ** 2 ))% 26)+ 65) 

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
    