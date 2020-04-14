from typing import Dict, List 

#=====================================
# Data
#=====================================
file_path: str = 'C:\\Games\\Ultima_5\\SAVED.GAM'

characters = ['avatar', 'shamino', 'iolo', 'mariah', 'geoffrey', 'jaana', 
			'julia', 'dupre', 'katrina', 'sentri', 'gwenno', 'johne', 
			'gorn', 'maxwell', 'toshi', 'saduj']

equipment = ['keys', 'skull keys', 'gems', 'black badge', 'magic carpets', 'magic axes', 'gold']

stats = ['strength', 'intelligence', 'dexterity', 'magic', 'hp', 'max hp', 'experience']

character_offsets = {'avatar': '0x0002', 'shamino': '0x0022', 'iolo': '0x0042', 
					'mariah': '0x0062', 'geoffrey': '0x0082', 'jaana': '0x00A2', 
					'julia': '0x00C2', 'dupre': '0x00E2', 'katrina': '0x0102', 
					'sentri': '0x0122', 'gwenno': '0x0142', 'johne': '0x0162', 
					'gorne': '0x0182', 'maxwell': '0x01A2', 'toshi': '0x01C2', 
					'saduj': '0x01E2'}

equipment_offsets = {'keys': '0x206', 'gems': '0x207', 'skull keys': '0x20B', 
					'black badge': '0x218', 'magic carpets': '0x20A', 
					'magic axes': '0x240','gold': '0x204'}

stat_offsets = {'strength': '0x0C', 'intelligence': '0x0E', 'dexterity': '0x0D',  
				'magic': '0x0F', 'hp': '0x10', 'max hp': '0x12', 'experience': '0x14'}


#=====================================
# File Alterations
#=====================================
def change(offset: int, val: any) -> None:
	data: List[int] = read()

	if type(val) == list:
		data = list_change(data, offset, val)
	elif type(val) == int:
		data = value_change(data, offset, val)

	write(data)


def read() -> List[int]:
	#Open the saved.gam file and read its
	#contents into a bytearray list
	with open(file_path, 'rb') as file:
		data = list(bytearray(file.read()))
	return data


def write(data: List[int]) -> None:
	#Open filepath and write data to file	
	with open(file_path, 'wb') as file:
		file.write(bytearray(data))


def value_change(data: List[int], offset: int, val: int) -> List[int]:
	#Changes the decimal value at the offset provided
	data[offset] = val
	return data


def list_change(data: List[int], offset: int, vals: List[int]) -> List[int]:
	#Alter the bytearray to match the new values in given list
	for i in range(len(vals)):
		data[offset+i] = vals[i]
	return data


def equip_change(choice: str, val: int) -> None:
	if val > 255:
		val = convert_to_dec_list(val)
	equip = equipment[int(choice)-1]
	offset = hex_to_decimal(equipment_offsets.get(equip))
	change(offset, val)


def stat_change(char_choice: str, stat_choice: str, val: any) -> None:
	if val > 255:
		val = convert_to_dec_list(val)
	#Stat Offset
	stat = stats[int(stat_choice)-1]
	stat_offset = hex_to_decimal(stat_offsets.get(stat))
	#Char Offset
	char = characters[int(char_choice)-1]
	char_offset = hex_to_decimal(character_offsets.get(char))
	#Effective Offset
	offset = stat_offset + char_offset
	change(offset, val)


#=====================================
# Utility Functions
#=====================================
def str_to_ascii(text: str) -> List[int]:
	#Convert str to list and return ascii values
	#for each chr 
	chr_list = list(text)
	int_list = [ord(char) for char in chr_list]
	return int_list


def int_to_hex(int_val: int) -> str:
	#Convert int to hex value
	#Strip 0x
	return(hex(int_val).strip('0x'))


def hex_to_decimal(hex_val: str) -> int:
	#Take hex str val and convert to int
	return(int(hex_val, 16))


def little_endian(val: str) -> List[str]:
	if len(val) == 3:
		byte1 = val[:1]
		byte2 = val[1:]
	else:
		byte1 = val[:2]
		byte2 = val[2:]
	vals = [byte2, byte1]
	return vals


def convert_to_dec_list(val: int) -> List[int]:
	hex_value = int_to_hex(val)
	little = little_endian(hex_value)
	values = [hex_to_decimal(elem) for elem in little]
	return values


def equip_validation(choice: str, val: int) -> int:
	ranges = {'1': 100, '2': 100, '3': 100, '4': 1, '5': 2, '6': 10, '7': 9999}
	valid_range = ranges.get(choice)
	if val not in range(valid_range+1):
		while(True):
			print("Error!")
			equip_val = int(input(f"Enter desired value (0-{valid_range}):"))
			if equip_val in range(valid_range+1):
				break
	return val


def stats_validation(choice: str, val: int) -> int:
	ranges = {'1': 99, '2': 99, '3': 99, '4': 999, '5': 999, '6': 9999, '7': 9999}
	valid_range = ranges.get(choice)
	if val not in range(valid_range+1):
		while(True):
			print("Error!")
			val = int(input(f"Enter desired value (0-{valid_range}):"))
			if val in range(valid_range+1):
				break
	return val


#=====================================
# UI
#=====================================
def banner() -> None:
	print("""
  _    _            _      _    _ _ _   _                   _____ 
 | |  | |          | |    | |  | | | | (_)                 | ____|
 | |__| | __ _  ___| | __ | |  | | | |_ _ _ __ ___   __ _  | |__  
 |  __  |/ _` |/ __| |/ / | |  | | | __| | '_ ` _ \\ / _` | |___ \\ 
 | |  | | (_| | (__|   <  | |__| | | |_| | | | | | | (_| |  ___) |
 |_|  |_|\\__,_|\\___|_|\\_\\  \\____/|_|\\__|_|_| |_| |_|\\__,_| |____/ 
                                                                  
	""")

def main_menu() -> None:
	banner()
	print("1) Stats\n2) Equipment\n3) Exit\n")


def char_menu() -> None:
	print("1) Avatar\n2) Shamino\n3) Iolo\n4) Mariah\n5) Geoffrey\
	\n6) Jaana\n7) Julia\n8) Dupre\n9) Katrina\n10) Sentri\
	\n11) Gwenno\n12) Johne\n13) Gorn\n14) Maxwell\n15) Toshi\
	\n16) Saduj\n17) Exit\n")


def stat_menu() -> None:
	print("1) Strength\n2) Intelligence\n3) Dexterity\n4) HP\
		\n5) Max HP\n6) Experience\n7) Exit\n")


def equip_menu() -> None:
	print("1) Keys\n2) Skull Keys\n3) Gems\n4) Black Badge\
		\n5) Magic Carpets\n6) Magic Axes\n7) Gold\n8) Exit\n")


#=====================================
# Main
#=====================================
def main():
	#Main Menu
	while(True):
		main_menu()
		menu_option = input(">>")

		if menu_option == '3':
			break

		#Character Menu
		if menu_option == '1':
			while(True):
				char_menu()
				character_choice = input(">>")
				if character_choice == '17':
					break

				while(True):
					stat_menu()
					stat_choice = input(">>")
					if stat_choice == '7':
						break

					elif stat_choice == '1' or stat_choice == '2' or stat_choice =='3':
						stat_val = int(input("Enter desired value (0-99): "))
						stat_val = stats_validation(stat_choice, stat_val)
						stat_change(character_choice, stat_choice, stat_val)

					elif stat_choice == '4' or stat_choice == '5':
						stat_val = int(input("Enter desired value (0-999): "))
						stat_val = stats_validation(stat_choice, stat_val)
						stat_change(character_choice, stat_choice, stat_val)

					elif stat_choice == '6':
						stat_val = int(input("Enter desired value (0-9999): "))
						stat_val = stats_validation(stat_choice, stat_val)
						stat_change(character_choice, stat_choice, stat_val)

		#Equipment Menu
		elif menu_option == '2':
			while(True):
				equip_menu()
				equip_choice = input("Choose Equipment: ")
				if equip_choice == '8':
					break
					
				elif equip_choice == '1' or equip_choice == '2' or equip_choice == '3':
					equip_val = int(input("Enter desired value (0-100): "))
					equip_val = equip_validation(equip_choice, equip_val)
					equip_change(equip_choice, equip_val)
					
				elif equip_choice == '4':
					equip_val = int(input("Enter desired value (0-1): "))
					equip_val = equip_validation(equip_choice, equip_val)
					equip_change(equip_choice, equip_val)
					
				elif equip_choice == '5':
					equip_val = int(input("Enter desired value (0-2): "))
					equip_val = equip_validation(equip_choice, equip_val)
					equip_change(equip_choice, equip_val)
					
				elif equip_choice == '6':
					equip_val = int(input("Enter desired value (0-10): "))
					equip_val = equip_validation(equip_choice, equip_val)
					equip_change(equip_choice, equip_val)
				elif equip_choice == '7':
					equip_val = int(input("Enter desired value (0-9999): "))
					equip_val = equip_validation(equip_choice, equip_val)
					equip_change(equip_choice, equip_val)

		#Exit Program
		elif menu_option == '3':
			break

if __name__ == '__main__':
	main()
