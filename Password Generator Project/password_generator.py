import itertools
import random
import os

# Function to read a file and return its lines as a list
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except IOError:
        print(f"Error: Could not read the file {file_path}.")
        return []

# Function to generate passwords by combining full names and years
def generate_passwords(names_file, years_file, num_passwords):
    names = read_file(names_file)
    years = read_file(years_file)
    
    if not names or not years:
        return []
    
    # Create all possible combinations of full names and years
    all_combinations = list(itertools.product(names, years))
    random.shuffle(all_combinations)  # Shuffle to add randomness
    
    # Create the specified number of passwords from the combinations
    passwords = [f"{name.replace(' ', '').lower()}{year}" for name, year in all_combinations[:num_passwords]]
    return passwords

# Function to save the generated passwords to a file
def save_passwords(passwords, output_file):
    try:
        with open(output_file, 'a') as file:
            for password in passwords:
                file.write(password + '\n')
    except IOError:
        print(f"Error: Could not write to the file {output_file}.")

def main():
    try:
        # Prompt the user for the names file path and validate it
        names_file = input("Enter the path to the names file: ")
        if not os.path.isfile(names_file):
            raise ValueError(f"The file {names_file} does not exist.")
        
        # Prompt the user for the years file path and validate it
        years_file = input("Enter the path to the years file: ")
        if not os.path.isfile(years_file):
            raise ValueError(f"The file {years_file} does not exist.")
        
        # Prompt the user for the number of passwords to generate and validate it
        num_passwords = int(input("Enter the number of passwords to generate: "))
        if num_passwords <= 0:
            raise ValueError("The number of passwords must be a positive integer.")
        
        # Generate the passwords
        passwords = generate_passwords(names_file, years_file, num_passwords)
        if not passwords:
            print("Error: Password generation failed due to missing or invalid input files.")
            return
        
        # Save the passwords to the output file
        output_file = "generated_passwords.txt"
        save_passwords(passwords, output_file)
        print(f"Passwords have been saved to {output_file}")
    
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()


