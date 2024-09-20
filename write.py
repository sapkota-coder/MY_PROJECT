def main():
    # Prompt the user for input
    input_1 = str(input("INPUT: "))
    
    # Write the input to the file
    with open('saved_data.txt', 'w') as file:
        file.write(input_1)

if __name__ == "__main__":
    main()
